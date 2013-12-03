from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'licenses.views.home', name='home'),
    url(r'^$', 'main.views.index', name='index'),
    url(r'^manage/$', 'main.views.manage', name='manage'),
    url(r'^search/$', 'main.views.search', name='search'),
    url(r'^reload/$', 'main.views.reload', name='reload'),
    url(r'^showsoft/$', 'main.views.showsoft', name='showsoft'),
    url(r'^showpcreport/$', 'main.views.showpcreport', name='showpcreport'),
    url(r'^download/$', 'main.views.download', name='download'),


    # url(r'^licenses/', include('licenses.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
