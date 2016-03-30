from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
from django.views.generic.base import RedirectView

from irndb import views


urlpatterns = patterns('',
    url(r'home/$', views.home_method, name='home_url_name'),
    url(r'contact/$', views.contact_method, name='contact_url_name'),
    url(r'doc/$', views.doc_method, name='doc_url_name'),
    url(r'tables/$', views.tables_method, name='tables_url_name'),
    url(r'charts/$', views.charts_method, name='charts_url_name'),                   
    url(r'search/$', views.search_method, name='search_url_name'),
    url(r'browse/$', views.browse_method, name='browse_url_name'),
    # redirect non-matching urls to home/
    url(r'^.*$', RedirectView.as_view(url='home/', permanent=False), name='index'), 
)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

