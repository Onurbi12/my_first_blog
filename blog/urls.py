from django.conf.urls import url
from . import views


urlpatterns = [
    url(r"^post/([0-9]+)/edit/$", views.post_edit, name="post_edit"),
    url(r"^post/([0-9]+)/$", views.post_detail, name="post_detail"),
    url(r"^akema/$", views.akema_temp, name="akema_temp"),
    url(r"post/new/", views.post_new, name="post_new"),
    url(r"", views.post_list, name="post_list"),
]
