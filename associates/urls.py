from django.urls import path

from . import views

app_name = 'associates'

urlpatterns = [
    path('', views.AssociateListView.as_view(), name='associate-list'),
    path('create/', views.AssociateCreateView.as_view(),
         name='associate-create'),
    path('<int:pk>/', views.AssociateDetailView.as_view(),
         name='associate-detail'),
    path('<int:pk>/update/', views.AssociateUpdateView.as_view(),
         name='associate-update'),
    path('<int:pk>/delete/', views.AssociateDeleteView.as_view(),
         name='associate-delete')
]
