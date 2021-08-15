# To make a model team-specific:
# - Add the TeamModelMixin to your model classs
# To make the views for a team-specific model:
# - Add the LoginAndTeamRequiredMixin or TeamAdminRequiredMixin to each view class
# - In the create-view class, add a form_valid() method which sets form.instance.team = self.request.team
# - In the delete-view, add a get_success_url() method which includes kwargs={'team_slug': self.request.team_slug}

from django.db import models
from django.contrib.auth.mixins import AccessMixin
from django.http.response import Http404, HttpResponseForbidden

# apps/teams/mixins.py

from .roles import user_can_access_team, user_can_administer_team
from .models import Team

class TeamModelMixin(models.Model):
    """
    Abstract model for objects with a team relationship
    """
    team = models.ForeignKey(Team, verbose_name="Team",
        on_delete=models.DO_NOTHING, blank=False, null=False, editable=True)

    class Meta:
        abstract = True


class TeamAccessMixin(AccessMixin):
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

    # For deletion, it would be nice if we could override get_success_url to include
    #     kwargs={'team_slug': self.object.team.slug}
    # I don't yet know if that can be done with a mixin

    class Meta:
        abstract = True

def team_view_dispatch(permission_test_function, request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        raise HttpResponseForbidden
    else:
        if 'team_slug' in kwargs:
            team_slug = kwargs['team_slug']
            team = Team.objects.get(slug=team_slug)
            if team:
                if permission_test_function(user, team):
                    request.team = team
                    request.team_slug = team_slug
                    request.session['team'] = team.id  # set in session for other views to access
                    return
    raise Http404

class LoginAndTeamRequiredMixin(TeamAccessMixin):
    """Verify that the current user is authenticated and a member of the team."""
    def dispatch(self, request, *args, **kwargs):
        team_view_dispatch(user_can_access_team, request, *args, **kwargs)
        return super().dispatch(request, request.team_slug, *args, **kwargs)

class TeamAdminRequiredMixin(TeamAccessMixin):
    """Verify that the current user is authenticated and admin of the team."""
    def dispatch(self, request, *args, **kwargs):
        team_view_dispatch(user_can_administer_team, request, *args, **kwargs)
        return super().dispatch(request, request.team_slug, *args, **kwargs)

