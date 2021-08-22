from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import permission_required

from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.exceptions import PermissionDenied
from django.urls import reverse


from .models import Polliwog
from .forms import PolliwogForm
from .serializers import PolliwogSerializer

from apps.teams.models import Team
from apps.teams.decorators import login_and_team_required
from apps.teams.permissions import TeamAccessPermissions, TeamModelAccessPermissions
from apps.teams.roles import is_admin, is_member

# team_slug comes from the url you're trying to access
# request.session['team'].slug and request.team are set for us by the login_and_team_required decorator

# List of objects, at http://<server>/a/<team>/polliwogs/
@login_and_team_required
@permission_required('polliwogs.view_polliwog', raise_exception=True)
def list_view(request, team_slug):
    context = {}
    # Only show this team's objects
    context['objects'] = Polliwog.objects.filter(team=request.team)
    context['team'] = request.team
    return render(request, 'polliwogs/polliwog_list.html', context)

# One object, at http://<server>/a/<team>/polliwogs/1/
@login_and_team_required
@permission_required('polliwogs.view_polliwog', raise_exception=True)
def detail_view(request, team_slug, pk):
    context = {}
    # Allow only if object belongs to this team
    context['object'] = get_object_or_404(Polliwog, id=pk, team=request.team)
    context['team'] = request.team
    return render(request, 'polliwogs/polliwog_detail.html', context)

# Create a new object, at http://<server>/a/<team>/polliwogs/new/
@login_and_team_required
@permission_required('polliwogs.add_polliwog', raise_exception=True)
def create_view(request, team_slug):
    context = {}
    form = PolliwogForm(request.POST or None)
    if form.is_valid():
        new_object = form.save(commit=False)
        # Add my team to the object
        new_object.team = request.team
        new_object.save()
        return HttpResponseRedirect(reverse('polliwogs:polliwog-detailview', kwargs={'team_slug': team_slug, 'pk': new_object.id}))
    context['form'] = form
    context['team'] = request.team
    return render(request, 'polliwogs/polliwog_form.html', context)

# Update object, at http://<server>/a/<team>/polliwogs/1/update/
@login_and_team_required
@permission_required('polliwogs.change_polliwog', raise_exception=True)
def update_view(request, team_slug, pk):
    context = {}
    # Allow only if object belongs to this team
    obj = get_object_or_404(Polliwog, id=pk, team=request.team)
    form = PolliwogForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('polliwogs:polliwog-detailview', kwargs={'team_slug': team_slug, 'pk': pk}))
    context['form'] = form
    context['team'] = request.team
    context['object'] = obj
    return render(request, 'polliwogs/polliwog_form.html', context)

# delete object, at http://<server>/a/<team>/polliwogs/1/delete/
@login_and_team_required
@permission_required('polliwogs.delete_polliwog', raise_exception=True)
def delete_view(request, team_slug, pk):
    # Allow only if object belongs to this team
    obj = get_object_or_404(Polliwog, id=pk, team=request.team)
    obj.delete()
    return HttpResponseRedirect(reverse('polliwogs:polliwog-listview', kwargs={'team_slug': team_slug}))

# API at http://localhost:8000/a/<team>/polliwogs/api/polliwogs/
class PolliwogViewSet(viewsets.ModelViewSet):
    queryset = Polliwog.objects.all()
    serializer_class = PolliwogSerializer
    permission_classes = (TeamModelAccessPermissions,)
    # ZZZ: Not sure why yet, but all users seem to be able to Read
    # permission_classes = (DjangoModelPermissions,)

    # permission_classes = (PolliwogAccessPermissions,)

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
