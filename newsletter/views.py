from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from newsletter.forms import NewsletterForm, ClientForm, MessageForm
from newsletter.models import Newsletter, Client, Message


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


class NewsletterDetailView(LoginRequiredMixin, DetailView):
    model = Newsletter
    template_name = 'newsletter/newsletter.html'


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'newsletter/newsletter_form.html'
    success_url = reverse_lazy('newsletter:newsletter_list')


class NewsletterDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Newsletter
    permission_required = 'newsletter.delete_newsletter'
    success_url = reverse_lazy('newsletter:newsletter_list')


# Client


class ClientListView(ListView):
    model = Client
    template_name = 'newsletter/client_list.html'


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client_list')


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'newsletter/client.html'


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'newsletter/client_form.html'
    success_url = reverse_lazy('newsletter:client_list')


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    permission_required = 'newsletter.delete_client'
    success_url = reverse_lazy('newsletter:client_list')


# Message


class MessageListView(ListView):
    model = Message
    template_name = 'newsletter/message_list.html'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletter:message_list')


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'newsletter/message.html'


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ['topic', 'content']
    success_url = reverse_lazy('newsletter:message_list')


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    permission_required = 'newsletter.delete_message'
    success_url = reverse_lazy('newsletter:message_list')


    # def form_valid(self, form):
    #     product = form.save()
    #     user = self.request.user
    #     product.salesman = user
    #     product.save()
    #     return super().form_valid(form)



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
