from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('capping.views',
    (r'^admin/', include(admin.site.urls)),
    (r'^api/external$', 'getExternalClass'),
    (r'^api/internal$', 'getInternalClass'),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
    url(r'^.*$', TemplateView.as_view(template_name='index.html'), name="home"),
)
