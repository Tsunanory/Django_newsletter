from django import forms
from django.core.exceptions import ValidationError

from newsletter.models import Newsletter, Client, Message


class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-control-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class NewsletterForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Newsletter
        exclude = ('status',)
        widgets = {
            'initial': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'frequency': forms.Select(choices=[('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly')],
                                      attrs={'class': 'form-control'}),
            'message': forms.Select(attrs={'class': 'form-control'}),
            'clients': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class ClientForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class MessageForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
