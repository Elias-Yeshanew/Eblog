# blog/forms.py

from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Comment, Category, CommentReply


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        
class PostForm(forms.ModelForm):
    authors = [(1, 'Author 1'), (2, 'Author 2'), (3, 'Author 3')]  # Replace with your actual author data

    # Create a ChoiceField for the author selection
    author = forms.ChoiceField(choices=authors, required=True)

    class Meta:
        model = Post
        fields = ['title', 'content', 'categories']  # Add fields as needed
    
    # categories = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter categories, separated by commas'}))
    # tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter tags, separated by commas'}))

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     categories_input = self.cleaned_data['categories']
    #     tags_input = self.cleaned_data['tags']

    #     if categories_input:
    #         instance.categories.set([category.strip() for category in categories_input.split(',')])
    #     else:
    #         instance.categories.clear()

    #     if tags_input:
    #         instance.tags.set([tag.strip() for tag in tags_input.split(',')])
    #     else:
    #         instance.tags.clear()

    #     if commit:
    #         instance.save()

    #     return instance

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'parent_comment']

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your comment here'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

# class TagForm(forms.ModelForm):
#     class Meta:
#         model = Tag
#         fields = ['name']


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = CommentReply
        fields = ['text', 'parent_comment']  