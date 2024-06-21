# Example Models for SaaS Pegasus

## Use the New Version Instead!

An improved and expanded version is now available at <https://github.com/pcherna/pegasus-example-apps-v2>. Please see that version instead.

## Older version follows here

Here are example apps for [SaaS Pegasus](https://saaspegasus.com). You can use these to get your own apps, models, and views up and running easily.

* **Frogs** uses Function-Based Views, and the objects are cross-team
* **Toads** uses Function-Based Views, and the objects are team-specific
* **Polliwogs** are like Toads, but also implement Django-object permissions
* **Cheetahs** uses Class-Based Views, and the objects are cross-team
* **Tigers** uses Class-Based Views, and the objects are team-specific
* **Pumas** are like Tigers, but also implement Django-object permissions
* **Herons** are like Cheetahs, but use htmx to cleanly update the list when moving through pages of objects

Each app:

* Implements a model with several sample fields (`Name`, `Number`, and `Notes`)
* Implements views (either Function-Based or Class-Based) for:
  * Create
  * List (summarize all objects, showing their `Name` and `Number`, including pagination)
  * Details (details on one object, showing all their fields)
  * Update
  * Delete
* Implements a basic CRUD API using django-rest-framework

I chose names that don't appear anywhere in the Pegasus codebase, to make it easy to search/replace if you use these to build your own apps. I use mnemonics:

* **Frogs** is mnemonic for **F**unction-Based Views
* **Cheetahs** is mnemonic for **C**lass-Based Views
* **Toads** and **Tigers** are mnemonic for **T**eam-specific, and are of course cousins to Frogs and Cheetahs.
* **Polliwogs** and **Pumas** are mnemonic for **P**ermissions-based.
* **Herons** are mnemonic for "htmx"

## Installation

In the following instructions, replace `project_slug` with your project's name.

### Clone this repository

Clone this **pegasus-example-apps** repository into a folder next to your Pegasus project.

```bash
git clone git@github.com:pcherna/pegasus-example-apps.git
```

### Copy teams mixin into your Pegasus project

Copy `example_apps/teams/mixins.py` into Pegasus project folder at `apps/teams/mixins.py`

Note: Pegasus includes a mixins.py that is derived from this project, but for now you need to use the version included with this project.

### Copy Paginator into your Pegasus project

Copy `templates/web/components/paginator.html` into Pegasus project folder at `templates/web/components/paginator.html`
Copy `templates/web/components/htmx_paginator.html` into Pegasus project folder at `templates/web/components/htmx_paginator.html`

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

If you're using Celery you'll also need to do a similar thing in `project_slug/celery.py`:

```python
# add these lines after os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_slug.settings')
base_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(base_dir / 'pegasus-example-apps'))
```

### Integrate the new apps into your project

* In `project_slug/settings.py`, to `PROJECT_APPS`, add:

```python
    'example_apps.frogs.apps.FrogsConfig',
    'example_apps.toads.apps.ToadsConfig',
    'example_apps.polliwogs.apps.PolliwogsConfig',
    'example_apps.cheetahs.apps.CheetahsConfig',
    'example_apps.tigers.apps.TigersConfig',
    'example_apps.pumas.apps.PumasConfig',
    'example_apps.herons.apps.HeronsConfig',
```

* Also in `project_slug/settings.py`, to `TEMPLATES` `'DIRS'` key add:

```python
  BASE_DIR / 'pegasus-example-apps' / 'templates',
```

* In `project_slug/urls.py`, to `urlpatterns`, add:

```python
    path('frogs/', include('example_apps.frogs.urls')),
    path('cheetahs/', include('example_apps.cheetahs.urls')),
    path('herons/', include('example_apps.herons.urls')),
```

* Also in `project_slug/urls.py`, to `team_urlpatterns`, add:

```python
    path('toads/', include('example_apps.toads.urls')),
    path('polliwogs/', include('example_apps.polliwogs.urls')),
    path('tigers/', include('example_apps.tigers.urls')),
    path('pumas/', include('example_apps.pumas.urls')),
```

### Update your database

```bash
./manage.py makemigrations frogs toads polliwogs cheetahs tigers pumas herons
./manage.py migrate
```

## Notes and Todos

Any and all comments and suggestions welcome. [peter@cherna.com](mailto:peter@cherna.com)

* I have a decent mixin for team-specific apps using Class Based Views (see `apps/teams/mixins`, but not everything is transparently solved
* The API entry points for Team-specific apps (Toads, Tigers, Pumas) handles team-filtering and related logic, but I'd like to build a clean Mixin to handle that
* Only standard (Bulma) templates are currently supplied
* There is an `UnorderedObjectListWarning` I haven't yet looked into, for team-specific CBVs
* For Herons, the `?page=n` query-parameter in the URL drives the initial page, but is not updated when you move through the pages
