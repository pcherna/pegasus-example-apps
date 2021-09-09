from django.urls import path
from rest_framework import routers

from . import views


app_name = 'herons'

urlpatterns = [
    path('', views.HeronsListView.as_view(), name='heron-listview'),
    path('<int:pk>/', views.HeronDetailView.as_view(), name='heron-detailview'),
    path('new/', views.HeronCreateView.as_view(), name='heron-createview'),
    path('<int:pk>/update/', views.HeronUpdateView.as_view(), name='heron-updateview'),
    path('<int:pk>/delete/', views.HeronDeleteView.as_view(), name='heron-deleteview'),
    path('htmx/list/', views.heron_htmx_list, name='heron-htmx-list'),
]


# drf config
router = routers.DefaultRouter()
router.register('api/herons', views.HeronViewSet)

urlpatterns += router.urls
