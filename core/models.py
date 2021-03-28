from django.db import models
from django.utils import timezone
from blogAPI.utils import *
from django.contrib.auth.models import User
# Create your models here.
from PIL import Image


def user_directory_path(instance, filename):
    return 'posts/{0}/{1}'.format(instance.id, filename)


class Post(models.Model):
	photo  = models.FileField(upload_to=user_directory_path, null=True)
	slug     = models.SlugField(max_length=200,null=True,blank=True)
	author   = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	location = models.CharField(max_length=30, blank=True)
	#likes    = models.ManyToManyField(User,blank=True,related_name="like")
	#dislikes = models.ManyToManyField(User,blank=True,related_name="dislikes")
	created_at = models.DateTimeField(default=timezone.now)
	caption = models.CharField(max_length=255, null=True)

	def __str__(self):
		return f"{self.author} {self.id}"

	def save(self, *args, **kwargs):  # new
		if not self.slug:
			self.slug = unique_slug_generator(self)
		return super().save(*args, **kwargs)		




class PostResource(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    resource = models.FileField(upload_to='profile_pics/', null=True)
    caption = models.CharField(max_length=255, null=True)

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	description = models.TextField()
	parent = models.ForeignKey('self', on_delete=models.CASCADE,related_name="replies", null=True,blank=True)
	created_at = models.DateTimeField(default=timezone.now)



class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path,blank=True,null=True)

    def __str__(self):
        return f"{self.user.username} Profile"
    '''
    def save(self,*args, **kawrgs):
        super().save(*args, **kawrgs)  
        print("FUCK FUCK ",self.image.name)  
        img = Image.open(self.image.name)

        if img.height > 300 and img.width > 300:
            out_size = (300,300)
            img.thumbnail(out_size)
            img.save(self.image.name)

    
  	'''        