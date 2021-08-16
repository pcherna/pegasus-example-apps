# Example Models for SaaS Pegasus

Here are example apps for [SaaS Pegasus](https://saaspegasus.com):

* **Frogs** uses Function-Based Views, and the objects are cross-team
* **Toads** uses Function-Based Views, and the objects are team-specific
* **Cheetahs** uses Class-Based Views, and the objects are cross-team
* **Tigers** uses Class-Based Views, and the objects are team-specific

Each app:

* Implements a model with a few sample fields (`Name`, `Number`, and `Notes`)
* Implements Function-Based Views for:
  * Create
  * List (summarize all objects, showing their `Name` and `Number`)
  * Details (details on one object, showing all their fields)
  * Update
  * Delete
* Implements a basic CRUD API using django-rest-framework

I chose names that don't appear anywhere in the Pegasus codebase, to make it easy to search/replace if you use these to build your own apps. **Frogs** is mnemonic for **F**unction-Based Views, and **Cheetahs** is mnemonic for **C**lass-Based Views. **Toads** and **Tigers** are mnemonic for **T**eam-specific, and are of course cousins to Frogs and Cheetahs.

## Installation

### Install the app files

Copy the following files and folders into your Pegasus project folder:

* `apps/teams/mixins.py`
* `apps/frogs` and `templates/frogs`
* `apps/toads` and `templates/toads`
* `apps/cheetahs` and `templates/cheetahs`
* `apps/tigers` and `templates/tigers`

### Integrate the new apps into your project

* In `<projectslug>/settings.py`:
  * To `PROJECT_APPS`, add:

```python
    'apps.frogs.apps.FrogsConfig',
    'apps.toads.apps.ToadsConfig',
    'apps.cheetahs.apps.CheetahsConfig',
    'apps.tigers.apps.TigersConfig',
```

* In `<projectslug>/urls.py`:
  * To `urlpatterns`, add:

```python
    path('frogs/', include('apps.frogs.urls')),
    path('cheetahs/', include('apps.cheetahs.urls')),
```

  * To `team_urlpatterns`, add:

```python
    path('toads/', include('apps.toads.urls')),
    path('tigers/', include('apps.tigers.urls')),
```

### Update your database

```bash
make migrations
make migrate
```

## Notes and Todos

Any and all comments and suggestions welcome. [peter@cherna.com](mailto:peter@cherna.com)

* I have a decent mixin for team-specific apps using Class Based Views (see `apps/teams/mixins`, but not everything is transparently solved. Looking to see if I can carry this further. I don't yet have a strategy for common team code for team-specific apps using Function Based Views.
* The API for Toads and Tigers does not yet handle team filtering and related logic.
* Only standard (Bulma) templates are currently supplied.
* I would like to add pagination support to the views
* There is an `UnorderedObjectListWarning` I haven't yet looked into, for team-specific CBVs
