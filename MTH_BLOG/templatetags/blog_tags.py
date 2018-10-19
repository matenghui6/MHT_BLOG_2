from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
from taggit.managers import TaggableManager
import markdown

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('MTH_BLOG/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.inclusion_tag('MTH_BLOG/post/most_comments.html')
def get_most_commented_posts_two(count=5):
    most_comments = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    return {'most_comments': most_comments}



@register.inclusion_tag('MTH_BLOG/post/tag.html')
def get_all_tags():
    all_tags = Post.tags.all()
    return {'all_tags': all_tags}




@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
