from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
import random
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from blog.models import Post
from newsletter.forms import NewsletterForm, ClientForm, MessageForm, NewsletterFinishForm
from newsletter.models import Newsletter, Client, Message, Attempt
import logging
from newsletter.services import get_newsletters_from_cache

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
    template_name = 'newsletter/main_page.html'
    context_object_name = 'newsletters'

    def get_queryset(self):
        return get_newsletters_from_cache()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        total_newsletters = Newsletter.objects.count()

        active_newsletters = Newsletter.objects.filter(
            initial__lte=now,
            end_date__gte=now,
            finished=False
        ).count()

        unique_clients = Client.objects.distinct().count()

        all_posts = list(Post.objects.all())
        random_posts = random.sample(all_posts, min(len(all_posts), 3))

        context.update({
            'total_newsletters': total_newsletters,
            'active_newsletters': active_newsletters,
            'unique_clients': unique_clients,
            'random_posts': random_posts
        })

        return context


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


class NewsletterFinishView(PermissionRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterFinishForm
    template_name = 'newsletter/newsletter_finish_form.html'
    success_url = reverse_lazy('newsletter:newsletter_list')
    permission_required = 'newsletter.can_turn_the_newsletter_off'