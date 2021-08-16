from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy

from apps.teams.mixins import LoginAndTeamRequiredMixin

from .models import Tiger
# from .permissions import TigerAccessPermissions
from .forms import TigerForm
# from .admin import TigerResource
from .serializers import TigerSerializer

# Create your views here.

# List of objects, at http://localhost:8000/tigers/
class TigersListView(LoginAndTeamRequiredMixin, UserPassesTestMixin, ListView):
    model = Tiger
    paginate_by = 20
    template_name = 'tigers/tiger_list.html'
    context_object_name = 'objects'

    def test_func(self):
        return self.request.user.has_perm('tigers.view_tiger')

# One object, at http://localhost:8000/tigers/1/
class TigerDetailView(LoginAndTeamRequiredMixin, UserPassesTestMixin, DetailView):
    model = Tiger

    def test_func(self):
        return self.request.user.has_perm('tigers.view_tiger')

# Create a new object, at http://localhost:8000/tigers/new/
class TigerCreateView(LoginAndTeamRequiredMixin, UserPassesTestMixin, CreateView):
    model = Tiger
    form_class = TigerForm

    def test_func(self):
        return self.request.user.has_perm('tigers.add_tiger')

    def form_valid(self, form):
        form.instance.team = self.request.team
        return super().form_valid(form)


# Update object, at http://localhost:8000/tigers/1/update/
class TigerUpdateView(LoginAndTeamRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tiger
    form_class = TigerForm

    def test_func(self):
        return self.request.user.has_perm('tigers.change_tiger')

# Delete object, at http://localhost:8000/tigers/1/delete/
class TigerDeleteView(LoginAndTeamRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tiger

    def get_success_url(self):
        return reverse_lazy('tigers:tiger-listview', kwargs={'team_slug': self.request.team_slug})

    def test_func(self):
        return self.request.user.has_perm('tigers.delete_tiger')

# API at /tigers/api/tigers
class TigerViewSet(viewsets.ModelViewSet):
    serializer_class = TigerSerializer
    queryset = Tiger.objects.all()
    # ZZZ: Not sure why yet, but all users seem to be able to Read
    permission_classes = (DjangoModelPermissions,)

    # permission_classes = (TigerAccessPermissions,)

    # def get_queryset(self):
    #     # filter queryset based on logged in user
    #     return self.request.user.tigers.all()

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
