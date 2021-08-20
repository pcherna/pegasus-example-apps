# Example Models for SaaS Pegasus

Here are example apps for [SaaS Pegasus](https://saaspegasus.com). You can use these to get your own apps, models, and views up and running easily.

* **Frogs** uses Function-Based Views, and the objects are cross-team
* **Toads** uses Function-Based Views, and the objects are team-specific
* **Cheetahs** uses Class-Based Views, and the objects are cross-team
* **Tigers** uses Class-Based Views, and the objects are team-specific

Each app:

* Implements a model with several sample fields (`Name`, `Number`, and `Notes`)
* Implements views (either Function-Based or Class-Based) for:
  * Create
  * List (summarize all objects, showing their `Name` and `Number`)
  * Details (details on one object, showing all their fields)
  * Update
  * Delete
* Implements a basic CRUD API using django-rest-framework

I chose names that don't appear anywhere in the Pegasus codebase, to make it easy to search/replace if you use these to build your own apps. **Frogs** is mnemonic for **F**unction-Based Views, and **Cheetahs** is mnemonic for **C**lass-Based Views. **Toads** and **Tigers** are mnemonic for **T**eam-specific, and are of course cousins to Frogs and Cheetahs.

## Installation

In the following instructions, replace `project_slug` with your project's name.

### Clone this repository

Clone this **pegasus-example-apps** repository into a folder next to your Pegasus project.

```bash
git clone git@github.com:pcherna/pegasus-example-apps.git
```

### Copy teams mixin into your Pegasus project

Copy `example_apps/teams/mixins.py` into Pegasus project folder at `apps/teams/mixins.py`

(This mixin will be included in a future Pegasus release).

### Update your Python path

So that your Pegasus project can find the **pegasus-example-apps**, add the following your Pegasus project's `manage.py`:

```python
# Add this after import sys
from pathlib import Path
...
# Add this after the os.environ.setdefault(...) statement
# You can map this wherever you cloned the repository.
base_dir = Path(__file__).resolve().parent
sys.path.append(str(base_dir / 'pegasus-example-apps'))
```

If you're using Celery you'll also need to do a similar thing in `<project_slug>/celery.py`:

```python
# add these lines after os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wedding_plan.settings')
base_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(base_dir / 'pegasus-example-apps'))
```

### Integrate the new apps into your project

* In `project_slug/settings.py`, to `PROJECT_APPS`, add:

```python
    'example_apps.frogs.apps.FrogsConfig',
    'example_apps.toads.apps.ToadsConfig',
    'example_apps.cheetahs.apps.CheetahsConfig',
    'example_apps.tigers.apps.TigersConfig',
```

* Also in `project_slug/settings.py`, to `TEMPLATES` `'DIRS'` key add:

```python
  BASE_DIR / 'pegasus-example-apps' / 'templates',
```

* In `project_slug/urls.py`, to `urlpatterns`, add:

```python
    path('frogs/', include('example_apps.frogs.urls')),
    path('cheetahs/', include('example_apps.cheetahs.urls')),
```

* Also in `project_slug/urls.py`, to `team_urlpatterns`, add:

```python
    path('toads/', include('example_apps.toads.urls')),
    path('tigers/', include('example_apps.tigers.urls')),
```

### Update your database

```bash
./manage.py makemigrations frogs toads cheetahs tigers
./manage.py migrate
```

## Notes and Todos

Any and all comments and suggestions welcome. [peter@cherna.com](mailto:peter@cherna.com)

* I have a decent mixin for team-specific apps using Class Based Views (see `apps/teams/mixins`, but not everything is transparently solved. Looking to see if I can carry this further. I don't yet have a strategy for common team code for team-specific apps using Function Based Views.
* The API for Toads and Tigers does not yet handle team filtering and related logic.
* Only standard (Bulma) templates are currently supplied.
* I would like to add pagination support to the views
* There is an `UnorderedObjectListWarning` I haven't yet looked into, for team-specific CBVs
