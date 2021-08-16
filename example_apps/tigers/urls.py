from django.urls import path
from rest_framework import routers

from . import views


app_name = 'tigers'

urlpatterns = [
    path('', views.TigersListView.as_view(), name='tiger-listview'),
    path('<int:pk>/', views.TigerDetailView.as_view(), name='tiger-detail'),
    path('new/', views.TigerCreateView.as_view(), name='tiger-createview'),
    path('<int:pk>/update/', views.TigerUpdateView.as_view(), name='tiger-updateview'),
    path('<int:pk>/delete/', views.TigerDeleteView.as_view(), name='tiger-deleteview'),
]


# drf config
router = routers.DefaultRouter()
router.register('api/tigers', views.TigerViewSet)

urlpatterns += router.urls
