from django.contrib import admin
from .models import Post, Comment, UserProfile, Favorite
from .models import Category 

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Favorite)
admin.site.register(Category)
