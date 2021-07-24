from django.shortcuts import render, redirect, get_object_or_404
from django.template import context
from django.views.generic import ListView
from .models import Article
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CommentForm, CreateBlogPostForm, UpdateBlogPostForm
import random
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


def like_post(request, pk, slug):
    post = get_object_or_404(Article, id=request.POST.get('post_id'))

    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('detail', args=[str(pk)], slug=slug))
    # return redirect('detail', post.pk)


class MyPosts(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'must_authenticate'
    model = Article
    queryset = Article.objects.filter(status=1).order_by('-created_on')
    template_name = 'my_posts.html'
    paginate_by = 10


def search(request):
    if request.method == "GET":
        searched = request.GET.get('search_value')
        print(searched)
        post_title = Article.objects.all().filter(title__contains=searched)
        print(post_title)
        return render(request, 'search_page.html', {'post_title': post_title, 'searched': searched})
    else:
        return render(request, 'search_page.html')


def create_blog_view(request):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    form = CreateBlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # author = request.user.username
        author = User.objects.filter(username=user.username).first()
        obj.author = author
        obj.save()
        messages.info(request,
                      'Congratulations! Your post has been submitted successfully. Admin will verify and approve your post.')
        form = CreateBlogPostForm()
    context['form'] = form
    return render(request, 'create_blog.html', context)


def update_blog_view(request, slug):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    blog_post = get_object_or_404(Article, slug=slug)
    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated!"
            blog_post = obj

    form = UpdateBlogPostForm(
        initial={'title': blog_post.title, 'body': blog_post.body, 'image': blog_post.image or None,
                 'slug': blog_post.slug})
    context['form'] = form
    return render(request, 'edit_blog.html', context)


def articledetailview(request, slug):
    if not request.user.is_authenticated:
        return redirect('must_authenticate')

    template_name = 'detail.html'
    post = get_object_or_404(Article, slug=slug)
    comments = post.comments.filter(active=True)
    total_like = post.total_likes()
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    new_comment = None
    comment_form = CommentForm()
    num = random.randrange(11111, 99999)
    global str_num
    str_num = str(num)
    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form,
                                           'cap': str_num,
                                           'total_like': total_like,
                                           'liked': liked})


def comment(request, slug):
    template_name = 'detail.html'
    post = get_object_or_404(Article, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        captcha = request.POST.get('cap')
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            if captcha == str_num:
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.save()
                return redirect('detail', slug=slug)
            else:
                messages.info(request, 'Incorrect Captcha!')
                return render(request, template_name, {'post': post,
                                                       'comments': comments,
                                                       'new_comment': new_comment,
                                                       'comment_form': comment_form,
                                                       'cap': str_num})

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form,
                                           'cap': str_num})


class ArticleListView(ListView):
    model = Article
    queryset = Article.objects.filter(status=1).order_by('-created_on')
    template_name = 'home.html'
    paginate_by = 3

    # def get_data(self):
    #     search_input = self.request.GET.get('search_value') or ''
    #     if search_input:
    #         context['object_list'] = context['object_list'].filter(title__icontains=search_input)
    #
    #     context['search_input'] = search_input
    #
    #     return context
