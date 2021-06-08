from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.serializers import  CustomUserSerializerWithPosts
from core.models import Post
#from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your views here.

@api_view(['GET'])
def user_details(request,user_name):
    if request.method == 'GET':
        try:
            user = User.objects.get(username=user_name)
        except:
                print ("go further")
                return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = CustomUserSerializerWithPosts(user)
        return Response(serializer.data)				

            