from django import forms
from main.models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title here'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter content here'}),
        }
        help_texts = {
            'title': '제목을 입력하세요.',
            'content': '내용을 입력하세요.',
        }

    # 추가적인 유효성 검사
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if 'badword' in title:
            raise forms.ValidationError("제목에 부적절한 단어가 포함되어 있습니다.")
        return title

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter comment here'}),
        }
        help_texts = {
            'content': '댓글을 입력하세요.',
        }

    # 추가적인 유효성 검사
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError("댓글은 최소 10자 이상이어야 합니다.")
        return content