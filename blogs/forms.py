from django.forms import ModelForm, BooleanField
from django.core.exceptions import ValidationError

from blogs.models import Post


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class PostForm(StyleFormMixin, ModelForm):

    class Meta:
        model = Post
        exclude = ("views_count",)
