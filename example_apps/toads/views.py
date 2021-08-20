from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import permission_required

from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from django.urls import reverse

from apps.teams.decorators import login_and_team_required
from apps.teams.models import Team

from .models import Toad
from .forms import ToadForm
from .serializers import ToadSerializer

# team_slug comes from the url you're trying to access
# request.session['team'].slug and request.team are set for us by the login_and_team_required decorator

# List of objects, at http://<server>/a/<team>/toads/
@login_and_team_required
@permission_required('toads.view_toad', raise_exception=True)
def list_view(request, team_slug):
    context = {}
    # Only show this team's objects
    context['objects'] = Toad.objects.filter(team=request.team)
    context['team'] = request.team
    return render(request, 'toads/toad_list.html', context)

# One object, at http://<server>/a/<team>/toads/1/
@login_and_team_required
@permission_required('toads.view_toad', raise_exception=True)
def detail_view(request, team_slug, pk):
    context = {}
    # Allow only if object belongs to this team
    context['object'] = get_object_or_404(Toad, id=pk, team=request.team)
    context['team'] = request.team
    return render(request, 'toads/toad_detail.html', context)

# Create a new object, at http://<server>/a/<team>/toads/new/
@login_and_team_required
@permission_required('toads.add_toad', raise_exception=True)
def create_view(request, team_slug):
    context = {}
    form = ToadForm(request.POST or None)
    if form.is_valid():
        new_object = form.save(commit=False)
        # Add my team to the object
        new_object.team = request.team
        new_object.save()
        return HttpResponseRedirect(reverse('toads:toad-detailview', kwargs={'team_slug': team_slug, 'pk': new_object.id}))
    context['form'] = form
    context['team'] = request.team
    return render(request, 'toads/toad_form.html', context)

# Update object, at http://<server>/a/<team>/toads/1/update/
@login_and_team_required
@permission_required('toads.change_toad', raise_exception=True)
def update_view(request, team_slug, pk):
    context = {}
    # Allow only if object belongs to this team
    obj = get_object_or_404(Toad, id=pk, team=request.team)
    form = ToadForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('toads:toad-detailview', kwargs={'team_slug': team_slug, 'pk': pk}))
    context['form'] = form
    context['team'] = request.team
    context['object'] = obj
    return render(request, 'toads/toad_form.html', context)

# delete object, at http://<server>/a/<team>/toads/1/delete/
@login_and_team_required
@permission_required('toads.delete_toad', raise_exception=True)
def delete_view(request, team_slug, pk):
    # Allow only if object belongs to this team
    obj = get_object_or_404(Toad, id=pk, team=request.team)
    obj.delete()
    return HttpResponseRedirect(reverse('toads:toad-listview', kwargs={'team_slug': team_slug}))

# API at /toads/api/toads
# TODO: Does not yet have team restrictions
class ToadViewSet(viewsets.ModelViewSet):
    serializer_class = ToadSerializer
    queryset = Toad.objects.all()
    # ZZZ: Not sure why yet, but all users seem to be able to Read
    permission_classes = (DjangoModelPermissions,)

    # permission_classes = (ToadAccessPermissions,)

    # def get_queryset(self):
    #     # filter queryset based on logged in user
    #     return self.request.user.toads.all()

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
