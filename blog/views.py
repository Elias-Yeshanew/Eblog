import json
from django.shortcuts import render, get_object_or_404,redirect
from .models import Post, Category,Comment
from .forms import PostForm
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CommentForm
from rest_framework import generics, status
from .serializers import PostSerializer, CommentSerializer,CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response




def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = Comment.objects.filter(post=post)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            if comment_form.cleaned_data['parent_comment']:
                parent_comment = Comment.objects.get(pk=comment_form.cleaned_data['parent_comment'])
                comment.parent_comment = parent_comment
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comment, 'comment_form': comment_form})

def category_list(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    posts = Post.objects.filter(categories=category)
    return render(request, 'blog/category_list.html', {'category': category, 'posts': posts})

# def tag_list(request, tag_id):
#     tag = get_object_or_404(Tag, pk=tag_id)
#     posts = Post.objects.filter(tags=tag)
#     return render(request, 'blog/tag_list.html', {'tag': tag, 'posts': posts})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save()
            categories = Category.objects.all()
            # tags = Tag.objects.all()
            context = {
                'categories': categories,
                # 'tags': tags,
            }
            return redirect('post_detail', post_id=new_post.id)  # Redirect to the newly created post detail page
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'  # Create this template
    success_url = reverse_lazy('home')  # Redirect to the post list after deletion


class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        # Process categories and tags as comma-separated values
        categories = self.request.POST.get('categories', '').split(',')
        # tags = self.request.POST.get('tags', '').split(',')
        
        form.instance.save()
        form.instance.categories.set(Category.objects.filter(name__in=categories))
        # form.instance.tags.set(Tag.objects.filter(name__in=tags))
        return super().form_valid(form)

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm

    # Update the success_url attribute to use post_id
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'post_id': self.object.id})


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    fields = ['title', 'content']
    
    # Update the success_url attribute to use post_id
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'post_id': self.object.id})
    
    def form_valid(self, form):
        # Get selected categories and tags from the form
        categories = self.request.POST.getlist('categories')
        # tags = self.request.POST.getlist('tags')
        
        # Clear existing categories and tags, and associate new ones with the post
        self.object.categories.clear()
        # self.object.tags.clear()
        self.object.categories.add(*categories)
        # self.object.tags.add(*tags)
        
        return super().form_valid(form)
    

def category_list(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    posts = Post.objects.filter(category=category)
    context = {
        'category': category,
        'posts': posts
    }
    return render(request, 'blog/category_list.html', context)

# def tag_list(request, tag_id):
#     tag = get_object_or_404(Tag, pk=tag_id)
#     posts = Post.objects.filter(tags=tag)
#     return render(request, 'blog/tag_list.html', {'tag': tag, 'posts': posts})

# def tag_list(request, tag_id):
#     tag = get_object_or_404(Tag, pk=tag_id)
#     posts = Post.objects.filter(tags=tag)
#     context = {
#         'tag': tag,
#         'posts': posts
#     }
#     return render(request, 'blog/tag_list.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print("user created")
            return redirect('login')
        else:
            print('user not created')
        
    else:
        print('user not created')
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to a success page or wherever you want
            return redirect('home')  # Replace 'home' with your URL name
    else:
        # Render the login form
        form = AuthenticationForm()
    return render(request, 'blog/login.html')



from django.http import JsonResponse

def add_comment_to_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        if request.content_type == 'application/json':
            # Handle API request
            data = json.loads(request.body.decode('utf-8'))
            comment_form = CommentForm(data)
            
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return JsonResponse({'message': 'Comment added successfully'})
            else:
                return JsonResponse({'errors': comment_form.errors}, status=400)
        else:
            # Handle HTML form submission
            comment_form = CommentForm(request.POST)
            
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('post_detail', post_id=post.id)
            else:
                print(comment_form.errors)
    else:
        comment_form = CommentForm()
    
    return render(request, 'blog/add_comment_to_post.html', {'form': comment_form})


def reply_to_comment(request, parent_comment_id):
    parent_comment = get_object_or_404(Comment, pk=parent_comment_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = parent_comment.post
            comment.author = request.user
            comment.parent_comment = parent_comment  # Set the parent comment
            comment.save()
            return redirect('post_detail', post_id=parent_comment.post.id)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/reply_to_comment.html', {'parent_comment': parent_comment, 'comment_form': comment_form})



class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostCommentsAPIView(APIView):
    def get(self, request, pk):
        try:
            comments = Comment.objects.filter(post=pk)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
