from django.db import models
from django.conf import settings

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    caption = models.CharField(max_length=250,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.caption[:30]}"
    
    
#ONE POST CAN CONTAIN MANY PHOTOTS

class Media(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="media")
    file = models.FileField(upload_to="media/")
    
    
    def is_video(self):
        vdos = ['mp4','mov','avi','webm','mkv']
        file = self.file.name.lower() 
        extension = file.rsplit(".", 1)[-1]
        if extension in vdos:
            return True
        return False
    
    def __str__(self):
        return self.file.name
    
    
    