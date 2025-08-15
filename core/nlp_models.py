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




class GeminiAGI:


    @classmethod
    @cache_output
    def generate_slides(cls,topic,content,min_slides=None,max_slides = None):
        if not min_slides:
            min_slides = 1
        if not max_slides:
            max_slides = 20
        client = genai.Client()
        prompt = f"Generate slides for topic : {topic} using following instructions : \
                    # Min {min_slides} of slides should be present upto maximum {max_slides} \
                    # Support 4 slide layouts: \
                         1 - Title slide \
                         2 - Bullet points (3-5 points) \
                         3 - Two-column layout \
                         4 - Content with image placeholder \
                    # Include source citations in the slides. "
        if content:
            prompt += "Include given content in the slides : " +content

        response = client.models.generate_content(
          model=settings.TEXT_GENERATION, contents=prompt,config={
            "response_mime_type": "application/json",
            "response_schema": list[Slide],
            }
          )
        print(response.parsed)
        return response.parsed


    @classmethod
    @cache_output
    def generate_image(cls,image_placeholder):
    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
        client = genai.Client()
        re.sub(r'[^a-zA-Z0-9/:._\-~]', '', image_placeholder)
        prompt = f"Generate Image for {image_placeholder} to be used into PPT"
        response = client.models.generate_content(
            model=settings.IMAGE_GENERATION, contents=prompt,config=types.GenerateContentConfig(
            response_modalities=['IMAGE','TEXT']
        )
        )
        fileurl = None
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image = Image.open(BytesIO((part.inline_data.data)))
                # Create a BytesIO object to hold the image data in memory
                image_io = BytesIO()

                # Save the PngImageFile to the BytesIO object as PNG
                # You might need to specify the format based on the actual image type
                image.save(image_io, format='PNG')
                cf = ContentFile(image_io.getvalue(), name=image_placeholder)
                file_name = image_placeholder.replace(' ', '_') + '.png'
                fs = FileSystemStorage()
                file = fs.save(file_name, cf)
                # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
                fileurl = fs.url(file)[1:]
        print(fileurl)
        return fileurl