from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect

def post_list(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()  

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    context = {'form':form, "posts":posts}
    return render(request, 'hellomin/post_list.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'hellomin/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'hellomin/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'hellomin/post_edit.html', {'form': form})

def post_remove(request, pk):
    context ={}
    if request.method =="POST":
        current_password = request.POST.get("checkpassword")
        post = get_object_or_404(Post, pk=pk)
        if current_password == post.password:
            post.delete()
            return redirect('post_list')
        else:
            return redirect('post_list')

    return render(request, 'hellomin/post_remove.html', context)