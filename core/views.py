from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from core.serializers import PostSerializer, CustomUserSerializerWithPosts
from .models import Post
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	lookup_field = 'slug'


@api_view(['GET','POST'])
def post_list(request):


	if request.method=='GET':
		print("GET REQUEST BEING PROCESSED")
		posts = Post.objects.all()
		serializer = PostSerializer(posts,many=True)
		return Response(serializer.data)


	elif request.method=='POST':
		print("POST REQUEST BEING PROCESSED")
		serializer = PostSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT', 'DELETE'])
def post_detail(request, slug):
	try:
		post = Post.objects.get(slug=slug)
	except Post.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	
	if request.method == "GET":
		serializer = PostSerializer(post)
		return Response(serializer.data)

	elif request.method == "PUT":
		serializer = PostSerializer(post, data=request.data)	
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)		

	
	elif request.method == "DELETE":
		post.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)				



@api_view(['GET'])
def user_details(request,user_name):
	if request.method == 'GET':
		user = User.objects.get(username=user_name)
		serializer = CustomUserSerializerWithPosts(user)
		return Response(serializer.data)