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


## Dev workflow
Pretty much similar to workflow at: [http://scottchacon.com/2011/08/31/github-flow.html](http://scottchacon.com/2011/08/31/github-flow.html)

Everything in `master` is deployable and should be deployed to production as soon as it it pushed to `origin/master`:

To work on a new feature (e.g. `new_feature`) branch of `master`:

```
git checkout -b new_feature
```


Make changes and add branch to `origin` if desired

```
git push origin new_feature
```

If `master` is going forward too much, merge `master` changes into feature branch (e.g. `new_feature`):

```
git checkout new_feature
git merge master
```


To deploy a branch (e.g. `new_feature`) involves merging it into `master`, bump version to `v1.2.5` and pushing `master` to `origin`, deploy on production hosts:

```
git checkout new_feature
fab github:version='v1.2.5',branch='new_feature'
# deploy to production
fab deploy
```


Once branch (e.g. `new_feature`) has been merged and is not longer required:

```
git branch -D new_feature
git push origin --delete new_feature
```