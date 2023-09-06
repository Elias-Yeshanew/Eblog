from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.post_list, name='home'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('category/<int:category_id>/', views.category_list, name='category_list'),    
    # path('tag/<int:tag_id>/', views.tag_list, name='tag_list'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    # path('post/list/', views.post_list, name='post_list'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('post/<int:post_id>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/reply/<int:parent_comment_id>/', views.reply_to_comment, name='reply_to_comment'),
    path('api/posts/', views.PostList.as_view(), name='post-list'),
    path('api/posts/<int:post_id>/', views.PostDetail.as_view(), name='post-detail'),
    path('api/posts/<int:post_id>/comments/', views.PostCommentsAPIView.as_view(), name='post-comments-api'),
]
