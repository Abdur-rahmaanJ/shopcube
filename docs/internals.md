

## Dashboard

Each dashboard template inherits from `base/module_base.html`


```
{% extends "base/module_base.html" %}
```

Then the sidebar_bgtrigger value is set to highlight the selected dashboard option

```
{% set sidebar_bgtrigger = 'category_home' %}
```

This is done using the sidebar block defined in `templates/base/blocks/macros.html`. It adds a `sidebar-color` class if they match. The `sidebar-color` css class is defined in `base/templates/base/blocks/resources.html`


The dashboard url is defined as the base module url. If the module url is `/fruit`, the dashboard will be
at `/fruit/` unless a `"dashboard": "<url>"` element is defined in the `info.json` file.
