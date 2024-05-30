from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
import pytz
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from newsletter.forms import NewsletterForm, ClientForm, MessageForm
from newsletter.models import Newsletter, Client, Message, Attempt
import logging


logger = logging.getLogger(__name__)


class UserIsOwnerOrHasPermissionMixin:
    permission_required = None

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        if user == obj.user or user.has_perm(self.permission_required):
            return True
        return False

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to perform this action.")


class ContactsTemplateView(LoginRequiredMixin, TemplateView):
    model = Newsletter
    template_name = 'newsletter/contacts.html'


# Newsletter


class NewsletterListView(ListView):
    model = Newsletter
    template_name = 'newsletter/newsletter_list.html'


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'newsletter/newsletter_form.html'
    success_url = reverse_lazy('newsletter:newsletter_list')

    def form_valid(self, form):
        newsletter = form.save()
        user = self.request.user
        newsletter.user = user
        newsletter.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['clients'].queryset = Client.objects.filter(user=self.request.user)
        form.fields['message'].queryset = Message.objects.filter(user=self.request.user)
        return form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class NewsletterDetailView(LoginRequiredMixin, UserIsOwnerOrHasPermissionMixin, DetailView):
    model = Newsletter
    permission_required = 'newsletter.can_view_any_newsletter'
    template_name = 'newsletter/newsletter.html'

    def get(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()
        return super().get(request, *args, **kwargs)


class NewsletterUpdateView(LoginRequiredMixin, UserIsOwnerOrHasPermissionMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    permission_required = 'newsletter.update_newsletter'
    template_name = 'newsletter/newsletter_form.html'
    success_url = reverse_lazy('newsletter:newsletter_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class NewsletterDeleteView(LoginRequiredMixin, UserIsOwnerOrHasPermissionMixin, DeleteView):
    model = Newsletter
    permission_required = 'newsletter.delete_newsletter'
    success_url = reverse_lazy('newsletter:newsletter_list')

    def delete(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()
        return super().delete(request, *args, **kwargs)


# Client


class ClientListView(ListView):
    model = Client
    template_name = 'newsletter/client_list.html'


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.user = user
        client.save()
        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, UserIsOwnerOrHasPermissionMixin, DetailView):
    model = Client
    template_name = 'newsletter/client.html'

    def get(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()
        return super().get(request, *args, **kwargs)


class ClientUpdateView(LoginRequiredMixin, UserIsOwnerOrHasPermissionMixin, UpdateView):
    model = Client
    form_class = ClientForm
    permission_required = 'newsletter.update_client'
    template_name = 'newsletter/client_form.html'
    success_url = reverse_lazy('newsletter:client_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ClientDeleteView(LoginRequiredMixin, UserIsOwnerOrHasPermissionMixin, DeleteView):
    model = Client
    permission_required = 'newsletter.delete_client'
    success_url = reverse_lazy('newsletter:client_list')

    def delete(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()
        return super().delete(request, *args, **kwargs)


# Message


class MessageListView(ListView):
    model = Message
    template_name = 'newsletter/message_list.html'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletter:message_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.user = user
        message.save()
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, UserIsOwnerOrHasPermissionMixin, DetailView):
    model = Message
    template_name = 'newsletter/message.html'

    def get(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()
        return super().get(request, *args, **kwargs)


class MessageUpdateView(LoginRequiredMixin, UserIsOwnerOrHasPermissionMixin, UpdateView):
    model = Message
    form_class = MessageForm
    permission_required = 'newsletter.update_message'
    success_url = reverse_lazy('newsletter:message_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MessageDeleteView(LoginRequiredMixin, UserIsOwnerOrHasPermissionMixin, DeleteView):
    model = Message
    permission_required = 'newsletter.delete_message'
    success_url = reverse_lazy('newsletter:message_list')

    def delete(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()
        return super().delete(request, *args, **kwargs)


class AttemptListView(ListView):
    model = Attempt
    template_name = 'newsletter/attempt_list.html'
    context_object_name = 'attempts'


    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     ProductFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)
    #     if self.request.method == 'POST':
    #         context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
    #     else:
    #         context_data['formset'] = ProductFormset(instance=self.object)
    #     return context_data

    # def form_valid(self, form):
    #     context_data = self.get_context_data()
    #     formset = context_data['formset']
    #     if form.is_valid() and formset.is_valid():
    #         self.object = form.save()
    #         formset.instance = self.object
    #         formset.save()
    #         return super().form_valid(form)
    #     else:
    #         return self.render_to_response(self.get_context_data(form=form, formset=formset))

    # def get_form_class(self):
    #     user = self.request.user
    #     if user == self.object.salesman:
    #         return ProductForm
    #     if user.has_perm('newsletter.set_published'):
    #         return ProductModeratorForm
    #     raise PermissionDenied




# class VersionCreateView(LoginRequiredMixin, CreateView):
#     model = Version
#     form_class = ProductForm
#     success_url = reverse_lazy('newsletter:product_list')
