from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy


from .models import Tiger
from .forms import TigerForm
# from .admin import TigerResource
from .serializers import TigerSerializer

from apps.teams.models import Team
from apps.teams.mixins import LoginAndTeamRequiredMixin
from apps.teams.roles import is_admin, is_member
from apps.teams.permissions import TeamAccessPermissions, TeamModelAccessPermissions

# Create your views here.

# List of objects, at http://<server>/a/<team>/tigers/
class TigersListView(LoginAndTeamRequiredMixin, ListView):
    model = Tiger
    paginate_by = 20
    template_name = 'tigers/tiger_list.html'
    context_object_name = 'objects'


# One object, at http://<server>/a/<team>/tigers/1/
class TigerDetailView(LoginAndTeamRequiredMixin, DetailView):
    model = Tiger


# Create a new object, at http://<server>/a/<team>/tigers/new/
class TigerCreateView(LoginAndTeamRequiredMixin, CreateView):
    model = Tiger
    form_class = TigerForm


# Update object, at http://<server>/a/<team>/tigers/1/update/
class TigerUpdateView(LoginAndTeamRequiredMixin, UpdateView):
    model = Tiger
    form_class = TigerForm


# Delete object, at http://<server>/a/<team>/tigers/1/delete/
class TigerDeleteView(LoginAndTeamRequiredMixin, DeleteView):
    model = Tiger

    def get_success_url(self):
        return reverse_lazy('tigers:tiger-listview', kwargs={'team_slug': self.request.team.slug})


# API at http://localhost:8000/a/<team>/tigers/api/tigers/
class TigerViewSet(viewsets.ModelViewSet):
    queryset = Tiger.objects.all()
    serializer_class = TigerSerializer
    permission_classes = (TeamModelAccessPermissions,)

    # permission_classes = (TigerAccessPermissions,)

    @property
    def team(self):
        """Get the team from the URL, and ensure user is a member."""
        team = get_object_or_404(Team, slug=self.kwargs['team_slug'])
        if is_member(self.request.user, team):
            return team
        else:
            raise PermissionDenied()

    def get_queryset(self):
        """Filter queryset based on logged-in user's team."""
        return self.queryset.filter(team=self.team)

    def perform_create(self, serializer):
        """Add team to the model during creation."""
        serializer.save(team=self.team)
