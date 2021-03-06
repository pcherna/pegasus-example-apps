from django.urls import path
from rest_framework import routers

from . import views


app_name = 'toads'

urlpatterns = [
    path('', views.list_view, name='toad-listview'),
    path('<int:pk>/', views.detail_view, name='toad-detailview'),
    path('new/', views.create_view, name='toad-createview'),
    path('<int:pk>/update/', views.update_view, name='toad-updateview'),
    path('<int:pk>/delete/', views.delete_view, name='toad-deleteview'),
]


# drf config
router = routers.DefaultRouter()
router.register('api/toads', views.ToadViewSet)

urlpatterns += router.urls
