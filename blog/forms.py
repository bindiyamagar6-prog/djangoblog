from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "category", "tags", "status"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 8, "class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title