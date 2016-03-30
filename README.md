# README

## Installation
- Clone the repo:

```bash
git clone git@gitlab.com:s-schmeier/django-app-template.git YOUR_APP_NAME
```

- Remove the remote of the template:

```bash
cd YOUR_APP_NAME
git remote rm origin
```

- Add `YOUR_APP_NAME` in the main project `settings.py `:

```python
# settings.py
INSTALLED_APPS = (
        ...,
        'YOUR_APP_NAME',
)
```

- Add `YOUR_APP_NAME` to the main projects `urls.py`:

```python
# urls.py
urlpatterns = patterns('',
       ...,
       url(r'^apps/YOUR_APP_NAME/', include('YOUR_APP_NAME.urls', namespace="YOUR_APP_NAME")),
)
```

- Execute the `BOOTSTRAP.py` script, this wil replace in all files 'testapp' with 'YOUR_APP_NAME':

```bash
python BOOTSTRAP.py YOUR_APP_NAME
```

- Set up new git repo:

```bash
rm -r .git/
git init
git add .
git commit -m "Init."
git checkout -b develop
```
