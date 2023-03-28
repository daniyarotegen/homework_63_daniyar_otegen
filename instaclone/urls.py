from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import RegisterView, UserLoginView, PostCreateView, ProfileView, UserSearchView, FollowUserView, \
    UnfollowUserView, LikePostView, CommentCreateView, FollowersListView, FollowingListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('profile/', ProfileView.as_view(), name='own_profile'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('search/', UserSearchView.as_view(), name='user_search'),
    path('follow/<int:pk>/', FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<int:pk>/', UnfollowUserView.as_view(), name='unfollow_user'),
    path('like/<int:pk>/', LikePostView.as_view(), name='like_post'),
    path('comment/<int:pk>/', CommentCreateView.as_view(), name='comment_create'),
    path('profile/<int:user_id>/followers/', FollowersListView.as_view(), name='followers_list'),
    path('profile/<int:user_id>/following/', FollowingListView.as_view(), name='following_list'),

]