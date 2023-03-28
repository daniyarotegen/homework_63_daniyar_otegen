from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import RegisterView, UserLoginView, PostCreateView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('profile/', ProfileView.as_view(), name='profile'),
]