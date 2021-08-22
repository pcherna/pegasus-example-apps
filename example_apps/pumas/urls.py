from django.urls import path
from rest_framework import routers

from . import views


app_name = 'pumas'

urlpatterns = [
    path('', views.PumasListView.as_view(), name='puma-listview'),
    path('<int:pk>/', views.PumaDetailView.as_view(), name='puma-detailview'),
    path('new/', views.PumaCreateView.as_view(), name='puma-createview'),
    path('<int:pk>/update/', views.PumaUpdateView.as_view(), name='puma-updateview'),
    path('<int:pk>/delete/', views.PumaDeleteView.as_view(), name='puma-deleteview'),
]


# drf config
router = routers.DefaultRouter()
router.register('api/pumas', views.PumaViewSet)

urlpatterns += router.urls
