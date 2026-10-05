from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post, Category
from .forms import PostForm


def post_list(request):
    posts = Post.objects.filter(status="published").order_by("-created_at")
    paginator = Paginator(posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/post_list.html", {
        "page_obj": page_obj,
        "title": "Japan Travel and Culture Blog",
        "categories": Category.objects.all(),
    })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status="published")
    return render(request, "blog/post_detail.html", {"post": post})


def about(request):
    return render(request, "blog/about.html", {"title": "Me"})


def contact(request):
    return render(request, "blog/contact.html", {"title": "Contact"})


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"slug": self.object.slug})


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"slug": self.object.slug})


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("home")