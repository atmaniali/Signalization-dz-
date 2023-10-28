from django.forms import ModelForm

from product.models import Comment


class CommentForm(ModelForm):
    class Meta:
        models = Comment
        fields = ["subject", "comment", "rate"]
