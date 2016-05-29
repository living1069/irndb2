# README

## Installation
- Clone the repo:

```bash
git clone git@gitlab.com:s-schmeier/irndb2.git irndb2
```

- Add `irndb2` in the main project `settings.py `:

```python
# settings.py
INSTALLED_APPS = (
        ...,
        'irndb2',
)
```

- Add `irndb2` to the main projects `urls.py`:

```python
# urls.py
urlpatterns = patterns('',
       ...,
       url(r'^apps/irndb/', include('irndb2.urls', namespace="irndb2")),
)
```

