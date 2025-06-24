from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # to use User model for profile page
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post, Favorite
from django.core.paginator import Paginator
from .models import UserProfile
from django.db.models import Q
from .models import Post, Category
from .forms import UserProfileForm
from .forms import UserSignupForm
from django.contrib.auth import login


# Sign-up view
def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            return redirect('home')  # Redirect to the home page after successful sign-up
    else:
        form = UserSignupForm()
    
    return render(request, 'signup.html', {'form': form})

# Home page view (Displays recent posts with pagination)
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'public_home.html')  # New guest homepage
    
    # Get the search query from the URL parameter
    query = request.GET.get('q', '')  # Default to empty string if no query
    category_filter = request.GET.get('category', '')  # Get category filter from URL
    tag_filter = request.GET.get('tag', '')
    
    if query:
        # If there is a query, filter posts based on the title or content
        posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-created_at')
    else:
        # If there is no query, show all posts
        posts = Post.objects.all().order_by('-created_at')

    if category_filter:
        posts = posts.filter(categories__name=category_filter)  # Filter posts by selected category

    if tag_filter:
        posts = posts.filter(tags__name__in=[tag_filter])  # taggit supports this lookup

    # Pagination
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')  # Get the page number from URL
    page_obj = paginator.get_page(page_number)  # Get the page object
    
    categories = Category.objects.all()  # Fetch all categories for the category filter
    tags = Post.tags.all()  # Get all tags

    return render(request, 'home.html', {'posts': page_obj, 'query': query,'categories': categories, 'category_filter' : category_filter, 'tag_filter': tag_filter, 'tags': tags})


# Post detail view (Displays individual post and its comments)
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    # Check if user has favorited this post
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, post=post).exists()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'is_favorited': is_favorited,
    })

# Create post view (Allows users to create new posts)
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # include request.FILES
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

# Profile page view (Only accessible to logged-in users)
@login_required
def profile(request):
    # Get or create a user profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = UserProfileForm(instance=user_profile)

    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'form': form, 'user_posts': user_posts})


# Edit post view
@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if post.author != request.user:
        return redirect('home')  # Only the author can edit their post
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)  # include request.FILES
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'edit_post.html', {'form': form, 'post': post})

# Delete post view
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if post.author != request.user:
        return redirect('home')  # Only the author can delete their post
    
    if request.method == 'POST':
        post.delete()
        return redirect('home')  # Redirect to the homepage after deletion

    return render(request, 'delete_post.html', {'post': post})


def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        content = request.POST['content']
        
        # Create a new comment and associate it with the post and the logged-in user
        Comment.objects.create(post=post, author=request.user, content=content)

        return redirect('post_detail', pk=post.id)  # Redirect to the post detail page

    return redirect('post_detail', pk=post_id)


# Edit the comment
@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    if comment.author != request.user:
        return redirect('post_detail', pk=comment.post.pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})

#delete the comment
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    if comment.author != request.user:
        return redirect('post_detail', pk=comment.post.pk)
    
    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', pk=comment.post.pk)

    return render(request, 'delete_comment.html', {'comment': comment})


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Remove like
    else:
        post.likes.add(request.user)  # Add like
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))  # Redirect to post detail page


@login_required
def toggle_favorite(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, post=post)
    if not created:
        favorite.delete()  # Remove favorite if it already exists
    return redirect('post_detail', pk=post.pk)  # Redirect to the post detail page

@login_required
def favorite_posts(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('post')
    posts = [favorite.post for favorite in favorites]
    return render(request, 'favorites.html', {'posts': posts})

def post_list(request):
    posts = Post.objects.all()

    # Filter by category (if applicable)
    category = request.GET.get('category')
    if category:
        posts = posts.filter(category__name=category)

    # Pagination
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'post_list.html', {'page_obj': page_obj})


@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')

    return render(request, 'profile.html', {
        'form': form,
        'user_posts': user_posts,
    })

def educational_resources(request):
    return render(request, 'educational_resources.html')

# views.py
def tagged_posts(request, tag):
    posts = Post.objects.filter(tags__name__in=[tag])
    return render(request, 'tagged_posts.html', {'tag': tag, 'posts': posts})
