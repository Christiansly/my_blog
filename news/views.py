from django.shortcuts import render, get_object_or_404
from .models import Comment, Post
from .forms import CommentForm
# Create your views here.
def post_list(request):
    query = None
    posts = None
    if 'query' in request.GET:
        query = request.GET['query']
        posts = Post.published.filter(title__icontains = query).order_by('-publish')
    else:
        posts = Post.published.order_by('-publish')
    return render(request, 'news/posts/post_list.html', {'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status = 'publish', publish__year = year, publish__month = month, publish__day = day, slug = post)
    comments = post.comments.filter(active = True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'news/posts/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form, 'new_comment': new_comment})