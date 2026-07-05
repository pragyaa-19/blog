from django.shortcuts import render,redirect
from .models import Post,Media
from django.contrib import messages
from homepage.models import Follow

def upload_photo(request):
    
    if request.method != 'POST':
        return render(request, 'photo_uploader/upload_photo.html')
        
    user = request.user
    caption = request.POST.get("caption")
    files = request.FILES.getlist("media")
        
    if len(files) > 10:
        messages.error(request,"YOu can only selelct 10 photos.")
        return redirect('index')
    
        
    post = Post.objects.create(
        user = user,
        caption = caption
    )

    for f in files:
        Media.objects.create(
            post=post,
            file = f
        )
    messages.success(request,"Posted")
    return redirect('index')


def display(request):
    following = Follow.objects.filter(follower=request.user).values_list("following_id", flat=True)

    #posts = Media.objects.all() #it will fetch eveyhting evey image but we dont want that are motive is to make it look like insta
    posts = Post.objects.filter(user__in=following).order_by('-created_at')
    return render(request, 'photo_uploader/display_photo.html',{"posts":posts})
