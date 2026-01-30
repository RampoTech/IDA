from django.urls import path
from .views import TicketListView, TicketCreateView, TicketDetailView, TicketUpdateView

urlpatterns = [
    path('', TicketListView.as_view(), name='ticket_list'),
    path('create/', TicketCreateView.as_view(), name='create_ticket'),
    path('<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('<int:pk>/update/', TicketUpdateView.as_view(), name='ticket_update'),
]
