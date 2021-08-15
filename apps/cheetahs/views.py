from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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

# List of objects, at http://localhost:8000/cheetahs/
class CheetahsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Cheetah
    paginate_by = 20
    template_name = 'cheetahs/cheetah_list.html'
    context_object_name = 'objects'

    def test_func(self):
        return self.request.user.has_perm('cheetahs.view_cheetah')

# One object, at http://localhost:8000/cheetahs/1/
class CheetahDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Cheetah

    def test_func(self):
        return self.request.user.has_perm('cheetahs.view_cheetah')

# Create a new object, at http://localhost:8000/cheetahs/new/
class CheetahCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Cheetah
    form_class = CheetahForm

    def test_func(self):
        return self.request.user.has_perm('cheetahs.add_cheetah')

# Update object, at http://localhost:8000/cheetahs/1/update/
class CheetahUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Cheetah
    form_class = CheetahForm

    def test_func(self):
        return self.request.user.has_perm('cheetahs.change_cheetah')

# Delete object, at http://localhost:8000/cheetahs/1/delete/
class CheetahDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Cheetah
    success_url = reverse_lazy('cheetahs:cheetah-listview')

    def test_func(self):
        return self.request.user.has_perm('cheetahs.delete_cheetah')

# API at /cheetahs/api/cheetahs
class CheetahViewSet(viewsets.ModelViewSet):
    serializer_class = CheetahSerializer
    queryset = Cheetah.objects.all()
    # ZZZ: Not sure why yet, but all users seem to be able to Read
    permission_classes = (DjangoModelPermissions,)

    # permission_classes = (CheetahAccessPermissions,)

    # def get_queryset(self):
    #     # filter queryset based on logged in user
    #     return self.request.user.cheetahs.all()

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
