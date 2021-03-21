from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
	name = serializers.CharField()
	name = serializers.SerializerMethodField()
	def get_name(self,obj):
		num = obj.author
		print("#############")
		print(num)
		#uname = User.objects.get(pk=num)
		#return uname.username
	class Meta:
		model = Post
		fields = ['title','content','created_at','photo','slug','author','name']