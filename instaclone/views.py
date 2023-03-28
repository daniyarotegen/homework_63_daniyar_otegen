from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, RedirectView, TemplateView
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from .models import Post, CustomUser, Like, Comment


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
        followed_users = self.request.user.following.all()
        return Post.objects.filter(
            Q(user=self.request.user) | Q(user__in=followed_users)
        ).order_by('-created_at')



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = kwargs.get('user_id', self.request.user.id)
        profile_user = get_object_or_404(CustomUser, pk=user_id)
        posts = Post.objects.filter(user=profile_user).order_by('-created_at')

        is_own_profile = self.request.user == profile_user
        is_following = self.request.user.following.filter(pk=profile_user.pk).exists()
        posts_count = profile_user.post_set.count()
        followers_count = profile_user.followers.count()
        following_count = profile_user.following.count()

        context.update({
            'profile_user': profile_user,
            'posts': posts,
            'is_own_profile': is_own_profile,
            'is_following': is_following,
            'posts_count': posts_count,
            'followers_count': followers_count,
            'following_count': following_count,
        })

        return context


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


class FollowUserView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user_to_follow = CustomUser.objects.get(pk=self.kwargs['pk'])
        self.request.user.following.add(user_to_follow)
        self.request.user.followers_count += 1
        self.request.user.save()
        user_to_follow.followers_count += 1
        user_to_follow.save()
        messages.success(self.request, f'You are now following {user_to_follow.username}.')
        return reverse('profile', kwargs={'user_id': self.kwargs['pk']})


class UnfollowUserView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user_to_unfollow = CustomUser.objects.get(pk=self.kwargs['pk'])
        self.request.user.following.remove(user_to_unfollow)
        self.request.user.followers_count -= 1
        self.request.user.save()
        user_to_unfollow.followers_count -= 1
        user_to_unfollow.save()
        messages.success(self.request, f'You have unfollowed {user_to_unfollow.username}.')
        return reverse('profile', kwargs={'user_id': self.kwargs['pk']})


class LikePostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()
            post.likes_count -= 1
        else:
            post.likes_count += 1
        post.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        form.instance.post = post
        post.comments_count += 1
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')


class FollowersListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'followers_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        profile_user = get_object_or_404(CustomUser, pk=user_id)
        return profile_user.followers.all()


class FollowingListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'following_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        profile_user = get_object_or_404(CustomUser, pk=user_id)
        return profile_user.following.all()
