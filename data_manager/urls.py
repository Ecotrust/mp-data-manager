from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'layers', views.LayerViewSet)

urlpatterns = [
    # url(''),
    url(r'^api/', include(router.urls)),
    url(r'^layer/([A-Za-z0-9_-]+)$', views.update_layer),
    url(r'^layer$', views.create_layer),
    url(r'^get_json$', views.get_json),
]
