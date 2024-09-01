from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required
from . import forms
#from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.http import JsonResponse


# Create your views here.

from .forms import LikeForm



@login_required(login_url='/users/login/')
def like_post(request):
    if request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data['post_id']
            post = get_object_or_404(Post, id=post_id)
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
                liked = False
            else:
                post.likes.add(request.user)
                liked = True
            total_likes = post.likes.count()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'liked': liked, 'total_likes': total_likes})
            else:
                return redirect('posts:like_post')
    else:
        return redirect('posts:list')


@login_required(login_url='/users/login/')
def posts_list(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'posts/posts_list.html', {'posts':posts})




@login_required(login_url='/users/login/')
def post_page(request, slug):
    # post = Post.objects.get(slug=slug)
    # return render(request, 'posts/post_page.html', {'post':post})

    posts = Post.objects.filter(slug=slug)
    if posts.count() == 1:
        post = posts.first()
    elif posts.count() > 1:
        # Handle the case where multiple posts are found
        post = posts.first()  # or handle in a way that suits your needs
    else:
        # Handle the case where no post is found
        post = get_object_or_404(Post, slug=slug)


    context = {
        'post': post,
    }
    return render(request, 'posts/post_page.html', context)



# @login_required
# def like_post(request, post_id):
#     if request.method == 'POST':
#         post = get_object_or_404(Post, id=post_id)
#         if request.user in post.likes.all():
#             post.likes.remove(request.user)
#             liked = False
#         else:
#             post.likes.add(request.user)
#             liked = True
        
#         # Make sure total_likes is updated
#         total_likes = post.likes.count()

#         return JsonResponse({'liked': liked, 'total_likes': total_likes})




@login_required(login_url='/users/login/')
def post_new(request):
    if request.method == 'POST':
        form = forms.CreatePost(request.POST, request.FILES)
        if form.is_valid():
            newposts = form.save(commit=False)
            newposts.author = request.user
            newposts.save()
            return redirect('posts:list')

    else:
        form = forms.CreatePost()
    return render(request, 'posts/post_new.html', {'form':form})



@login_required(login_url='/users/login/')
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = forms.CreatePost(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post edited successful.")
            return redirect('posts:page', slug=post.slug)
    else:
        form = forms.CreatePost(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})




@login_required(login_url='/users/login/')
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('posts:list')
    return render(request, 'posts/delete_post.html', {'post': post})