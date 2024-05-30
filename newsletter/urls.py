from django.urls import path


from newsletter.views import NewsletterListView, NewsletterDetailView, NewsletterCreateView, NewsletterUpdateView, \
    NewsletterDeleteView, ClientCreateView, ClientDetailView, ClientUpdateView, ClientDeleteView, MessageDetailView, \
    MessageCreateView, MessageUpdateView, MessageDeleteView, ClientListView, MessageListView, AttemptListView, \
    NewsletterFinishView

app_name = 'newsletter'



urlpatterns = [
    # Newsletter
    path('', NewsletterListView.as_view(), name='newsletter_list'),
    path('newsletter/<int:pk>', NewsletterDetailView.as_view(), name='newsletter_page'),
    path('newsletter_create/', NewsletterCreateView.as_view(), name='create_newsletter'),
    path('newsletter_update/<int:pk>', NewsletterUpdateView.as_view(), name='update_newsletter'),
    path('newsletter_delete/<int:pk>', NewsletterDeleteView.as_view(), name='delete_newsletter'),
    # Clients
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>', ClientDetailView.as_view(), name='client_page'),
    path('client_create/', ClientCreateView.as_view(), name='create_client'),
    path('client_update/<int:pk>', ClientUpdateView.as_view(), name='update_client'),
    path('client_delete/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),
    # Messages
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>', MessageDetailView.as_view(), name='message_page'),
    path('message_create/', MessageCreateView.as_view(), name='create_message'),
    path('message_update/<int:pk>', MessageUpdateView.as_view(), name='update_message'),
    path('message_delete/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),
    # Other
    path('attempts/', AttemptListView.as_view(), name='attempt_list'),
    path('newsletter_finish/<int:pk>/', NewsletterFinishView.as_view(), name='newsletter_finish'),

]
