from django.db import models
from django.utils.text import slugify
from django.conf import settings


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(blank=True,upload_to='blog_images')
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:               
            base_slug = slugify(self.title)
            slug = base_slug
            count = 1
            while Blog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    
class Comments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
      

class Reaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    reaction = models.CharField(max_length=20,
                                choices=[("Like","like"),
                                         ("Dislike","dislike")])
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "blog"],
                name="unique_user_blog_reaction"
            )
        ]
    
    
    
class Save(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "blog"],
                name="unique_user_blog_save"
            )
        ]
        

class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="following")
    following = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="follower")
    created_at = models.DateField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["following", "follower"],
                name="unique_user_follow"
            )
        ]