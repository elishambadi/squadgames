# forms.py
from django import forms
from .models import Game, Comment

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'description', 'instructions', 'min_players', 'max_players', 
                  'duration_minutes', 'difficulty', 'categories', 'materials_needed']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'instructions': forms.Textarea(attrs={'rows': 8}),
            'materials_needed': forms.Textarea(attrs={'rows': 3}),
            'categories': forms.CheckboxSelectMultiple(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share your thoughts...'}),
        }

