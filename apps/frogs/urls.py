from django.urls import path
from rest_framework import routers

from . import views


app_name = 'frogs'

urlpatterns = [
    path('', views.list_view, name='frog-list'),
    path('<int:pk>/', views.detail_view, name='frog-detail'),
    path('new/', views.create_view, name='frog-create'),
    path('<int:pk>/update/', views.update_view, name='frog-update'),
    path('<int:pk>/delete/', views.delete_view, name='frog-delete'),
]


# drf config
router = routers.DefaultRouter()
router.register('api/frogs', views.FrogViewSet)

urlpatterns += router.urls
