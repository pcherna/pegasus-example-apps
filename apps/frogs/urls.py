from django.urls import path
from rest_framework import routers

from . import views


app_name = 'frogs'

urlpatterns = [
    path('', views.list_view, name='frogs-listview'),
    path('<int:pk>/', views.detail_view, name='frog-detailview'),
    path('new/', views.create_view, name='frog-createview'),
    path('<int:pk>/update/', views.update_view, name='frog-updateview'),
    path('<int:pk>/delete/', views.delete_view, name='frog-deleteview'),
]


# drf config
router = routers.DefaultRouter()
router.register('api/frogs', views.FrogViewSet)

urlpatterns += router.urls
