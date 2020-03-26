from django.shortcuts import render, get_object_or_404 , redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
#from django.contrib.auth.models import User

import os,requests,uuid,json

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


def post_translate(request, pk):
    
    if request.method == "GET":
        post = get_object_or_404(Post, pk=pk)
        post_text = post.text

        subscription_key = '7f8c40bec39a43c7b3457caf089f8bd7'
        endpoint = 'https://api.cognitive.microsofttranslator.com'
        path = '/translate?api-version=3.0'
        params = '&to=it'
        constructed_url = endpoint + path + params

        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        # You can pass more than one object in body.
        body = [{
            'text' : post_text
        }]
        requestapi = requests.post(constructed_url, headers=headers, json=body)
        response = requestapi.json() 
        
        jsonString=(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))

        dict = json.loads(jsonString)
        translatetext=(dict[0]['translations'][0]['text'])
        context = {'text': translatetext}

    return render(request, 'hellomin/post_translate.html', context)






