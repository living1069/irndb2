from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
from django.views.generic.base import RedirectView
from django.views.static import serve

from irndb2 import views

urlpatterns = [
    url(r'home/$', views.home_method, name='home_url_name'),
    url(r'contact/$', views.contact_method, name='contact_url_name'),
    url(r'doc/$', views.doc_method, name='doc_url_name'),
    url(r'tables/$', views.tables_method, name='tables_url_name'),
    url(r'charts/$', views.charts_method, name='charts_url_name'),                   
    url(r'search/$', views.search_method, name='search_url_name'),
    url(r'browse/$', views.browse_method, name='browse_url_name'),
    url(r'browse-pw/$', views.browse_pw_method, name='browse_pw_url_name'),
    url(r'target/(?P<sym>[A-Za-z0-9\-\.]+)$', views.target_method, name='target_url_name'),
    url(r'mirna/(?P<name>[A-Za-z0-9\-\.]+)$', views.mirna_method, name='mirna_url_name'),
    url(r'lncrna/(?P<sym>[A-Za-z0-9\-\.]+)$', views.lncrna_method, name='lncrna_url_name'),
    url(r'pirna/(?P<name>[A-Za-z0-9\-\.]+)$', views.pirna_method, name='pirna_url_name'),
    # redirect non-matching urls to home/
    url(r'^.*$', RedirectView.as_view(url='home/', permanent=False), name='index'), 
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

