from django.conf.urls import  url
from . import views
#from clickmuncher import views


urlpatterns = [
    #url(r"^$", views.akema_temp, name="akema_temp"),
    #url(r"^akema/$", views.inc, name="akema_temp"),
    #url('clicked-on-img/<str:value>/', views.function_url, name='lien'),
    url(r'^$',views.graphic,name="graphic"),
    #(r'^charts/simple.png$', 'myapp.views.charts.simple'),
]
