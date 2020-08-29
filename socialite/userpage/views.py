from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import DeleteView

from django.contrib.auth.models import User
from .models import Post, Profile, Like, Following
# Create your views here.
def userhome_page(request):
    posts = Post.objects.all()

    for p in posts:
        p.liked=False
        liked_user = Like.objects.filter(post=p, user__username=request.user)
        if liked_user:
            p.liked=True

    context = {'posts': posts}
    template = 'userpage/home_page.html'
    return render(request, template, context)


def postcreate(request):
    if request.method == 'POST':
        image = request.POST.get('image_field')
        caption = request.POST.get('caption_field')

        post = Post(caption=caption, image=image, user=request.user)
        post.save()
        messages.success(request, "Post Created Successfully")
        return redirect('/userpage/homepage/')

    else:
        messages.error(request, "Something went wrong")
        return redirect('/userpage/homepage/')

# class Delete_Post(DeleteView):
#     model = Post
#     success_url = "/userpage/homepage/"

def delete_post(request, id):
    try:
        post = Post.objects.get(id=id)
    except post.DoesNotExists:
        pass
    if post is not None:
        post.delete()
        messages.info(request, "Post has deleted successfully")
        return redirect('/userpage/homepage/')
    else:
        pass

def user_profile(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        pass

    if user:
        profile = get_object_or_404(Profile, user__username=user)
        post = Post.objects.filter(user=user)


        followed = False
        dd = Following.objects.filter(user__username=user, followedby__username=request.user)
        if dd:
            followed = True

        context = {'profile_detail': profile, 'post':post, 'followed': followed, 'follower':dd}
    template = 'userpage/user_profile.html'
    return render(request, template, context)


def likes(request, id):
    try:
        post = Post.objects.get(id=id)
        print("POST", post)
    except:
        return HttpResponse("Post is not found")

    obj, create = Like.objects.get_or_create(post=post)
    if obj:
        print("Post obj already created")
        obj.user.add(request.user)
        obj.likes+=1
        obj.save()
        messages.info(request, "Liked")
        return redirect('/userpage/homepage/')
    else:
        print("Post obj is newley created")
        # obj.user.add(request.user)
        create.user.add(request.user)
        return redirect('/userpage/homepage/')

def remove_like(request, id):
    try:
        post = Post.objects.get(id=id)
        print("POST", post)
    except:
        return HttpResponse("Post is not found")

    like = Like.objects.get(post__caption=post, user__username=request.user)
    # for like in like_user:
    like.user.remove(request.user)
    like.likes-=1
    like.save()
    # return redirect('/userpage/homepage/')
    return  HttpResponseRedirect(redirect_to="/userpage/homepage/")


def follow_user(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        raise HttpResponse('User Not found')

    object, create = Following.objects.get_or_create(user=user)
    if object:
        object.followedby.add(request.user)
        object.followcount+=1
        object.save()
        messages.info(request, 'Followed successfully')
        print("Followed")
        return HttpResponseRedirect(redirect_to='/userpage/homepage/')

def unfollow(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        raise HttpResponse('No Such User')

    followed = Following.objects.get(user__username=user, followedby__username=request.user)
    if followed:
        followed.followedby.remove(request.user)
        followed.followcount-=1
        followed.save()
        return HttpResponseRedirect(redirect_to='/userpage/homepage/')


def serach_item(request):
    pass