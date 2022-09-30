from django.http import HttpResponse
from django.shortcuts import render, redirect

from posts.forms import PostForm, Commentform
from posts.models import Post, Comment


def main(request):
    if request.method == 'GET':
        posts = Post.objects.all()

        data = {
            'posts': posts
        }

        return render(request, 'posts.html', context=data)


def post_detail(request, id):
    if request.method == 'GET':
        post = Post.objects.get(id=id)
        comments = Comment.objects.filter(post=post)

        data = {
            'comment_form': Commentform,
            'post': post,
            'comments': comments
        }
        return render(request, 'detail.html', context=data)
    elif request.method == 'POST':
        form = Commentform(request.POST)
        if form.is_valid():
            Comment.objects.create(
                author=form.cleaned_data.get('author'),
                text=form.cleaned_data.get('text'),
                post_id=id
            )
            return redirect(f"/posts/{id}/")
        else:
            post = Post.objects.get(id=id)
            comments = Comment.objects.filter(post=post)
            return render(request, 'detail.html', context={
                'post': post,
                'comments': comments,
                'post_form': form,
                'id': id
            })





def create_post(request):
    if request.method == 'GET':
        return render(request, 'create_post.html', context={
            'post_form': PostForm
        })

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            Post.objects.create(
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                stars=form.cleaned_data.get('stars'),
                type=form.cleaned_data.get('type')
            )
            return redirect('/')
        else:
            return render(request, 'create_post.html', context={
                'post_form': form
            })


def creat_comment(request):
    if request.method == 'GET':
        return render(request, 'create_comment.html', context={
            'coment_form': Commentform
        })

    if request.method == "POST":
        form = Commentform(request.POST)
        if form.is_valid():
            Post.objects.create(
                author=form.cleaned_data.get('author'),
                desciption=form.cleaned_data.get('description'),
            )
            return redirect('/')
        else:
            return render(request, 'create_post.html', context={
                'post_form': form
            })


