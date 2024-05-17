from rest_framework import serializers
from .models import Layer, Theme

class BriefLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layer
        fields = ('id', 'name', 'layer_type', 'url', 'opacity', 'vector_color', 'vector_fill', 'vector_outline_color', 'vector_outline_opacity', 'arcgis_layers')

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'

class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layer
        fields = '__all__'