from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import (CreateView, UpdateView, DeleteView,)
from django.db.models import Count
from django.shortcuts import render
from .forms import PostForm, RegisterForm
from .models import Post, Category
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404



class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.annotate(post_count=Count("posts"))
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"slug": self.object.slug})


class MyPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/my_posts.html"
    paginate_by = 6
    login_url = "login"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by("-created_at")

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "blog/register.html"
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"slug": self.object.slug})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    login_url = "login"
    success_url = reverse_lazy("home")

    def test_func(self):
        return self.get_object().author == self.request.user

class CategoryPostsView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    paginate_by = 6

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return Post.objects.filter(
            category=self.category, status="published"
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.annotate(post_count=Count("posts"))
        return context


def about(request):
    return render(request, "blog/about.html", {"team": "DjangoBlog Team"})


def contact(request):
    return render(request, "blog/contact.html")