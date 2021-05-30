from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Article
from django.contrib import messages
from .forms import CommentForm
import random


# Create your views here.





def search(request):
    if request.method == "GET":
        searched = request.GET.get['search_value']
        post_title = Article.objects.all().filter(title=searched)
        return render(request, 'search_page.html', {'post_title': post_title})
    else:
        return render(request, 'search_page.html')




def articledetailview(request,slug):
    model = Article
    template_name = 'detail.html'
    post = get_object_or_404(Article, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    comment_form = CommentForm()
    num = random.randrange(1111, 9999)
    global str_num
    str_num = str(num)
    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form,
                                           'cap': str_num})


def post_detail(request, slug):

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
            else:
                messages.info(request, 'Incorrect Captcha!')
                return render(request, template_name, {'post': post,
                                                       'comments': comments,
                                                       'new_comment': new_comment,
                                                       'comment_form': comment_form,
                                                       'cap': str_num})

    else:
        comment_form = CommentForm()

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


class AddPostView(CreateView):
    model = Article
    template_name = 'add.html'
    fields = '__all__'
