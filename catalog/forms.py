from django.forms import ModelForm, BooleanField
from django.core.exceptions import ValidationError

from catalog.models import Product


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ProductForm(StyleFormMixin, ModelForm):
    FORBIDDEN_WORDS = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]

    class Meta:
        model = Product
        fields = "__all__"
        exclude = ["owner"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            for word in self.FORBIDDEN_WORDS:
                if word in name.lower():
                    raise ValidationError(f"Название товара содержит запрещенное слово: {word}")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if description:
            for word in self.FORBIDDEN_WORDS:
                if word in description.lower():
                    raise ValidationError(f"Описание товара содержит запрещенное слово: {word}")
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise ValidationError("Цена не может быть отрицательной!")
        return price


class ProductModeratorForm(StyleFormMixin, ModelForm):

    class Meta:
        model = Product
        fields = ("is_published",)
