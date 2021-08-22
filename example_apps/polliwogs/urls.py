from django.urls import path
from rest_framework import routers

from . import views


app_name = 'polliwogs'

urlpatterns = [
    path('', views.list_view, name='polliwog-listview'),
    path('<int:pk>/', views.detail_view, name='polliwog-detailview'),
    path('new/', views.create_view, name='polliwog-createview'),
    path('<int:pk>/update/', views.update_view, name='polliwog-updateview'),
    path('<int:pk>/delete/', views.delete_view, name='polliwog-deleteview'),
]


# drf config
router = routers.DefaultRouter()
router.register('api/polliwogs', views.PolliwogViewSet)

urlpatterns += router.urls
