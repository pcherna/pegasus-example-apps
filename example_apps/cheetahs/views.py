from rest_framework import viewsets
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy


from .models import Cheetah
# from .permissions import CheetahAccessPermissions
from .forms import CheetahForm
# from .admin import CheetahResource
from .serializers import CheetahSerializer

# Create your views here.

# List of objects, at http://<server>/cheetahs/
class CheetahsListView(LoginRequiredMixin, ListView):
    model = Cheetah
    paginate_by = 20
    template_name = 'cheetahs/cheetah_list.html'
    context_object_name = 'objects'


# One object, at http://<server>/cheetahs/1/
class CheetahDetailView(LoginRequiredMixin, DetailView):
    model = Cheetah


# Create a new object, at http://<server>/cheetahs/new/
class CheetahCreateView(LoginRequiredMixin, CreateView):
    model = Cheetah
    form_class = CheetahForm


# Update object, at http://<server>/cheetahs/1/update/
class CheetahUpdateView(LoginRequiredMixin, UpdateView):
    model = Cheetah
    form_class = CheetahForm


# Delete object, at http://<server>/cheetahs/1/delete/
class CheetahDeleteView(LoginRequiredMixin, DeleteView):
    model = Cheetah
    success_url = reverse_lazy('cheetahs:cheetah-listview')


# API at http://localhost:8000/cheetahs/api/cheetahs/
class CheetahViewSet(viewsets.ModelViewSet):
    serializer_class = CheetahSerializer
    queryset = Cheetah.objects.all()
    # ZZZ: Not sure why yet, but all users seem to be able to Read
    # permission_classes = (CheetahAccessPermissions,)
