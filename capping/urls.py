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
	(r'^api/test_major_req$','getMajorReqX'),
	(r'^api/get_majors$','getMajors'),
	(r'^api/get_all_internal_courses$','getAllInternalCourses'),
	(r'^api/get_all_external_courses$','getAllExternalCourses'),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
    url(r'^.*$', TemplateView.as_view(template_name='index.html'), name="home"),
)

