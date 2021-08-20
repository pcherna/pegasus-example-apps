# apps/teams/mixins.py

# To make a model team-specific:
# - Add the TeamModelMixin to your model class
# - In your model, add a get_absolute_url() that adds the team slug, e.g.:
#    def get_absolute_url(self):
#        return reverse('appname:model-detailview', kwargs={'team_slug': self.team.slug, 'pk': self.pk})
# To make the views for a team-specific model:
# - Add the LoginAndTeamRequiredMixin or TeamAdminRequiredMixin to each view class
# - In the delete-view, add a get_success_url() method which includes
#       kwargs={'team_slug': self.request.team.slug}
# - Update all references to your views to include the team slug as the first argument

from django.db import models
from django.contrib.auth.mixins import AccessMixin
from django.utils.decorators import method_decorator
from apps.teams.decorators import login_and_team_required, team_admin_required

from .roles import is_member, is_admin
from .models import Team


class TeamModelMixin(models.Model):
    """
    Abstract model for objects with a team relationship
    """
    team = models.ForeignKey(Team, verbose_name="Team",
        on_delete=models.DO_NOTHING, blank=False, null=False, editable=True)

    class Meta:
        abstract = True


class TeamObjectViewMixin(AccessMixin):
    """
    Abstract model for views with a team relationship
    """
    def get_context_data(self, *args, **kwargs):
        """Add team to the context, for use by templates."""
        context = super().get_context_data(*args, **kwargs)
        context['team'] = self.request.team
        return context

    def get_queryset(self):
        """Narrow queryset to only include objects of this team."""
        return self.model.objects.filter(team=self.request.team)

    def form_valid(self, form):
        form.instance.team = self.request.team
        return super().form_valid(form)

    # For deletion, it would be nice if we could override get_success_url to include
    #     kwargs={'team_slug': self.object.team.slug}
    # I don't yet know if that can be done with a mixin

    class Meta:
        abstract = True


class LoginAndTeamRequiredMixin(TeamObjectViewMixin):
    """
    Verify that the current user is authenticated and a member of the team.
    """

    @method_decorator(login_and_team_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TeamAdminRequiredMixin(TeamObjectViewMixin):
    """
    Verify that the current user is authenticated and admin of the team.
    """

    @method_decorator(team_admin_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
