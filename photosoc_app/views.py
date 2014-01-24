from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from photosoc_app.forms import *
from photosoc_app.models import *
from django.contrib.auth.decorators import login_required


def main_page(request):
	return render_to_response('main_page.html',RequestContext(request))
	
	
def users_page(request):
	users = User.objects.all()
	variables = RequestContext(request,{
	'users': users,
	})
	return render_to_response('users_page.html', variables)
	
	
def user_page(request, uname):
	userr=User.objects.get(username=uname)
	logged_in_user=request.user
	friends=[friendship.to_friend for friendship in userr.friend_set.all()]
	if request.user.is_authenticated():
		is_friend=Friendship.objects.filter(from_friend=request.user, to_friend=userr)
	else:
		is_friend=False
	if logged_in_user==userr:
		photos=userr.photo_set.all()
		is_friend=True
	else:
		if is_friend:
			photos=userr.photo_set.all()
		else:
			photos=userr.photo_set.filter(private=False)
	variables=RequestContext(request,{
	'userr': userr,
	'photos': photos,
	'friends':friends,
	'is_friend': is_friend,
	'logged_in_user':logged_in_user,
	})
	return render_to_response('user_page.html', variables)


def photos_page(request):
	user=request.user
	friends=[friendship.to_friend for friendship in request.user.friend_set.all()]
	photos=[]
	for friend in friends:
		photos.extend(friend.photo_set.all())
	photos.extend(user.photo_set.all())
	public_photos=Photo.objects.filter(private=False)
	for photo in public_photos:
		if photo not in photos:
			photos.append(photo)
	photos.sort(key=lambda x: x.pub_date, reverse=True)
	variables = RequestContext(request,{
	'photos': photos,
	'user':user,
	})
	return render_to_response('photos_page.html', variables)


def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')


def register_page(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
				username=form.cleaned_data['username'],
				first_name=form.cleaned_data['first_name'],
				last_name=form.cleaned_data['last_name'],
				password=form.cleaned_data['password1'],
				email=form.cleaned_data['email']
			)
		return HttpResponseRedirect('/register/success/')
	else:
		form = RegistrationForm()
		variables = RequestContext(request, {
		'form': form
	})
	return render_to_response('registration/register.html',variables)


@login_required
def tag_photo_page(request, photo_id):
	photo=Photo.objects.get(id=photo_id)
	if request.method=='POST':
		form=PhotoTagForm(request.POST)
		if form.is_valid():
			tag_names=form.cleaned_data['tags'].split('  ')
		for tag_name in tag_names:
				newtag, c=Tag.objects.get_or_create(name=tag_name)
				newtag.save()
				photo.tag_set.add(newtag)
		photo.save()
		return HttpResponseRedirect('/photos')	
	else:
		form=PhotoTagForm()
	variables=RequestContext(request,{
		'form':form
	})
	return render_to_response('tag_photo_page.html', variables)
	

@login_required
def upload_photo(request):
	if request.method == 'POST':
		form = PhotoUploadForm(request.POST, request.FILES)
		if form.is_valid():
			newpic, created=Photo.objects.get_or_create(user=request.user, photo=request.FILES['photo'], 
			caption=form.cleaned_data['caption'], private=form.cleaned_data['private'])
			if not created:
				newpic.tag_set.clear()
			tag_names=form.cleaned_data['tags'].split('  ')	
			for tag_name in tag_names:
				newtag, c=Tag.objects.get_or_create(name=tag_name)
				newtag.save()
				newpic.tag_set.add(newtag)
			newpic.save()
			# Redirect to the document list after POST
			return HttpResponseRedirect('/upload')
	else:
		form = PhotoUploadForm() 
	variables=RequestContext(request,{
		'form':form
	})
	return render_to_response('upload_photo.html', variables)
		
	
def friends_page(request):
	friends=[friendship.to_friend for friendship in request.user.friend_set.all()]	
	variables=RequestContext(request,{
		'friends':friends,
	})
	return render_to_response('friends_page.html', variables)
	
	
@login_required
def friend_add(request):
	if 'username' in request.GET:
		friend = get_object_or_404(User, username=request.GET['username'])
		friendship = Friendship(
			from_friend=request.user,
			to_friend=friend
			)
		friendship.save()
		return HttpResponseRedirect('/users/')
	else:
		raise Http404
		

@login_required
def like_photo_page(request):
	if 'id' in request.GET:
		try:
			id=request.GET['id']
			liked_photo=Photo.objects.get(id=id)
			liker=liked_photo.likers.filter(username=request.user.username)
			if not liker:
				liked_photo.likes += 1
				liked_photo.likers.add(request.user)
				liked_photo.save()
		except Photo.DoesNotExist:
			raise Http404('Photo not found.')
	if 'HTTP_REFERER' in request.META:
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	return HttpResponseRedirect('/')


@login_required
def unlike_photo_page(request):
	if 'id' in request.GET:
		try:
			id=request.GET['id']
			liked_photo=Photo.objects.get(id=id)
			liker=liked_photo.likers.filter(username=request.user.username)
			liked_photo.likes -= 1
			liked_photo.likers.remove(request.user)
			liked_photo.save()
		except Photo.DoesNotExist:
			raise Http404('Photo not found.')
	if 'HTTP_REFERER' in request.META:
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	return HttpResponseRedirect('/')
			
	
def photo_comments_page(request, photo_id):
	photo=get_object_or_404(Photo, id=photo_id)
	variables=RequestContext(request, {
	'photo': photo
	})
	return render_to_response('photo_comments_page.html', variables)
