import hashlib

from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.models import SlideGenerationRequest
from core.nlp_models import GeminiAGI
from core.serializers import SlideGenerationSerializer


# Serializers define the API representation.
class GenerateTemplates(mixins.CreateModelMixin,GenericViewSet):
    serializer_class = SlideGenerationSerializer
    queryset = SlideGenerationRequest.objects.all()

    def create(self, request):
        data = request.data
        topic = data.get('topic')
        content = data.get('content')
        if not topic and not content:
            return Response({'error': 'topic or content is required'}, status=status.HTTP_400_BAD_REQUEST)
        cache_key = topic
        if content:
            md5_hash_object = hashlib.md5()
            # Encode the string to bytes before updating the hash object
            md5_hash_object.update(content.encode('utf-8'))
            md5_hex_digest = md5_hash_object.hexdigest()
            cache_key += md5_hex_digest
        slides = GeminiAGI.generate_slides(topic,content,min_slides=data.get("min_slides"),
                                           max_slides=data.get("max_slides"),cache_key=cache_key)
        slides_json = []
        for slide in slides:
            image_placeholder = slide.image_placeholder
            if image_placeholder:
                # create a new instance of FileSystemStorage
                fileurl = GeminiAGI.generate_image(image_placeholder, cache_key=image_placeholder)
                if not fileurl:
                    continue
                slide.image = fileurl
                slides_json.append(slide.dict())
        serializer =SlideGenerationSerializer(data=data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save(slides =slides_json )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RetrieveTemplates(GenericViewSet, mixins.RetrieveModelMixin,mixins.ListModelMixin):
    serializer_class = SlideGenerationSerializer
    queryset = SlideGenerationRequest.objects.all()

    







