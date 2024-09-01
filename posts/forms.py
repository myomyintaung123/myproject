from django import forms
from .models import Post

class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','body','slug','image']




class LikeForm(forms.Form):
    post_id = forms.IntegerField(widget=forms.HiddenInput)