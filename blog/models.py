from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  
from django.conf import settings


# Define Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Define Tag Model
# class Tag(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# Define Comment Model
# class Comment(models.Model):
#     post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'Comment by {self.author} on {self.post.title}'

# Define Post Model
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, related_name='posts')
    # tags = models.ManyToManyField(Tag, related_name='posts')
    updated_date = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Update the updated_date field when saving
        self.updated_date = timezone.now()
        super().save(*args, **kwargs)

# class Post(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     author = models.ForeignKey(User, on_delete=models.CASCADE)  # If using Django's User model
#     publication_date = models.DateTimeField(auto_now_add=True)
#     # Add more fields as needed
    
#     def __str__(self):
#         return self.title  # Return a human-readable representation of the object

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    
class CommentReply(models.Model):
    id = models.AutoField(primary_key=True)  # Ensure an AutoField primary key
    text = models.TextField()
    parent_comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Other fields for your comment reply model

    def __str__(self):
        return self.text