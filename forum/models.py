from django.db import models
from django.contrib.auth.models import User


class ForumPost(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField("date and time sent")
    content = models.TextField("Forum post content")
    title = models.CharField(max_length=100, blank=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f"Forum post by {self.sender.__getattribute__("username")} sent at {self.timestamp}"
    
    def get_timestamp(self):
        return self.timestamp.timestamp() * 1000
    
    def get_sender_name(self):
        return self.sender.username
    
    def get_title(self):
        if not self.title:
            if len(self.content) > 100:
                return f"{self.content[:100]}..."
            return self.content
        return self.title
    
    def edit_post(self, new_content, new_title):
        self.content = new_content
        self.title = new_title
        self.edited = True

    class Meta:
        ordering = ["-timestamp"]


class ForumReply(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(ForumPost, on_delete=models.CASCADE)
    timestamp = models.DateTimeField("date and time sent")
    content = models.TextField("Reply content")

    def __str__(self):
        return f"Reply for post id {self.parent.__getattribute__("pk")} by {self.sender.__getattribute__("username")} sent at {self.timestamp}"
    
    def get_timestamp(self):
        return self.timestamp.timestamp() * 1000
    
    def get_sender_name(self):
        return self.sender.username

    class Meta:
        ordering = ["timestamp"]
