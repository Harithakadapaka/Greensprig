from django import forms
from .models import Post, Comment, Category
from taggit.forms import TagWidget
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    categories = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Select a season"
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'categories', 'tags']
        widgets = {
            'tags': TagWidget(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']

class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        email = cleaned_data.get("email")
        
        # Check if passwords match
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        # Check if email is already used
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already taken.")
        
        return cleaned_data