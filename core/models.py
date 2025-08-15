from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Model, CharField, JSONField, IntegerField


class SlideGenerationRequest(Model):
    topic = CharField(null=True,blank=True)
    content = CharField(null=True,blank=True)
    slides = JSONField(null=True)
    font = CharField(null=True,blank=True)
    color = CharField(null=True,blank=True)
    max_slides = IntegerField(null=True,blank=True,validators = [MaxValueValidator(20)])
    min_slides = IntegerField(null=True,blank=True,validators = [MinValueValidator(1)])

