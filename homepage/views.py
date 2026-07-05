from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required 
from .models import Blog,Comments,Reaction,Save,Follow
from .forms import BlogForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.conf import settings
from accounts.models import MyUser
from photo_uploader.models import Post,Media

#handling hearts
def react_blog(request, blog_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    blog = get_object_or_404(Blog, id=blog_id)

    reaction_obj = Reaction.objects.filter(
        user=request.user,
        blog=blog
    ).first()

    if reaction_obj and reaction_obj.reaction == "Like":

        reaction_obj.delete()

        return JsonResponse({
            "liked": False
        })

    if reaction_obj:
        reaction_obj.reaction = "Like"
        reaction_obj.save()

    else:
        Reaction.objects.create(
            user=request.user,
            blog=blog,
            reaction="Like"
        )

    return JsonResponse({
        "liked": True
    })

@login_required
def index(request):
    search_query = request.GET.get('q','') # getting the text from user
    if search_query:
        blog_list = blog_list.filter(
            Q(title__icontains=search_query) |
            Q(author__username__icontains=search_query))
        
    
    
    following = Follow.objects.filter(follower=request.user).values_list("following_id", flat=True)
    blog_list = Blog.objects.filter(published=True,author__in=following).order_by('-created_at')   
    paginator = Paginator(blog_list,49)
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    
    liked_blogs = Reaction.objects.filter(
        user=request.user,
        reaction="Like"
        ).values_list("blog_id", flat=True)
    

    return render(request,"homepage/index.html",
                  {'blogs':blogs,
                   "liked_blogs":liked_blogs,
                   "search_query":search_query,})

@login_required
def create_blog(request):
    if request.method == 'POST':

        title = request.POST.get('title')
        content = request.POST.get('content')

        is_published = request.POST.get('is_published') == 'on'

        status = 'published' if is_published else 'draft'

        Blog.objects.create(
        title=title,
        content=content,
        author=request.user,
        published=is_published
        )

        messages.success(request, "Blog saved!")
        return redirect('dashboard')

    return render(request, 'homepage/create.html')



@login_required
def dashboard(request):
    #all but we need only posted 
    blogs = Blog.objects.filter(author=request.user,published=True).order_by('-created_at')
    #like
    
    liked_blogs = Reaction.objects.filter(
        user=request.user,
        reaction="Like").values_list("blog_id", flat=True)

    return render(request,'homepage/dashboard.html',{"blogs":blogs,"liked_blogs":liked_blogs})



def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    
    if not request.user.is_authenticated:
        return redirect("login")
    
    if request.method == "POST":
        comment_text = request.POST.get("comment")
        
        if not comment_text.strip():
            return JsonResponse(
        {"error": "Empty comment"},
        status=400
    )
        comment = Comments.objects.create(
                blog=blog,
                user=request.user,
                content = comment_text
            )

        return JsonResponse({
        "username": comment.user.username,
        "content": comment.content,
        "created_at": comment.created_at.strftime("%d %b %Y")
    })
        
    liked_blogs = Reaction.objects.filter(
        user=request.user,
        reaction="Like").values_list("blog_id", flat=True)
    
    comments = Comments.objects.filter(blog=blog).order_by("-id")
            
    return render(request, 'homepage/blog_details.html', {'blog': blog,'comments': comments,"liked_blogs":liked_blogs})



def blog_edit(request,slug):
    blog = get_object_or_404(Blog,slug=slug)

    if blog.author != request.user:
        messages.error(request,"You are not allowed to edit this blog.")
        return redirect("index")
    
    if request.method == 'POST':
        
        form  = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request,"Blog updated Successfully!!")
            return redirect("index")
    else:
        form = BlogForm(instance=blog)
    return render(request,'homepage/edit_blog.html',{"form":form})



def blog_delete(request,slug) :
    blog = get_object_or_404(Blog,slug=slug)

    if blog.author != request.user:
        messages.error(request,"You are not allowed to delete this post")
        return redirect("index")
    
    if request.method == 'POST':
        blog.delete()
        messages.success(request,"Blog Deleted Succesfully")
        return redirect('index')
    
    return render(request,'homepage/delete_blog.html',{"blog":blog})


def about(request):
    return render(request,'about.html')



def explore(request):
    all_blogs = Blog.objects.filter(published=True).order_by('-created_at')
    return render(request,'explore.html',{"all_blogs":all_blogs})

def author_profile(request,username):
    author = get_object_or_404(MyUser,username=username)
    
    blogs = Blog.objects.filter(
    author=author,
    published=True).order_by('-created_at')
    
    followers = Follow.objects.filter(following=author).count()
    is_following = False
    posts = Post.objects.filter(user=author)

    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=author
        ).exists()

    
    return render(request,'homepage/author_profile.html',{
        "author": author,
        "blogs": blogs,
        "is_following": is_following,
        "followers":followers,
        "posts":posts,
        
    })
    
    



def follow(request):

    if request.method != "POST":
        return redirect("index")  # or wherever you want

    currfollower = request.user
    author_id = request.POST.get("author_id")

    currfollowing = MyUser.objects.get(id=author_id)

    if currfollower == currfollowing:
        messages.error(request, "You can't follow yourself!")
        return redirect("author_profile", currfollowing.username)

    follow_obj = Follow.objects.filter(
        follower=currfollower,
        following=currfollowing
    )

    if follow_obj.exists():
        follow_obj.delete()
    else:
        Follow.objects.create(
            follower=currfollower,
            following=currfollowing
        )

    return redirect("author_profile", currfollowing.username)

def save(request):
    if request.method != "POST":
        return redirect("index")
    # pragya saves blog #4
    user = request.user
    blog_id = request.POST.get("blog_id")
    
    save_obj = Save.objects.filter(
        user=user,
        blog=blog_id)
    
    if save_obj.exists():
        save_obj.delete()
        messages.error(request,"Blog unsaved!")
        
    else:
        saving_blog = Blog.objects.get(id=blog_id)
        
        Save.objects.create(
            user=user,
            blog=saving_blog
        )
        messages.success(request,"Blog saved successfully!")
        
    return redirect("index")



def saved(request):
    saved = Save.objects.filter(user=request.user)
    return render(request,'homepage/saved.html', {"saved": saved})
    
    
def drafts(request):
    # not punlished = drafts
    drafts = Blog.objects.filter(author=request.user,published=False).order_by('-created_at')
    return render(request,'homepage/drafts.html',{"drafts":drafts})
    
    