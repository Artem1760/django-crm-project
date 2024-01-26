from django.urls import path

from . import views

app_name = 'tickets'

urlpatterns = [
    # Ticket views
    path('', views.TicketListView.as_view(), name='ticket-list'),
    path('create/', views.TicketCreateView.as_view(), name='ticket-create'),
    path('<int:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('<int:pk>/update/', views.TicketUpdateView.as_view(),
         name='ticket-update'),
    path('<int:pk>/delete/', views.TicketDeleteView.as_view(),
         name='ticket-delete'),
    path('<int:pk>/assign-associate/', views.AssignAssociateView.as_view(),
         name='assign-associate'),
    path('<int:pk>/category/', views.TicketCategoryUpdateView.as_view(),
         name='ticket-category-update'),

    # FollowUp views
    path('<int:pk>/followups/create/', views.FollowUpCreateView.as_view(),
         name='ticket-followup-create'),
    path('followups/<int:pk>/update/', views.FollowUpUpdateView.as_view(),
         name='ticket-followup-update'),
    path('followups/<int:pk>/delete/', views.FollowUpDeleteView.as_view(),
         name='ticket-followup-delete'),

    # Category views
    path('categories/', views.CategoryListView.as_view(),
         name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(),
         name='category-detail'),
    path('create-category/', views.CategoryCreateView.as_view(),
         name='category-create'),

    # JSON view
    path('json/', views.TicketJsonView.as_view(), name='ticket-list-json'),
]
