from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required, permission_required

from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from django.urls import reverse


from .models import Frog
from .forms import FrogForm
from .serializers import FrogSerializer

# List of objects, at http://localhost:8000/frogs/
@login_required
@permission_required('frogs.view_frog', raise_exception=True)
def list_view(request):
    context = {}
    context['objects'] = Frog.objects.all()
    return render(request, 'frogs/frogs_list.html', context)

# One object, at http://localhost:8000/frogs/1/
@login_required
@permission_required('frogs.view_frog', raise_exception=True)
def detail_view(request, pk):
    context = {}
    context['object'] = Frog.objects.get(id=pk)
    return render(request, 'frogs/frog_detail.html', context)

# Create a new object, at http://localhost:8000/frogs/new/
@login_required
@permission_required('frogs.add_frog', raise_exception=True)
def create_view(request):
    context = {}
    form = FrogForm(request.POST or None)
    if form.is_valid():
        saved_form = form.save()
        return HttpResponseRedirect(reverse('frogs:frog-detailview', kwargs={'pk': saved_form.id}))
    context['form'] = form
    return render(request, 'frogs/frog_form.html', context)

# Update object, at http://localhost:8000/frogs/1/update/
@login_required
@permission_required('frogs.change_frog', raise_exception=True)
def update_view(request, pk):
    context = {}
    obj = get_object_or_404(Frog, id=pk)
    form = FrogForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('frogs:frog-detailview', kwargs={'pk': pk}))
    context['form'] = form
    context['object'] = obj
    return render(request, 'frogs/frog_form.html', context)

# delete object, at http://localhost:8000/frogs/1/delete/
@login_required
@permission_required('frogs.delete_frog', raise_exception=True)
def delete_view(request, pk):
    obj = get_object_or_404(Frog, id=pk)
    obj.delete()
    return HttpResponseRedirect(reverse('frogs:frogs-listview'))

# API at /frogs/api/frogs
class FrogViewSet(viewsets.ModelViewSet):
    serializer_class = FrogSerializer
    queryset = Frog.objects.all()
    # ZZZ: Not sure why yet, but all users seem to be able to Read
    permission_classes = (DjangoModelPermissions,)

    # permission_classes = (FrogAccessPermissions,)

    # def get_queryset(self):
    #     # filter queryset based on logged in user
    #     return self.request.user.frogs.all()

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
