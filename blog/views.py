from django.shortcuts import render, get_object_or_404
from django.core.files import File
from .models import Post
from django.utils import timezone
from .forms import PostForm
from django.shortcuts import redirect
import re
import io
import os


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "published_date"
    )
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=int(pk))
    return render(request, "blog/post_detail.html", {"post": post},)


def akema_temp(request):

    with open(
        "/home/Onurbi12/onurbi12.pythonanywhere.com/blog/templates/blog/test.html",
        "r",
    ) as html_t:
        html_test = File(html_t)
        html_string = html_test.read()

    new_string = re.sub(
        r"(<a.*?</a>)",
        r'<span class="url" style="background-color: red;">\1</span>',
        html_string,
        flags=re.MULTILINE | re.DOTALL,
    )

    with open(
        "/home/Onurbi12/onurbi12.pythonanywhere.com/blog/templates/blog/test2.html",
        "w",
    ) as html_t:
        html_test = File(html_t)
        html_test.write(new_string)

    return render(request, "blog/test2.html")


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()
    return render(request, "blog/post_edit.html", {"form": form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=int(pk))
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_edit.html", {"form": form})
