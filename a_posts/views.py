from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from bs4 import BeautifulSoup
import requests
from django.contrib import messages 


def home_view(request, tag=None):
    title = 'Test Blog Comments'
    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:
        posts = Post.objects.all()
    
    # for i in posts:
    #     if i.image :
    #         print("_____________", i.image)
    #     else: 
    #         print('ssssssssssss', i.photo_field)

    categories = Tag.objects.all()
    
    context = {
        'posts' : posts,
        'categories': categories,
        'title': title,
        'tag': tag,
    }
    
    return render(request, 'a_posts/home.html', context)



@login_required
def post_create_view(request):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            
            # website = requests.get(form.data['body'])
            # print(website.text)
            # sourcecode = BeautifulSoup(website.text, 'html.parser')
            
            # find_image = sourcecode.select('meta[content^="https://live.staticflickr.com/"]')
            
            # image = find_image[0]['content']
            # post.image = image 
            
            # find_title = sourcecode.select('h1.photo-title')
            # title = find_title[0].text.strip()
            # post.title = title
            
            # find_artist = sourcecode.select('a.owner-name')
            # artist = find_artist[0].text.strip()
            # post.artist = artist
            # title = form.cleaned_data['h1.photo-title']
            # post.title = 
            print(form)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('home')
        
    return render(request, 'a_posts/post_create.html', {'form': form})
@login_required
def post_delete_view(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted')
        return redirect('home')
    return render(request, 'a_posts/post_delete.html', {'post': post})

@login_required
def post_edit_view(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    form = PostEditForm(instance=post)
    
    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid:
            form.save()
            messages.success(request, 'Post updated')
            return redirect('home')
    
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'a_posts/post_edit.html', context)

def post_page_view(request, pk):

    post = get_object_or_404(Post, id=pk)
    
    commentform = CommentCreateForm()
    replyform = ReplyCreateForm()
    context = {
        'post': post,
        'commentform': commentform,
        'replyform': replyform
    }
    
    return render(request, 'a_posts/post_page.html', context)

@login_required
def comment_sent(request, pk):
    post = get_object_or_404(Post, id=pk)
    replyform = ReplyCreateForm()
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
            
    context = {
        'post': post,
        'comment': comment,
        'replyform': replyform,
    }          
    return render(request, 'snippets/add_comment.html', context)

@login_required
def reply_sent(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    replyform = ReplyCreateForm()
    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid:
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment

            reply.save()
    context = {
        'reply': reply,
        'comment': comment,
        'replyform': replyform,
    }    
    return render(request, 'snippets/add_reply.html', context)


@login_required
def reply_form(request, pk):
    reply = get_object_or_404(Reply, id=pk)
    replyform = NestedReplyCreateForm()
    
    if request.method == 'POST':
        form = NestedReplyCreateForm(request.POST)
        if form.is_valid:
            reply_nested = form.save(commit=False)
            reply_nested.author = request.user
            reply_nested.parent_reply = reply
            reply_nested.level = reply.level + 1
            reply_nested.save()
            return render(request, 'a_posts/reply.html', {'reply': reply_nested})
    
    context = {
        'reply': reply,
        'replyform': replyform
    }
    return render(request, 'snippets/add_replyform.html', context)



# @login_required
# def reply_reply_sent(request, pk):
    
#     reply = get_object_or_404(Reply, id=pk)
#     if request.method == 'POST':
#         form = ReplyCreateForm(request.POST)
#         if form.is_valid:
#             reply = form.save(commit=False)
#             reply.author = request.user
            
#             reply.parent_reply = reply
#             reply.save()
            
#     return redirect('post', reply.parent_post.id)

@login_required
def comment_delete_view(request, pk):
    post = get_object_or_404(Comment, id=pk, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Comment deleted')
        return redirect('post', post.parent_post.id)
    return render(request, 'a_posts/comment_delete.html', {'comment': post})



@login_required
def reply_delete_view(request, pk):
    reply = get_object_or_404(Reply, id=pk, author=request.user)
    reply.delete()
    return HttpResponse('')
    
    


def like_toggle(model):
    def inner_func(func):
        def wrapper(request, *args, **kwargs):
            post = get_object_or_404(model, id=kwargs.get('pk'))
            user_exist = post.likes.filter(username=request.user.username).exists()
            
            if post.author != request.user:
                if user_exist:
                    post.likes.remove(request.user)
                else:
                    post.likes.add(request.user)
                    
            return func(request, post)
        return wrapper
    return inner_func

@login_required
@like_toggle(Post)
def like_post(request, post):
    return render(request, 'snippets/likes.html', {'post': post})

@login_required
@like_toggle(Comment)
def like_comment(request, post):
    return render(request, 'snippets/likes_comment.html', {'comment': post})


@login_required
@like_toggle(Reply)
def like_reply(request, post):
    return render(request, 'snippets/likes_reply.html', {'reply': post})