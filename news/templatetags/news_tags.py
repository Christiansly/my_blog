from django import template
from ..models import Post
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.inclusion_tag('news/posts/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

