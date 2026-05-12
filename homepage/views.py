from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required 
from .models import Blog
from .forms import BlogForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse


def index(request):
    blog_list = Blog.objects.filter(published=True).order_by('-created_at')

    paginator = Paginator(blog_list,6)
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)

    return render(request,"homepage/index.html",{'blogs':blogs})

@login_required
def create_blog(request):
    if request.method=="POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)   
            blog.author = request.user      
            blog.save()                      
            messages.success(request,"Blog saved!")
            return redirect('index')

        else:

            messages.error(request,"Try Again!")

    else:
        form = BlogForm()
    return render(request,'homepage/create.html',{'form':form})


def dashboard(request):
    blogs = Blog.objects.filter(author=request.user).order_by('-created_at')
    return render(request,'homepage/dashboard.html',{"blogs":blogs})



def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'homepage/blog_details.html', {'blog': blog})



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




def test(request):
    print(request.session.items())
    print()
    print(request.COOKIES)
    return HttpResponse("Check terminal")
