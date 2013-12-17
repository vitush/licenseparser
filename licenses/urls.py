from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'licenses.views.home', name='home'),
    url(r'^$', 'main.views.index', name='index'),
    url(r'^manage/$', 'main.views.manage', name='manage'),
    url(r'^search/$', 'main.views.search', name='search'),
    url(r'^reload/$', 'main.views.reload', name='reload'),
    url(r'^load/$', 'main.views.load', name='load'),
    url(r'^download/$', 'main.views.download', name='download'),
    url(r'^appinfo/$', 'main.views.appinfo', name='appinfo'),
    url(r'^prices/$', 'main.views.prices', name='prices'),
    url(r'^update/$', 'main.views.update', name='update'),

    #url(r'^static/', document_root=settings.STATIC_ROOT),
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    #    {'document_root': settings.STATIC_ROOT, 'show_indexes': True }),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),



    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)            # + static(settings.STATIC_URL, document_root="/home/vitush/PycharmProjects/licenses/static")
              #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#urlpatterns += staticfiles_urlpatterns()


urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
           { 'document_root': '/licenses/staticfiles' }),
    )