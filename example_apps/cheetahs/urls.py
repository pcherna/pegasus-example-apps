from django.urls import path
from rest_framework import routers

from . import views


app_name = 'cheetahs'

urlpatterns = [
    path('', views.CheetahsListView.as_view(), name='cheetah-listview'),
    path('<int:pk>/', views.CheetahDetailView.as_view(), name='cheetah-detailview'),
    path('new/', views.CheetahCreateView.as_view(), name='cheetah-createview'),
    path('<int:pk>/update/', views.CheetahUpdateView.as_view(), name='cheetah-updateview'),
    path('<int:pk>/delete/', views.CheetahDeleteView.as_view(), name='cheetah-deleteview'),
]


# drf config
router = routers.DefaultRouter()
router.register('api/cheetahs', views.CheetahViewSet)

urlpatterns += router.urls
