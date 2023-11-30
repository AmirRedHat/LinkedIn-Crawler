import os 
import sys
import django
from django.shortcuts import get_list_or_404
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LinkedInCrawler.settings")
django.setup()
from api.models import *
from api.serializers import *



def bulkCreateEducation(data):
   Education.objects.bulk_create(data)


def bulkCreateExperience(data):
   Experience.objects.bulk_create(data)


def insertProfileDetail(data: list):
   bulk_education_data = []
   bulk_experience_data = []
   for user in data:
      detail = user.pop("details", False)

      luser_filter = LinkedinUser.objects.filter(profile_link=user["profile_link"])
      if luser_filter.count() == 0:
         if detail:
            skills = " | ".join(detail["skills_details"])
            user["skills"] += " || " + skills

         luser = LinkedinUser(**user)
         luser.save()
      else:
         luser = luser_filter.first()


      if detail:
         luser.is_completed = True
         education = detail["education_details"]
         experience = detail["experience_details"]
         
         for edu in education:
            edu["linkedin_user"] = luser
            if Education.objects.filter(linkedin_user=luser).count() == 0:
               bulk_education_data.append(Education(**edu))
         
         for exp in experience:
            exp["linkedin_user"] = luser
            if Experience.objects.filter(linkedin_user=luser).count() == 0:
               bulk_experience_data.append(Experience(**exp))

         luser.save()


   if bulk_education_data:
      bulkCreateEducation(bulk_education_data)

   if bulk_experience_data:
      bulkCreateExperience(bulk_experience_data)


def getProfileLinks():
   return [i[0] for i in LinkedinUser.objects.all().values_list("profile_link", flat=False)]


def getUncompletedProfiles():
   return LinkedinUser.objects.filter(is_completed=False)


def getEducationProfile(user):
   return Education.objects.filter(linkedin_user=user)


def getExperienceProfile(user):
   return Experience.objects.filter(linkedin_user=user)


def getProfileDetails():
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

   return data


def getNestedProfileDetail():
   linkedin_users = LinkedinUser.objects.prefetch_related("education_user").prefetch_related("experience_user").all()
   return NestedLinkedinUserSerializer(linkedin_users, many=True).data
