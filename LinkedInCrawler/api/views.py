from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import *
from .serializers import *
from .permissions import AccessLevelPermissionOrAdmin
# Create your views here.



class LinkedinUsersView(ListAPIView):
   serializer_class = LinkedinUserSerializer
   model = serializer_class.Meta.model
   queryset = model.objects.all()
   permission_classes = (IsAuthenticated,)


class LinkedinUserView(RetrieveAPIView):
   serializer_class = LinkedinUserSerializer
   model = serializer_class.Meta.model
   queryset = model.objects.all()
   permission_classes = (IsAuthenticated,)
   lookup_field = "pk"


class LinkedinUserDetailView(APIView):

   permission_classes = (IsAuthenticated, AccessLevelPermissionOrAdmin)

   def get(self, *args, **kwargs):
      pk = kwargs.get("pk")
      linkedin_user = get_object_or_404(LinkedinUser, pk=pk)
      educations = Education.objects.filter(linkedin_user=linkedin_user)
      experiences = Experience.objects.filter(linkedin_user=linkedin_user)
      data = {
         "user": LinkedinUserSerializer(linkedin_user).data,
         "educations": EducationSerializer(educations, many=True).data,
         "experiences": ExperienceSerializer(experiences, many=True).data
      }
      return Response(data, 200)


class LinkedinUsersDetailView(APIView):
   permission_classes = (IsAuthenticated, AccessLevelPermissionOrAdmin)

   def get(self, *args, **kwargs):
      linkedin_users = LinkedinUser.objects.all()
      data = list()

      for luser in linkedin_users:
         educations = Education.objects.filter(linkedin_user=luser)
         experiences = Experience.objects.filter(linkedin_user=luser)
         data.append({
            "user": LinkedinUserSerializer(luser).data,
            "educations": EducationSerializer(educations, many=True).data,
            "experiences": ExperienceSerializer(experiences, many=True).data
         })
      return Response(data, 200)



class LinkedinUserKeyFilterView(ListAPIView):
   serializer_class = LinkedinUserSerializer
   model = serializer_class.Meta.model
   queryset = model.objects.all()
   permission_classes = (IsAuthenticated,)
   lookup_field = "key"

   def get_queryset(self):
      return LinkedinUser.objects.filter(skills__icontains=self.kwargs.get(self.lookup_field, ""))
