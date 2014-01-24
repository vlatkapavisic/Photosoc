from django.contrib import admin
from photosoc_app.models import *

class PhotoAdmin(admin.ModelAdmin):
	pass
	
class TagAdmin(admin.ModelAdmin):	
	pass
	
class FriendshipAdmin(admin.ModelAdmin):
	pass
	

	
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Friendship, FriendshipAdmin)

