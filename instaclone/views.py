from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from .models import Post, CustomUser


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'register.html'

    def form_valid(self, form):
        messages.success(self.request, 'Registration successful.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Registration failed. Please check the entered information.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('login')


class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['image', 'description']
    template_name = 'post_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('home')


class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-created_at')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, pk=user_id)
        posts = Post.objects.filter(user=user).order_by('-created_at')
        context = {
            'profile_user': user,
            'posts': posts,
        }
        return render(request, 'profile.html', context)



class UserSearchView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'user_search.html'
    context_object_name = 'users'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return CustomUser.objects.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(name__icontains=query)
            )
        return CustomUser.objects.none()
