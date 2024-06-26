# from django.conf.urls import url, include, patterns
from django.urls import path, re_path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'layers', views.LayerViewSet)

urlpatterns = [
    #'',
    re_path(r'^nested_admin/', include('nested_admin.urls')),
    re_path(r'^api/', include(router.urls)),
    re_path(r'^layer/([A-Za-z0-9_-]+)$', views.update_layer),
    re_path(r'^layer$', views.create_layer),
    re_path(r'^get_json$', views.get_json),
    re_path(r'^get_themes$', views.get_themes),
    re_path(r'^get_layer_search_data$', views.get_layer_search_data),
    re_path(r'^get_layers_for_theme/(?P<themeID>\d+)$', views.get_layers_for_theme),
    re_path(r'^get_layer_details/(?P<layerID>\d+)$', views.get_layer_details),
    re_path(r'^wms_capabilities', views.wms_request_capabilities),
    re_path(r'^get_layer_catalog_content/(?P<layerID>\d+)/$', views.get_layer_catalog_content),
    re_path(r'^get_catalog_records', views.get_catalog_records),
    re_path(r'^get_portal_catalog_map', views.get_portal_catalog_map),
    re_path(r'^migration/layer_status', views.layer_status),
    re_path(r'^migration/layer_details', views.migration_layer_details),
    path('migration/get_layer_details/<str:uuid>/', views.migration_layer_details),
    re_path(r'^migration/merge_layer', views.migration_merge_layer_request),

]
