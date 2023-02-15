from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm, PostVehicleForm, VehicleForm
from .forms import SparePartForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )


def delete_post(request, post_id=None):
    post_to_delete = Post.objects.get(id=post_id)
    post_to_delete.delete()
    return HttpResponseRedirect(reverse('home'))


class PostVehicle(View):

    def get(self, request, slug="big-car/", *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, pk=1)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "templates/post_vehicle.html",
            {
                "post": post,
                "comment_form": comment_form,
            },
        )

    def post(self, request, slug="big-car/", *args, **kwargs):
        """
        Users can post their vehicle
        """
        post = get_object_or_404(Post, pk=1)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return render(
            request,
            "templates/post_vehicle.html",
            {
                "post": post,
                "comment_form": comment_form,
            },
        )


class PostLike(View):

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def post_vehicle_view(request):
    if request.method == 'POST':
        form = PostVehicleForm(request.POST)
        if form.is_valid():
            # do something with the form data
            return render(request, 'index.html')
    else:
        form = PostVehicleForm()
    return render(request, 'PostVehicleForm.html', {'form': form})


def post_vehicle(request):
    if request.method == 'POST':
        form = PostVehicleForm(request.POST)
        if form.is_valid():
            # do something with the form data
            return render(request, 'index.html')
    else:
        form = PostVehicleForm()
    return render(request, 'post_vehicle.html', {'form': form})


@login_required
def addVehicle(request):

    if request.method == 'POST':

        form = VehicleForm(request.POST)

        if form.is_valid():
            vehicle = form.save(commit=False)

            vehicle.save()
            messages.success(request, 'Your vehicle post was created successfully!')  # noqa
            return render(request, '')
            return redirect(vehicle.get_update_url())
    else:
        form = VehicleForm()

    return render(request, 'PostVehicleForm.html', {'form': form})

    messages.error(request, 'At the end!')
