# Create your models here.
from django.utils.text import slugify
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("email_verified", True)

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("USER", "Normal User"),
        ("BLOGGER", "Blogger"),
    )

    followers = models.ManyToManyField('self',symmetrical=False,related_name="following",blank=True)



    id = models.BigAutoField(primary_key=True)

    # Authentication
    objects = UserManager()

    username = models.CharField(max_length=150, unique=True)#
    email = models.EmailField(unique=True)#
    password_updated_at = models.DateTimeField(null=True, blank=True)#

    # Role & Status
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="USER")
    
    is_staff = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    # Profile
    full_name = models.CharField(max_length=255, blank=True) #
    bio = models.TextField(blank=True) ##
    profile_image = models.ImageField(upload_to="profiles/", null=True, blank=True)
    website = models.URLField(blank=True) ##
    instagram_link = models.URLField( blank=True)##
    x_link = models.URLField( blank=True)##
    git_link = models.URLField( blank=True)##
    

    # Blogging Metrics
    total_posts = models.PositiveIntegerField(default=0)
    total_views = models.PositiveBigIntegerField(default=0)
    total_likes = models.PositiveBigIntegerField(default=0)
    is_approved_blogger = models.BooleanField(default=False)

    # System Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active_at = models.DateTimeField(null=True, blank=True)
    timezone = models.CharField(max_length=50, default="UTC")
    language_preference = models.CharField(max_length=10, default="en")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
# ---------------------------- BLOG DATA MODEL ------------------------------


author = models.ForeignKey(
    "User",
    on_delete=models.CASCADE,
    related_name="blogs"
)


class Blog(models.Model):

    STATUS_CHOICES = (
        ("DRAFT", "Draft"),
        ("PUBLISHED", "Published"),

    )
    COLOR_CHOICES = (
    ("BLACK", "Black"),
    ("WHITE", "White"),
    ("NONE", "None"),
)


    id = models.BigAutoField(primary_key=True)

    # Author
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blogs"
    )

    # Content
    title = models.CharField(max_length=255)
    title_bg_color = models.CharField(max_length=10,choices=COLOR_CHOICES,default="NONE")

    slug = models.SlugField(max_length=300, unique=True)
    short_description = models.TextField(blank=True)
    content = models.TextField()  # CKEditor HTML stored here
    cover_image = models.ImageField(upload_to="blogs/covers/", null=True, blank=True)

    # Classification & Search
    keywords = models.ManyToManyField(
        "BlogKeyword",
        blank=True,
        related_name="blogs"
    )

    category = models.CharField(max_length=100, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_blogs', blank=True)
    nation = models.CharField(max_length=100, blank=True)  # optional geo targeting

    # Status & Visibility
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="DRAFT"
    )

    is_comments_enabled = models.BooleanField(default=True)

    # Metrics (denormalized for performance)
    views = models.IntegerField(default=0)
    total_views = models.PositiveBigIntegerField(default=0)
    total_likes = models.PositiveBigIntegerField(default=0)
    total_comments = models.PositiveBigIntegerField(default=0)
    total_bookmarks = models.PositiveBigIntegerField(default=0)

    # Timestamps
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["status"]),
            models.Index(fields=["published_at"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        original_slug = self.slug
        queryset = Blog.objects.all()
        if self.pk:
            queryset = queryset.exclude(pk=self.pk)

        # If the slug exists, append a unique suffix
        while queryset.filter(slug=self.slug).exists():
            self.slug = f'{original_slug}-{str(uuid.uuid4())[:4]}'
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.author}"


class BlogKeyword(models.Model):

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)    

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.blog.title}"

# ================================ Bookmark =======================================
class Bookmark(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookmarks"
    )
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name="bookmarked_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "blog")

    def __str__(self):
        return f"{self.user.username} bookmarked {self.blog.title}"

class BlogView(models.Model):
    """
    Tracks individual blog views strictly for traffic time and new/returning reader analytics.
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="view_events")
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['blog', 'session_key']),
            models.Index(fields=['created_at']),
        ]
        
    def __str__(self):
        return f"View for {self.blog.title} at {self.created_at}"
