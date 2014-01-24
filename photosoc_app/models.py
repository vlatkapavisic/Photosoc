from django.db import models
from django.contrib.auth.models import User
from django.core.files import File


class Photo(models.Model):
	user=models.ForeignKey(User)
	photo=models.ImageField(upload_to='uploaded_photos/',blank=True,null=True)
	caption=models.CharField(max_length=200)
	pub_date=models.DateTimeField(auto_now_add=True)
	private=models.BooleanField() 
	likes=models.IntegerField(default=0)
	likers=models.ManyToManyField(User, related_name='likers')
	
	def __unicode__(self):
		return self.caption
	
	
class Tag(models.Model):
	name=models.CharField(max_length=100)
	photo=models.ManyToManyField(Photo)
	
	def __unicode__(self):
		return self.name
	
	
class Friendship(models.Model):
	from_friend=models.ForeignKey(
		User, related_name='friend_set'
		)
	to_friend=models.ForeignKey(
		User, related_name='to_friend_set'
		)
		
	def __unicode__(self):
		return u'%s, %s' % (self.from_friend.username, self.to_friend.username)
			
	class Meta:
		unique_together=(('to_friend', 'from_friend'), )
