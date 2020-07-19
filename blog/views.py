from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Post, Comment, Category
from .forms import NewCommentForm
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):

    all_posts = Post.newmanager.all()

    return render(request, 'index.html', {'posts': all_posts})


def post_single(request, post):

    post = get_object_or_404(Post, slug=post, status='published')

    allcomments = post.comments.filter(status=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(allcomments, 10)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    user_comment = None

    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.save()
            return HttpResponseRedirect('/' + post.slug)
    else:
        comment_form = NewCommentForm()
    return render(request, 'single.html', {'post': post, 'comments':  user_comment, 'comments': comments, 'comment_form': comment_form, 'allcomments': allcomments, })


class CatListView(ListView):
    template_name = 'category.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        content = {
            'cat': self.kwargs['category'],
            'posts': Post.objects.filter(category__name=self.kwargs['category']).filter(status='published')
        }
        return content


def category_list(request):
    category_list = Category.objects.exclude(name='default')
    context = {
        "category_list": category_list,
    }
    return context
