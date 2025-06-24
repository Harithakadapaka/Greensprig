from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from plants import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('profile/', views.profile, name='profile'),  # Add the profile page URL
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('comment/<int:pk>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('favorites/', views.favorite_posts, name='favorite_posts'),
    path('post/<int:post_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('profile/', views.profile_view, name='profile'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('educational-resources/', views.educational_resources, name='educational_resources'),
    path('tag/<slug:tag>/', views.tagged_posts, name='tagged_posts'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)