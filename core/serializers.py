from rest_framework import serializers
from .models import Comment, Post
from django.contrib.auth.models import User
from django.core.paginator import Paginator


class CustomUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username', 'first_name')

class CommentSerializer(serializers.ModelSerializer):
	author = CustomUserSerializer(read_only=True)
	class Meta:
		model = Comment
		fields= ('id', 'author','description','created_at')
		

class PostSerializer(serializers.ModelSerializer):
	author = CustomUserSerializer(read_only=True)
	post_comments = serializers.SerializerMethodField('paginated_post_comments')
	number_of_comments = serializers.SerializerMethodField()
	photo = serializers.ImageField(max_length=None, allow_empty_file=False)
	class Meta:
		model = Post
		fields = ['caption','created_at','slug','author','photo','post_comments','number_of_comments','location']

	def get_number_of_comments(self,obj):
		return Comment.objects.filter(post=obj).count()

	def paginated_post_comments(self, obj):
		page_size = 2
		#paginator = Paginator(Comment.objects.filter(post=obj), page_size)
		#page = self.context['request'].query_params.get('page') or 1
		#post_comments = paginator.page(page)
		serializer = CommentSerializer(Comment.objects.filter(post=obj), many=True)
		return serializer.data	


        