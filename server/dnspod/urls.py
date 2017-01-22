from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^api/token/', obtain_auth_token, name='api-token'),
    url(r'^api/domains/$', views.DomainList.as_view()),
    url(r'^api/domains/(?P<domain_id>[0-9]+)/$', views.DomainDetail.as_view()),
    url(r'^api/domains/(?P<domain_id>[0-9]+)/(?P<record_id>[0-9]+)/$', views.RecordDetail.as_view()),
    url(r'^api/', include(router.urls)),
]
