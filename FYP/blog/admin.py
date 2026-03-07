from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Blog, BlogKeyword

User = get_user_model()

# ===========================
# USER ADMIN
# ===========================

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = (
        "email",
        "username",
        "role",
        "is_approved_blogger",
        "email_verified",
        "is_staff",
        "is_superuser",
        "created_at",
    )

    list_filter = (
        "role",
        "is_approved_blogger",
        "email_verified",
        "is_staff",
        "is_superuser",
        "created_at",
    )

    search_fields = (
        "email",
        "username",
        "full_name",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "last_login",
        "password_updated_at",
        "total_posts",
        "total_views",
        "total_likes",
        "followers",
    )

    fieldsets = (
        ("Authentication", {
            "fields": (
                "email",
                "username",
                "password",
            )
        }),
        ("Profile", {
            "fields": (
                "full_name",
                "bio",
                "profile_image",
            )
        }),
        ("Social Links", {
            "fields": (
                "website",
                "instagram_link",
                "x_link",
                "git_link",
            )
        }),
        ("Blogging & Metrics", {
            "fields": (
                "role",
                "is_approved_blogger",
                "total_posts",
                "total_views",
                "total_likes",
                "followers",
            )
        }),
        ("Permissions", {
            "fields": (
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("System", {
            "fields": (
                "email_verified",
                "timezone",
                "language_preference",
                "last_login",
                "last_active_at",
                "created_at",
                "updated_at",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "username",
                "password1",
                "password2",
                "role",
                "is_staff",
                "is_superuser",
            ),
        }),
    )

    filter_horizontal = ("groups", "user_permissions")

    actions = (
        "approve_blogger",
        "verify_email",
    )

    def approve_blogger(self, request, queryset):
        queryset.update(is_approved_blogger=True)

    approve_blogger.short_description = "Approve selected bloggers"

    def verify_email(self, request, queryset):
        queryset.update(email_verified=True)

    verify_email.short_description = "Mark email as verified"


# ===========================
# BLOG ADMIN
# ===========================

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "status",
        "category",
        "total_views",
        "total_likes",
        "published_at",
        "created_at",
    )

    list_filter = (
        "status",
        "category",
        "nation",
        "published_at",
        "created_at",
    )

    search_fields = (
        "title",
        "slug",
        "author__email",
        "author__username",
    )

    prepopulated_fields = {"slug": ("title",)}

    ordering = ("-created_at",)

    readonly_fields = (
        "id",
        "total_views",
        "total_likes",
        "total_comments",
        "total_bookmarks",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Author", {
            "fields": ("author",)
        }),
        ("Content", {
            "fields": (
                "title",
                "slug",
                "short_description",
                "content",
                "cover_image",
            )
        }),
        ("Classification", {
            "fields": (
                "category",
                "nation",
                "keywords",
            )
        }),
        ("Status & Visibility", {
            "fields": (
                "status",
                "is_comments_enabled",
                "published_at",
            )
        }),
        ("Metrics (Read-only)", {
            "fields": (
                "total_views",
                "total_likes",
                "total_comments",
                "total_bookmarks",
            )
        }),
        ("System", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    filter_horizontal = ("keywords",)

    actions = (
        "publish_blogs",
        "unpublish_blogs",
    )

    def publish_blogs(self, request, queryset):
        queryset.update(status="PUBLISHED")

    publish_blogs.short_description = "Publish selected blogs"

    def unpublish_blogs(self, request, queryset):
        queryset.update(status="DRAFT")

    unpublish_blogs.short_description = "Move selected blogs to Draft"


# ===========================
# BLOG KEYWORD ADMIN
# ===========================

@admin.register(BlogKeyword)
class BlogKeywordAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
