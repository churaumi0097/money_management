from .models import Post,Category
from django import forms
from datetime import datetime

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =  ['date', 'name', 'category', 'price']
        widgets = {
            "date":forms.DateInput(attrs={"placeholder":f"{datetime.now()}","type": "date"})
        }

