from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import viewsets
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse, reverse_lazy


from .models import Heron
# from .permissions import HeronAccessPermissions
from .forms import HeronForm
# from .admin import HeronResource
from .serializers import HeronSerializer

# Create your views here.

# List of objects, at http://<server>/herons/
class HeronsListView(LoginRequiredMixin, ListView):
    model = Heron
    template_name = 'herons/heron_list.html'
    # Note: Do not use paginate_by in the ListView class -- see heron_htmx_list()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # Tell the template how it can find the htmx view that contains/refreshes the list data
        context['htmx_list_url'] = reverse('herons:heron-htmx-list')
        context['page'] = self.request.GET.get('page', 1)
        return context

    # def get_queryset(self):
    #     return super().get_queryset()

# htmx view that returns just the object list and paginators
@login_required
def heron_htmx_list(request):
    heron_list = Heron.objects.all()
    paginate_by = 4
    paginator = Paginator(heron_list, paginate_by)

    # Read the ?page= query-parameter
    page = request.GET.get('page', 1)

    # Implement pagination ourselves (we need the values within our context,
    # but also if we add htmx driven filtering, the values will change within our context)
    try:
        heron_list = paginator.page(page)
    except PageNotAnInteger:
        # Default page is first
        heron_list = paginator.page(1)
    except EmptyPage:
        # Do not go past the last page
        heron_list = paginator.page(paginator.num_pages)

    return render(request, 'herons/heron_htmx_list.html', {
        # Pagination context, just like ListView provides
        'object_list': heron_list,
        'paginator': paginator,
        'page_obj': heron_list,
        'is_paginated': paginator.num_pages > 1,
        # Tell the template how it can find the htmx view that contains/refreshes the list data
        'htmx_list_url': reverse('herons:heron-htmx-list'),
    })


# One object, at http://<server>/herons/1/
class HeronDetailView(LoginRequiredMixin, DetailView):
    model = Heron


# Create a new object, at http://<server>/herons/new/
class HeronCreateView(LoginRequiredMixin, CreateView):
    model = Heron
    form_class = HeronForm


# Update object, at http://<server>/herons/1/update/
class HeronUpdateView(LoginRequiredMixin, UpdateView):
    model = Heron
    form_class = HeronForm


# Delete object, at http://<server>/herons/1/delete/
class HeronDeleteView(LoginRequiredMixin, DeleteView):
    model = Heron
    success_url = reverse_lazy('herons:heron-listview')


# API at http://localhost:8000/herons/api/herons/
class HeronViewSet(viewsets.ModelViewSet):
    serializer_class = HeronSerializer
    queryset = Heron.objects.all()
    # ZZZ: Not sure why yet, but all users seem to be able to Read
    # permission_classes = (HeronAccessPermissions,)
