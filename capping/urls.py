from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('capping.views',
    # Examples:
    # url(r'^$', 'capping.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^test$', 'getClass'),
    (r'^$', 'homeView'),
    (r'^.*/$', 'homeView'),
)
