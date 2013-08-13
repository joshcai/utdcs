from django.db import models

# Create your models here.



class Post(models.Model):
	title = models.CharField(max_length=120)
	content = models.TextField()
	content_rendered = models.TextField(default="")
	author = models.CharField(max_length=120)
	date = models.DateTimeField('date created')
	date_str = models.CharField(max_length=120)
	deleted = models.BooleanField(default=False)
	def __unicode__(self):
		return self.title
