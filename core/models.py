from django.db import models
from django.utils import timezone
from blogAPI.utils import *
# Create your models here.


class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.CharField(max_length=200)
	#content  = models.TextField()
	slug     = models.SlugField(max_length=200,null=True,blank=True)
	photo    = models.ImageField(upload_to='profile_pics',blank=True,null=True)
	#author   = models.Foreignkey(User,on_delete=models.CASCADE)
	#likes    = models.ManyToManyField(User,blank=True,related_name="like")
	#dislikes = models.ManyToManyField(User,blank=True,related_name="dislikes")
	created_at = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f"{self.title} {self.id}"

	def save(self, *args, **kwargs):  # new
		if not self.slug:
			self.slug = unique_slug_generator(self)
		return super().save(*args, **kwargs)		




