from rest_framework import serializers
from core.models import  Post, UserProfile
from django.contrib.auth.models import User



class CustomUserSerializer(serializers.ModelSerializer):
	image      = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = ('id','username', 'first_name','image')
	def get_image(self,obj):
		return '/media/'+UserProfile.objects.get(user=obj).image.name	
	







        