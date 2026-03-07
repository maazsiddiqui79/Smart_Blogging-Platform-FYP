from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('forget-id-pass/', views.fogretcred, name='forget-id-pass'),
    path('guide/', views.guide, name='guide'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('create-blog/', views.create_blog_func, name='create_blog'),
    path('delete-blog/<int:id>/', views.delete_blog_func, name='delete'),
    path('change-visibility/<int:id>/<str:status>/', views.change_visibility, name='change_visibility'),
    path('access-blog/<int:id>/', views.access_blog, name='access_blog'),
    path('access-blog/<str:slug>/', views.access_blog_slug, name='access_blog_slug'),
    path("edit-blog/<int:blog_id>/", views.edit_blog, name="edit_blog"),
    path("follow-user/<str:username>/", views.follow_user, name="follow_user"),
    path('author/<str:username>/', views.public_profile, name='public_profile'),
    path('like/<int:id>/', views.like_blog, name='like_blog'),
    path('search/', views.search_blogs, name='search_blogs'),
    path('email-verify/', views.email_verify, name='email_verify'),
    path('delete-acc/', views.delete_acc, name='delete_acc'),
    path('terms-n-condtion/', views.terms_n_condtion, name='terms_n_condtion'),
    path('privacy/', views.privacy, name='privacy'),
    path('add_blog_bm/<int:id>/', views.add_blog_bm, name='add_blog_bm'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
