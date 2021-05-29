from lib2to3.fixes.fix_input import context
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Article
from .forms import CommentForm


# Create your views here.


# class ArticleDetailView(DetailView):
#     model = Article
#     template_name = 'detail.html'


def search(request):
    if request.method == "POST":
        searched = request.POST['search_value']
        return render(request, 'events/search_page.html', {'search_value': searched})
    else:
        return render(request, 'events/search_page.html')


def post_detail(request, slug):
    template_name = 'detail.html'
    post = get_object_or_404(Article, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


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
