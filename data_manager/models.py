from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
#from sorl.thumbnail import ImageField

# From MARCO/utils.py
def get_domain(port=8010):
    try:
        #domain = Site.objects.all()[0].domain
        domain = Site.objects.get(id=SITE_ID).domain
        if 'localhost' in domain:
            domain = 'localhost:%s' %port
        # domain = 'http://' + domain
    except:
        domain = '..'
    #print domain
    return domain

class SiteFlags(object):#(models.Model):
    """Add-on class for displaying sites in the list_display
    in the admin.
    """
    def primary_site(self):
        return self.site.filter(id=1).exists()
    primary_site.boolean = True

    def preview_site(self):
        return self.site.filter(id=2).exists()
    preview_site.boolean = True

class ThemeSite(models.Model):
    theme = models.ForeignKey('Theme')
    site = models.ForeignKey(Site)

    class Meta:
        auto_created = True
        unique_together = ('theme', 'site')
        app_label = 'data_manager'

class Theme(models.Model, SiteFlags):
    site = models.ManyToManyField(Site, through=ThemeSite)
    display_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField(default=10, blank=True, null=True, help_text='input an integer to determine the priority/order of the layer being displayed (1 being the highest)')
    visible = models.BooleanField(default=True)
    header_image = models.CharField(max_length=255, blank=True, null=True)
    header_attrib = models.CharField(max_length=255, blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.URLField(max_length=255, blank=True, null=True)

    factsheet_thumb = models.CharField(max_length=255, blank=True, null=True)
    factsheet_link = models.CharField(max_length=255, blank=True, null=True)

    # not really using these atm
    feature_image = models.CharField(max_length=255, blank=True, null=True)
    feature_excerpt = models.TextField(blank=True, null=True)
    feature_link = models.CharField(max_length=255, blank=True, null=True)

    objects = CurrentSiteManager('site')
    all_objects = models.Manager()

    def url(self):
        from django.conf import settings
        if hasattr(settings, 'INITIAL_X'):
            initial_x = settings.INITIAL_X
        else:
            initial_x = -73.24
        if hasattr(settings, 'INITIAL_Y'):
            initial_y = settings.INITIAL_Y
        else:
            initial_y = 38.93
        if hasattr(settings, 'INITIAL_Z'):
            initial_z = settings.INITIAL_Z
        else:
            initial_z = 7
        if hasattr(settings, 'INITIAL_BASEMAP'):
            initial_basemap = settings.INITIAL_BASEMAP
        else:
            initial_basemap = "Ocean"
        id = self.id
        return '/visualize/#x=%d&y=%d&z=%d&logo=true&controls=true&basemap=%s&themes[ids][]=%s&tab=data&legends=false&layers=true' % (initial_x, initial_y, initial_z, initial_basemap, id)

    def __unicode__(self):
        return unicode('%s' % (self.name))

    def __str__(self):
        return self.display_name

    @property
    def learn_link(self):
        domain = get_domain(8000)
        return '%s/learn/%s' %(domain, self.name)

    @property
    def toDict(self):
        layers = [layer.id for layer in self.layer_set.filter(is_sublayer=False).exclude(layer_type='placeholder')]
        themes_dict = {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'learn_link': self.learn_link,
            'is_visible': self.visible,
            'layers': layers,
            'description': self.description
        }
        return themes_dict

    class Meta:
        app_label = 'data_manager'

class LayerSite(models.Model):
    layer = models.ForeignKey('Layer')
    site = models.ForeignKey(Site)

    class Meta:
        auto_created = True
        unique_together = ('layer', 'site')
        app_label = 'data_manager'

class Layer(models.Model, SiteFlags):
    TYPE_CHOICES = (
        ('XYZ', 'XYZ'),
        ('WMS', 'WMS'),
        ('ArcRest', 'ArcRest'),
        ('radio', 'radio'),
        ('checkbox', 'checkbox'),
        ('Vector', 'Vector'),
        ('placeholder', 'placeholder'),
    )
    site = models.ManyToManyField(Site, through=LayerSite)
    name = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField(default=10, blank=True, null=True, help_text='input an integer to determine the priority/order of the layer being displayed (1 being the highest)')
    slug_name = models.CharField(max_length=100, blank=True, null=True)
    layer_type = models.CharField(max_length=50, choices=TYPE_CHOICES, help_text='use placeholder to temporarily remove layer from TOC')
    url = models.CharField(max_length=255, blank=True, null=True)
    shareable_url = models.BooleanField(default=True, help_text='Indicates whether the data layer (e.g. map tiles) can be shared with others (through the Map Tiles Link)')
    arcgis_layers = models.CharField(max_length=255, blank=True, null=True, help_text='comma separated list of arcgis layer IDs')
    disable_arcgis_attributes = models.BooleanField(default=False, help_text='Click to disable clickable ArcRest layers')
    wms_slug = models.CharField(max_length=255, blank=True, null=True)
    wms_version = models.CharField(max_length=10, blank=True, null=True, help_text='WMS Versioning - usually either 1.1.1 or 1.3.0')
    is_sublayer = models.BooleanField(default=False)
    sublayers = models.ManyToManyField('self', blank=True)
    themes = models.ManyToManyField("Theme", blank=True)
    search_query = models.BooleanField(default=False, help_text='Select when layers are queryable - e.g. MDAT and CAS')
    has_companion = models.BooleanField(default=False, help_text='Check if this layer has a companion layer')
    connect_companion_layers_to = models.ManyToManyField('self', blank=True, help_text='Select which main layer(s) you would like to use in conjuction with this companion layer.')
    is_disabled = models.BooleanField(default=False, help_text='when disabled, the layer will still appear in the TOC, only disabled')
    disabled_message = models.CharField(max_length=255, blank=True, null=True)
    legend = models.CharField(max_length=255, blank=True, null=True, help_text='URL or path to the legend image file')
    legend_title = models.CharField(max_length=255, blank=True, null=True, help_text='alternative to using the layer name')
    legend_subtitle = models.CharField(max_length=255, blank=True, null=True)
    utfurl = models.CharField(max_length=255, blank=True, null=True)

    #tooltip
    description = models.TextField(blank=True, null=True)

    #data description (updated fact sheet) (now the Learn pages)
    data_overview = models.TextField(blank=True, null=True)
    data_source = models.CharField(max_length=255, blank=True, null=True)
    data_notes = models.TextField(blank=True, null=True)

    #data catalog links
    bookmark = models.CharField(max_length=755, blank=True, null=True, help_text='link to view data layer in the planner')
    kml = models.CharField(max_length=255, blank=True, null=True, help_text='link to download the KML')
    data_download = models.CharField(max_length=255, blank=True, null=True, help_text='link to download the data')
    learn_more = models.CharField(max_length=255, blank=True, null=True, help_text='link to view description in the Learn section')
    metadata = models.CharField(max_length=255, blank=True, null=True, help_text='link to view/download the metadata')
    source = models.CharField(max_length=255, blank=True, null=True, help_text='link back to the data source')
    map_tiles = models.CharField(max_length=255, blank=True, null=True, help_text='internal link to a page that details how others might consume the data')
    thumbnail = models.URLField(max_length=255, blank=True, null=True, help_text='not sure we are using this any longer...')

    #geojson javascript attribution
    EVENT_CHOICES = (
        ('click', 'click'),
        ('mouseover', 'mouseover')
    )
    attribute_fields = models.ManyToManyField('AttributeInfo', blank=True)
    compress_display = models.BooleanField(default=False)
    attribute_event = models.CharField(max_length=35, choices=EVENT_CHOICES, default='click')
    mouseover_field = models.CharField(max_length=75, blank=True, null=True, help_text='feature level attribute used in mouseover display')
    lookup_field = models.CharField(max_length=255, blank=True, null=True)
    lookup_table = models.ManyToManyField('LookupInfo', blank=True)
    is_annotated = models.BooleanField(default=False)
    vector_outline_color = models.CharField(max_length=7, blank=True, null=True)
    vector_outline_opacity = models.FloatField(blank=True, null=True)
    vector_color = models.CharField(max_length=7, blank=True, null=True)
    vector_fill = models.FloatField(blank=True, null=True)
    vector_graphic = models.CharField(max_length=255, blank=True, null=True)
    point_radius = models.IntegerField(blank=True, null=True, help_text='Used only for for Point layers (default is 2)')
    opacity = models.FloatField(default=.5, blank=True, null=True)

    objects = CurrentSiteManager('site')
    all_objects = models.Manager()

    def __unicode__(self):
        return unicode('%s' % (self.name))

    @property
    def is_parent(self):
        return self.sublayers.all().count() > 0 and not self.is_sublayer

    @property
    def parent(self):
        if self.is_sublayer:
            return self.sublayers.all()[0]
        return self

    def get_absolute_url(self):
        try:
            theme = self.themes.filter(visible=True).first()
            if theme:
                theme_url = reverse('portal.data_catalog.views.theme', args=[theme.name])
                if theme_url:
                    return "{0}#layer-info-{1}".format(theme_url, self.slug)
            return None
        except Exception as e:
            return None

    @property
    def slug(self):
        return slugify(self.name)

    @property
    def data_overview_text(self):
        if not self.data_overview and self.is_sublayer:
            return self.parent.data_overview
        else:
            return self.data_overview

    @property
    def data_source_text(self):
        if not self.data_source and self.is_sublayer:
            return self.parent.data_source
        else:
            return self.data_source

    @property
    def data_notes_text(self):
        if not self.data_notes and self.is_sublayer:
            return self.parent.data_notes
        else:
            return self.data_notes

    @property
    def bookmark_link(self):
        if self.bookmark:
            return self.bookmark

        if self.is_sublayer and self.parent.bookmark:
            return self.parent.bookmark.replace('<layer_id>', str(self.id))

        if self.is_parent:
            for theme in self.themes.all():
                return theme.url()

    @property
    def data_download_link(self):
        if self.data_download and self.data_download.lower() == 'none':
            return None
        if not self.data_download and self.is_sublayer:
            return self.parent.data_download
        else:
            return self.data_download

    @property
    def metadata_link(self):
        if self.metadata and self.metadata.lower() == 'none':
            return None
        if not self.metadata and self.is_sublayer:
            return self.parent.metadata
        else:
            return self.metadata

    @property
    def source_link(self):
        if self.source and self.source.lower() == 'none':
            return None
        if not self.source and self.is_sublayer:
            return self.parent.source
        else:
            return self.source

    @property
    def description_link(self):
        theme_name = self.themes.all()[0].name
        domain = get_domain(8000)
        return '%s/learn/%s#%s' %(domain, theme_name, self.slug)

    @property
    def tiles_link(self):
        if self.is_shareable and self.layer_type in ['XYZ', 'ArcRest', 'WMS']:
            domain = get_domain(8000)
            return self.slug
        return None

    @property
    def tooltip(self):
        if self.description and self.description.strip() != '':
            return self.description
        elif self.parent.description and self.parent.description.strip() != '':
            return self.parent.description
        else:
            return self.data_overview_text

    @property
    def is_shareable(self):
        if self.shareable_url == False:
            return False
        if self.parent and self.parent.shareable_url == False:
            return False
        return True

    def serialize_attributes(self):
        return {'compress_attributes': self.compress_display,
                'event': self.attribute_event,
                'attributes': [{'display': attr.display_name, 'field': attr.field_name, 'precision': attr.precision} for attr in self.attribute_fields.all().order_by('order')],
                'mouseover_attribute': self.mouseover_field }

    @property
    def serialize_lookups(self):
        return {'field': self.lookup_field,
                'details': [{'value': lookup.value, 'color': lookup.color, 'dashstyle': lookup.dashstyle, 'fill': lookup.fill, 'graphic': lookup.graphic} for lookup in self.lookup_table.all()]}

    @property
    def toDict(self):
        sublayers = [
            {
                'id': layer.id,
                'name': layer.name,
                'order': layer.order,
                'type': layer.layer_type,
                'url': layer.url,
                'arcgis_layers': layer.arcgis_layers,
                'disable_arcgis_attributes': layer.disable_arcgis_attributes,
                'wms_slug': layer.wms_slug,
                'wms_version': layer.wms_version,
                'utfurl': layer.utfurl,
                'parent': self.id,
                'legend': layer.legend,
                'legend_title': layer.legend_title,
                'legend_subtitle': layer.legend_subtitle,
                'description': layer.tooltip,
                'overview': layer.data_overview_text,
                'data_source': layer.data_source,
                'data_notes': layer.data_notes,
                'kml': layer.kml,
                'data_download': layer.data_download_link,
                'learn_more': layer.learn_more,
                'metadata': layer.metadata_link,
                'source': layer.source_link,
                'tiles': layer.tiles_link,
                'attributes': layer.serialize_attributes(),
                'lookups': layer.serialize_lookups,
                'outline_color': layer.vector_outline_color,
                'outline_opacity': layer.vector_outline_opacity,
                'point_radius': layer.point_radius,
                'color': layer.vector_color,
                'fill_opacity': layer.vector_fill,
                'graphic': layer.vector_graphic,
                'opacity': layer.opacity,
                'annotated': layer.is_annotated,
                'is_disabled': layer.is_disabled,
                'disabled_message': layer.disabled_message,
                'data_url': layer.get_absolute_url(),
                'has_companion': layer.has_companion
            }
            for layer in self.sublayers.all()
        ]
        connect_companion_layers_to = [
            {
                'id': layer.id,
                'name': layer.name,
                'order': layer.order,
                'type': layer.layer_type,
                'url': layer.url,
                'arcgis_layers': layer.arcgis_layers,
                'disable_arcgis_attributes': layer.disable_arcgis_attributes,
                'wms_slug': layer.wms_slug,
                'wms_version': layer.wms_version,
                'utfurl': layer.utfurl,
                'parent': self.id,
                'legend': layer.legend,
                'legend_title': layer.legend_title,
                'legend_subtitle': layer.legend_subtitle,
                'description': layer.tooltip,
                'overview': layer.data_overview_text,
                'data_source': layer.data_source,
                'data_notes': layer.data_notes,
                'kml': layer.kml,
                'data_download': layer.data_download_link,
                'learn_more': layer.learn_more,
                'metadata': layer.metadata_link,
                'source': layer.source_link,
                'tiles': layer.tiles_link,
                'attributes': layer.serialize_attributes(),
                'lookups': layer.serialize_lookups,
                'outline_color': layer.vector_outline_color,
                'outline_opacity': layer.vector_outline_opacity,
                'point_radius': layer.point_radius,
                'color': layer.vector_color,
                'fill_opacity': layer.vector_fill,
                'graphic': layer.vector_graphic,
                'opacity': layer.opacity,
                'annotated': layer.is_annotated,
                'is_disabled': layer.is_disabled,
                'disabled_message': layer.disabled_message,
                'data_url': layer.get_absolute_url(),
                'has_companion': layer.has_companion
            }
            for layer in self.connect_companion_layers_to.all()
        ]
        layers_dict = {
            'id': self.id,
            'name': self.name,
            'order': self.order,
            'type': self.layer_type,
            'url': self.url,
            'arcgis_layers': self.arcgis_layers,
            'disable_arcgis_attributes': self.disable_arcgis_attributes,
            'wms_slug': self.wms_slug,
            'wms_version': self.wms_version,
            'utfurl': self.utfurl,
            'subLayers': sublayers,
            'companion_layers': connect_companion_layers_to,
            'has_companion': self.has_companion,
            'queryable': self.search_query,
            'legend': self.legend,
            'legend_title': self.legend_title,
            'legend_subtitle': self.legend_subtitle,
            'description': self.description,
            'overview': self.data_overview,
            'data_source': self.data_source,
            'data_notes': self.data_notes,
            'kml': self.kml,
            'data_download': self.data_download_link,
            'learn_more': self.learn_more,
            'metadata': self.metadata_link,
            'source': self.source_link,
            'tiles': self.tiles_link,
            'attributes': self.serialize_attributes(),
            'lookups': self.serialize_lookups,
            'outline_color': self.vector_outline_color,
            'outline_opacity': self.vector_outline_opacity,
            'point_radius': self.point_radius,
            'color': self.vector_color,
            'fill_opacity': self.vector_fill,
            'graphic': self.vector_graphic,
            'opacity': self.opacity,
            'annotated': self.is_annotated,
            'is_disabled': self.is_disabled,
            'disabled_message': self.disabled_message,
            'data_url': self.get_absolute_url()
        }
        return layers_dict

    def save(self, *args, **kwargs):
        self.slug_name = self.slug
        super(Layer, self).save(*args, **kwargs)

    class Meta:
        app_label = 'data_manager'

class AttributeInfo(models.Model):
    display_name = models.CharField(max_length=255, blank=True, null=True)
    field_name = models.CharField(max_length=255, blank=True, null=True)
    precision = models.IntegerField(blank=True, null=True)
    order = models.IntegerField(default=1)

    def __unicode__(self):
        return unicode('%s' % (self.field_name))

    class Meta:
        app_label = 'data_manager'

class LookupInfo(models.Model):
    DASH_CHOICES = (
        ('dot', 'dot'),
        ('dash', 'dash'),
        ('dashdot', 'dashdot'),
        ('longdash', 'longdash'),
        ('longdashdot', 'longdashdot'),
        ('solid', 'solid')
    )
    value = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=7, blank=True, null=True)
    dashstyle = models.CharField(max_length=11, choices=DASH_CHOICES, default='solid')
    fill = models.BooleanField(default=False)
    graphic = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return unicode('%s' % (self.value))

    class Meta:
        app_label = 'data_manager'


class DataNeed(models.Model):
    name = models.CharField(max_length=100)
    archived = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.CharField(max_length=255, blank=True, null=True)
    expected_date = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    themes = models.ManyToManyField("Theme", blank=True)

    @property
    def html_name(self):
        return self.name.lower().replace(' ', '-')

    def __unicode__(self):
        return unicode('%s' % (self.name))

    class Meta:
        app_label = 'data_manager'
