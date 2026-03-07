from django import forms
from .models import User, Comment

class ProfileUpdateForm(forms.ModelForm):
    """
    Form used to update user profile information,
    including profile image.
    hi i am maaz siddiqui
    i am from india
    i am a student
    i am a web developer
    
    """

    class Meta:
        model = User
        fields = [
            "profile_image",     # ✅ included ONCE
            "full_name",
            "bio",
            "website",
            "instagram_link",
            "x_link",
            "git_link",
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control mt-2'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram_link': forms.URLInput(attrs={'class': 'form-control'}),
            'x_link': forms.URLInput(attrs={'class': 'form-control'}),
            'git_link': forms.URLInput(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            })
        }
