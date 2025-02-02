from django.forms import ModelForm
from django.contrib.auth import get_user_model

from xss.models import Comment


class CommentForm(ModelForm):
    
    def save(self, commit=True):
        # adding superuser as the user of the comment.
        user = get_user_model().objects.get(username='amin')
        instance = super().save(commit=False)
        instance.user = user
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Comment
        fields = ['message']
