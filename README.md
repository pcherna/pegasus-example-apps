# Example Models for SaaS Pegasus

Here are two example apps for [SaaS Pegasus](https://saaspegasus.com). They are called **Frogs** and **Toads**. Each app:

* Implements a model with a few sample fields (`Name`, `Number`, and `Notes`)
* Implements Function-Based Views for:
  * Create
  * List (summarize all objects, showing their `Name` and `Number`)
  * Details (details on one object, showing all fields)
  * Update
  * Delete
* Implements a basic CRUD API using django-rest-framework

The **Frogs** are accessible regardless of team. The **Toads** are team-specific.

I chose names that don't appear anywhere in the Pegasus codebase, to make it easy to search/replace if you use these to build your own apps. **Frogs** is mnemonic for **F**unction-Based Views, and **Toads** is mnemonic for **T**eam-specific.

## Installation

### Install the app files

Copy the following folders into your Pegasus project folder:

* `apps/frogs` and `templates/frogs`
* `apps/toads` and `templates/toads`

### Integrate the new apps into your project

* In `<projectslug>/settings.py`:
  * To `PROJECT_APPS`, add:

```python
    'apps.frogs.apps.FrogsConfig',
    'apps.toads.apps.ToadsConfig,'
```

* In `<projectslug>/urls.py`:
  * To `urlpatterns`, add:

```python
    path('frogs/', include('apps.frogs.urls')),
```

  * To `team_urlpatterns`, add:

```python
    path('toads/', include('apps.toads.urls')),
```

### Update your database

```bash
make migrations
make migrate
```

## Notes and Todos

This is the first working version. Any and all comments and suggestions welcome. [peter@cherna.com](mailto:peter@cherna.com)

* I hope to try building a Class-Based Views version.
* I plan to study how to factor the team-specific code into some kind of helper or mixin.
* The CRUD API for Toads does not yet handle team filtering and related logic.
* Only standard (Bulma) templates are currently supplied.
