from django.urls import path

from blog.views import PostCreateView, PostListView, PostDetailView, PostDeleteView, PostUpdateView

app_name = 'blog'
# from blog.views import PostListView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
]

