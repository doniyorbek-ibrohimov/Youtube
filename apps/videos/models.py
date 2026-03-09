from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name
    

class Channel(models.Model):
    """
    Represents a video channel owned by a user.
    Stores metadata such as name, avatar, banner,
    subscriber count, and verification status.
    """
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='channel'
        ) # can be changes into ForeignKey for multi-owner channels in the future
    
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)

    avatar = models.ImageField(upload_to='channels/avatars/', blank=True, null=True)
    banner = models.ImageField(upload_to='channels/banners/', blank=True, null=True)

    subscribers_count = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('unlisted', 'Unlisted'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name='videos'
        )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='videos'
        )
    
    # Video content
    video_file = models.FileField(upload_to='videos/%Y/%m/%d/')
    thumbnail = models.ImageField(upload_to='thumbnails/%Y/%m/%d/', blank=True, null=True)
    duration = models.IntegerField(help_text='Duration in seconds', default=0)
    
    # Metadata
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['creator']),
            models.Index(fields=['visibility']),
        ]

    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='comments'
        )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
        )
    text = models.TextField()
    likes = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.video.title}'


class VideoReaction(models.Model):
    LIKE_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]
    
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='reactions'
        )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='video_reactions'
        )
    like_type = models.CharField(max_length=10, choices=LIKE_CHOICES)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('video', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} {self.like_type} {self.video.title}'


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'
        )
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name='subscribers'
        )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'channel')

    def __str__(self):
        return f'{self.subscriber.username} subscribed to {self.channel.username}'
    
    # Custom validation to prevent self-subscription
    def clean(self):
        if self.subscriber == self.channel.owner:
            raise ValidationError("Users cannot subscribe to themselves.")

