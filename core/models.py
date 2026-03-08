from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Model, CharField, JSONField, IntegerField


class SlideGenerationRequest(Model):
    topic = CharField(null=True,blank=True,max_length=20)
    content = CharField(null=True,blank=True,max_length=20)
    slides = JSONField(null=True)
    font = CharField(null=True,blank=True,max_length=20)
    color = CharField(null=True,blank=True,max_length=20)
    max_slides = IntegerField(null=True,blank=True,validators = [MaxValueValidator(20)])
    min_slides = IntegerField(null=True,blank=True,validators = [MinValueValidator(1)])
    provider = CharField(null=True,blank=True,choices = [('ollama','ollama'),('gemini','gemini')],max_length=20)
