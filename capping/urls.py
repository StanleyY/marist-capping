from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('capping.views',
    (r'^admin/', include(admin.site.urls)),
    (r'^api/external$', 'getExternalClass'),
    (r'^api/internal$', 'getInternalClass'),
    (r'^api/get_external_data$', 'getMappedExternalData'),
    (r'^api/get_marist_equal$', 'getMaristEqual'),
    (r'^api/get_major_req$', 'getMajorReq'),
    (r'^api/get_pdf$', 'getPDF'),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
    url(r'^.*$', TemplateView.as_view(template_name='index.html'), name="home"),
)

