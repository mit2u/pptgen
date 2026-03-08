import re
from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from google import genai
from google.genai import types
from core.decorators import cache_output
from PIL import Image

from core.utils import Slide

from abc import ABC, abstractmethod


class AGI(ABC):
    """
    Base class for all AI providers (Gemini, Qwen etc.)
    """

    @classmethod
    @abstractmethod
    def call_model(cls, prompt, config=None):
        pass

    @classmethod
    @cache_output
    def generate_slides(cls, topic, content=None, min_slides=None, max_slides=None):

        if not min_slides:
            min_slides = 1

        if not max_slides:
            max_slides = 4

        prompt = f"""
        Generate presentation slides for the topic: {topic}.

        REQUIREMENTS:
        - Return ONLY valid JSON.
        - Support 4 slide layouts: \
                         1 - Title slide \
                         2 - Bullet points (3-5 points) \
                         3 - Two-column layout \
                         4 - Content with image placeholder \

        Constraints:
        - Minimum slides: {min_slides}
        - Maximum slides: {max_slides}

        Example format:
        [
          {{ 
            "title": "Slide title",
            "slide_type": 3,
            "col1_bullet_points": ["point 3", "point 4"],
            "col2_bullet_points": ["point 5", "point 6"],
          }},\
          {{
            "title": "Slide title",
            "slide_type": 2,
            "bullet_points": ["point 1", "point 2"],
          }},
          {{
          "title": "Slide title",
          "slide_type": 4,
          "image_placeholder": "description",
          "content":"some content",
          }}
        ]
        """

        if content:
            prompt += "\nInclude this content:\n" + content

        return cls.call_model(prompt,{"config": types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=list[Slide])}
            )

    @classmethod
    @cache_output
    def generate_image(cls, image_placeholder):

        image_placeholder = (
            image_placeholder.replace(".", "")
            .replace("/", "")
            .replace("\\", "")
            .replace(",", "")
            .replace(":", "")
            .replace(";", "")
            .lower()
        )

        prompt = f"Generate image for {image_placeholder}"

        response = cls.call_model(
            prompt,
            {
                "model": settings.IMAGE_GENERATION,
                "config": types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"]
                ),
            },
        )
        print(response)
        if not response:
            return None
        fileurl = None

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:

                image = Image.open(BytesIO(part.inline_data.data))

                image_io = BytesIO()
                image.save(image_io, format="PNG")

                cf = ContentFile(image_io.getvalue(), name=image_placeholder)

                file_name = image_placeholder.replace(" ", "_") + ".png"

                fs = FileSystemStorage()
                file = fs.save(file_name, cf)

                fileurl = fs.url(file)[1:]

        return fileurl


class GeminiAGI(AGI):
    """
    Gemini model implementation
    """



    @classmethod
    def call_model(cls, prompt, config=None):

        # create client using API key from Django settings
        client = genai.Client(api_key=getattr(settings, "GEMINI_API_KEY", None))

        if config is None:
            config = {}
        model = config.get("model", settings.TEXT_GENERATION)
        config = config.get("config")
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=config,
            )
        except Exception as e:
            print(e)
            return

        print(response)
        if config.response_schema:
            return [ item.dict() for item in response.parsed]
        return response


class QwenAGI(AGI):
    """
    Placeholder for Qwen implementation
    """

    @classmethod
    def call_model(cls, prompt, config=None):

        host = getattr(settings, "OLLAMA_HOST", "http://localhost:11434")
        model = getattr(settings, "QWEN_MODEL", "qwen3.5:4b")


        # allow overriding model only if config is a dict (Gemini uses GenerateContentConfig)
        if isinstance(config, dict):
            model = config.get("model", model)

        from ollama import Client, web_search, web_fetch

        client = Client(host, timeout=360.0)

        messages = [{'role': 'user', 'content':prompt}]
        try:
            # Pass the web search and web fetch functions as tools
            response = client.chat(
                model=model,  # Use a model with strong tool-use capabilities
                messages=messages,
                tools=[web_search, web_fetch],
                # You can also enable 'thinking' to see the model's reasoning process
                #think=True
            )
        except Exception as e:
            print(e)
        print(response.message['content'])

        try:
            return eval(response.message["content"].replace("```", "").replace("json", ""))
        except Exception as e:
            print(e)
            return response.message["content"]


    @classmethod
    def image_generation(cls):
        from openai import OpenAI

        client = OpenAI(
            base_url='http://localhost:11434/v1/',
            api_key='ollama',  # required but ignored
        )

        response = client.images.generate(
            model='x/z-image-turbo',
            prompt='A cute robot learning to paint',
            size='1024x1024',
            response_format='b64_json',
        )
        print(response.data[0].b64_json[:50] + '...')