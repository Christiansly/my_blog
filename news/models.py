from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager
from django.urls import reverse
# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status = 'publish')

class Post(models.Model):
    STATUS = (
        ('draft', 'Draft'),
        ('publish', 'Publish'),
    )

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=400, unique_for_date='publish')
    body = models.TextField()
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add= True)
    status = models.CharField(max_length=10, choices=STATUS, default='draft')
    publish = models.DateTimeField(default=timezone.now)
    tags = TaggableManager()
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #pylint: disable=E1101
        return reverse('news:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        
    def __str__(self):
        return self.name