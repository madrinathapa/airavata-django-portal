from django.conf.urls import url
from . import views

app_name ='dashboard'

urlpatterns = [
    # /dashboard/
    # url(r'^$', views.index, name='index'),
    #url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^$', views.index, name="index"),
    # /dashboard/reviewer
   url(r'^reviewer/$', views.ReviewerView, name='reviewer'),


    # /dashboard/admin
    url(r'^admin/$', views.admin, name='admin'),

    # /dashboard/admin/141
    url(r'^admin/request-view/$', views.AdminRequestView, name='admin-request-view'),

    # /dashboard/reviewer/141
    url(r'^reviewer/request-view/$', views.ReviewerRequestView, name='reviewer-request-view'),

    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # /dashboard/712/
    # url(r'^(?P<request_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),


    # /dashboard/request/add
    url(r'^request/add/$', views.requestCreate, name='request-add'),

    # /dashboard/request/2/
    url(r'^request/(?P<pk>[0-9]+)/$', views.RequestUpdate.as_view(), name='request-update'),

    # /dashboard/request/2/delete/
    url(r'^request/(?P<pk>[0-9]+)/delete/$', views.RequestDelete.as_view(), name='request-delete'),
]