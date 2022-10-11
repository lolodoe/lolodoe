from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from posts.forms import PostForm, Commentform
from posts.models import Post, Comment
from posts.constants import PAGINATION__LIMIT
from django.views import View
from django.views.generic import ListView, CreateView, DetailView


def get_user_from_request(request):
    return request.user if not request.user.is_anonymous else None


class MainView(ListView):
    queryset = Post.objects.all()
    template_name = 'posts.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
                # 'posts':self.queryset,
                # 'user': get_user_from_request(self.request),
                # 'pages': kwargs['page']
            }

    def get(self,request, **kwargs):
        page = int(request.GET.get('page', 1))

        start_post = PAGINATION__LIMIT * page if page != 1 else 0
        end_post = start_post + PAGINATION__LIMIT

        max_page = len(self.queryset) / PAGINATION__LIMIT
        if max_page < round(max_page): max_page = round(max_page)
        else:
            max_page = round(max_page)
        # if max_page > round(max_page):
        #     max_page = round(max_page) + 1
        # else:
        #     max_page = round(max_page)


        context = {
            'posts': self.queryset[start_post:end_post],
            'user': get_user_from_request(self.request),
            'pages': range(1, max_page)

        }

        return render(request, self.template_name, context=context)


        # def get(self,request, **kwargs):
        #         page = int(request.GET.get('page', 1))
        #
        #         start_posts = (len(self.queryset) // ((len(self.queryset) // PAGINATION__LIMIT) + 1)) * page -1 if page > 1 else 0
        #         # start_posts = (len(posts)) // PAGINATION__LIMIT * page - 1 if page > 1 else 0
        #         end_posts = start_posts + PAGINATION__LIMIT
        #         print(start_posts, end_posts)
        #
        #         data = {
        #             'posts': self.queryset[start_posts:end_posts],
        #             'user': get_user_from_request(request),
        #             'pages': range(1, (len(self.queryset) // PAGINATION__LIMIT) + 2)
        #         }
        #
        #         return render(request, self.template_name, context=data)


class PostDetailView(DetailView):
    queryset = Post.objects.all()
    template_name = 'detail.html'
    context_object_name = 'post'
    #     post = Post.objects.get(id=id)
    #     comments = Comment.objects.filter(post=post)
    #
    #     data = {
    #         'user': get_user_from_request(request),
    #         'comment_form': Commentform,
    #         'post': post,
    #         'comments': comments
    #     }
    #     return render(request, 'detail.html', context=data)
    # elif request.method == 'POST':
    #     form = Commentform(request.POST)
    #     if form.is_valid():
    #         Comment.objects.create(
    #             author=form.cleaned_data.get('author'),
    #             text=form.cleaned_data.get('text'),
    #             post_id=id
    #         )
    #         return redirect(f"/posts/{id}/")
    #     else:
    #         post = Post.objects.get(id=id)
    #         comments = Comment.objects.filter(post=post)
    #         return render(request, 'detail.html', context={
    #             'post': post,
    #             'comments': comments,
    #             'post_form': form,
    #             'id': id
    #         })


class CreatePostView(ListView,CreateView):
    model = Post
    template_name = 'create_post.html'
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={
            'post_form': self.form_class
        })

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
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


class EditPostView(ListView, CreateView):
    template_name = 'edit.html'
    queryset = Post.objects.all()
    form_class = PostForm

    def get(self, request, pk, *args):
        return render(request, self.template_name, context={
            'post_form': self.form_class,
            'pk': pk
        })

    def post(self, request, pk, **kwargs):
        form = self.form_class(request.POST)
        instance = get_object_or_404(Post, pk=pk)
        if form.is_valid():
            instance.title = form.cleaned_data.get('title')
            instance.description = form.cleaned_data.get('description')
            instance.stars = form.cleaned_data.get('stars')
            instance.type = form.cleaned_data.get('type')
            instance.save()
            return redirect('/')
        else:
            return render(request, self.template_name, context={
                'post_form': self.form_class,
                'pk': pk
            })


    # if request.method == 'GET':
    #     return render(request, 'edit.html', context={
    #         'post_form': PostForm,
    #         'id': id
    #     })
    # if request.method == "POST":
    #     form = PostForm(request.POST)
    #     if form.is_valid():
    #         post = Post.objects.get(id=id)
    #         post.title=form.cleaned_data.get('title')
    #         post.description=form.cleaned_data.get('description')
    #         post.stars=form.cleaned_data.get('stars')
    #         post.type=form.cleaned_data.get('type')
    #         post.save()
    #         return redirect('/')
    #     else:
    #         return render(request, 'edit.html', context={
    #             'post_form': form,
    #             'id': id
    #         })
