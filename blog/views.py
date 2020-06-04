from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Post
from django.utils import timezone
from .forms import PostForm
from django.shortcuts import redirect
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.resources import CDN


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "published_date"
    )
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=int(pk))
    x = [1, 3, 5, 7, 9, 11, 13]
    y = [1, 2, 3, 4, 5, 6, 7]
    title = "y = f(x)"

    plot = figure(
        title=title,
        x_axis_label="X-Axis",
        y_axis_label="Y-Axis",
        plot_width=400,
        plot_height=400,
    )

    plot.line(x, y, legend="f(x)", line_width=2)
    # Store components
    script, div = components(plot)

    # Feed them to the Django template.
    return render(
        request,
        "blog/post_detail.html",
        {"post": post, "script": script, "div": div},
    )


def akema_temp(request):
    return render(request, "blog/test.html")


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


def index(request):
    x = [1, 3, 5, 7, 9, 11, 13]
    y = [1, 2, 3, 4, 5, 6, 7]
    title = "y = f(x)"

    plot = figure(
        title=title,
        x_axis_label="X-Axis",
        y_axis_label="Y-Axis",
        plot_width=400,
        plot_height=400,
    )

    plot.line(x, y, legend="f(x)", line_width=2)
    # Store components
    script, div = components(plot)

    # Feed them to the Django template.
    return render_to_response(
        "blog/bokeh_test.html", {"script": script, "div": div}
    )
