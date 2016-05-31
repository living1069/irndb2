# IRNdb source ([irndb.org](http://irndb.org))

## Installation
- Clone the repo:

```bash
git clone git@github.com:sschmeier/irndb2.git irndb2
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
urlpatterns = [
       ...,
       url(r'^apps/irndb/', include('irndb2.urls', namespace="irndb2")),
]
```

- Get the data
- Load the data (look at 00README_data.txt)
