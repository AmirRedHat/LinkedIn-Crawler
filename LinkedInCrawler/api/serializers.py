from rest_framework.serializers import ModelSerializer
from .models import *


class LinkedinUserSerializer(ModelSerializer):
   class Meta:
      model = LinkedinUser
      fields = "__all__"


class EducationSerializer(ModelSerializer):
   class Meta:
      model = Education
      fields = "__all__"


class ExperienceSerializer(ModelSerializer):
   class Meta:
      model = Experience
      fields = "__all__"


class NestedLinkedinUserSerializer(ModelSerializer):
   educations = EducationSerializer(many=True, read_only=True)
   experiences = ExperienceSerializer(many=True, read_only=True)

   class Meta:
      model = LinkedinUser
      fields = "__all__"