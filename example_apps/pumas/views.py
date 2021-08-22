from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy


from .models import Puma
from .forms import PumaForm
# from .admin import PumaResource
from .serializers import PumaSerializer

from apps.teams.models import Team
from apps.teams.mixins import LoginAndTeamRequiredMixin
from apps.teams.roles import is_admin, is_member
from apps.teams.permissions import TeamAccessPermissions, TeamModelAccessPermissions

# Create your views here.

# List of objects, at http://<server>/a/<team>/pumas/
class PumasListView(LoginAndTeamRequiredMixin, UserPassesTestMixin, ListView):
    model = Puma
    paginate_by = 20
    template_name = 'pumas/puma_list.html'
    context_object_name = 'objects'

    def test_func(self):
        return self.request.user.has_perm('pumas.view_puma')

# One object, at http://<server>/a/<team>/pumas/1/
class PumaDetailView(LoginAndTeamRequiredMixin, UserPassesTestMixin, DetailView):
    model = Puma

    def test_func(self):
        return self.request.user.has_perm('pumas.view_puma')

# Create a new object, at http://<server>/a/<team>/pumas/new/
class PumaCreateView(LoginAndTeamRequiredMixin, UserPassesTestMixin, CreateView):
    model = Puma
    form_class = PumaForm

    def test_func(self):
        return self.request.user.has_perm('pumas.add_puma')


# Update object, at http://<server>/a/<team>/pumas/1/update/
class PumaUpdateView(LoginAndTeamRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Puma
    form_class = PumaForm

    def test_func(self):
        return self.request.user.has_perm('pumas.change_puma')

# Delete object, at http://<server>/a/<team>/pumas/1/delete/
class PumaDeleteView(LoginAndTeamRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Puma

    def get_success_url(self):
        return reverse_lazy('pumas:puma-listview', kwargs={'team_slug': self.request.team.slug})

    def test_func(self):
        return self.request.user.has_perm('pumas.delete_puma')

# API at http://localhost:8000/a/<team>/pumas/api/pumas/
class PumaViewSet(viewsets.ModelViewSet):
    queryset = Puma.objects.all()
    serializer_class = PumaSerializer
    permission_classes = (TeamModelAccessPermissions,)
    # ZZZ: Not sure why yet, but all users seem to be able to Read
    # permission_classes = (DjangoModelPermissions,)

    # permission_classes = (PumaAccessPermissions,)

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
