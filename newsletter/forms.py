from django import forms
from newsletter.models import Newsletter, Client, Message
from django.utils import timezone


class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-control-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class NewsletterForm(FormStyleMixin, forms.ModelForm):
    initial = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Newsletter
        exclude = ('status', 'user', )

        widgets = {
            'initial': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'frequency': forms.Select(choices=[('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly')],
                                      attrs={'class': 'form-control'}),
            'message': forms.Select(attrs={'class': 'form-control'}),
            'clients': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(user=user)
        self.fields['message'].queryset = Message.objects.filter(user=user)


class ClientForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('user', )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


class MessageForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('user', )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


class NewsletterFinishForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['finished']