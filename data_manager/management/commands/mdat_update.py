from django.core.management.base import BaseCommand
from data_manager.models import Layer, Theme
import requests

class Command(BaseCommand):
    help = "Run an update on MDAT layers"

    def handle(self, *args, **options):
        #theme object for mdat
        mdat = Theme.objects.all().filter(name='MDAT')[0]
        mdat_id = mdat.pk

        #allows initial endpoint url to be updated via a faux layer
        mdat_rest_path = Layer.objects.all().filter(name='MDAT', layer_type="placeholder")[0].url

        #grab all parent service directories for enpoint
        r = requests.get(mdat_rest_path+'MDAT?f=json')
        parent_json = r.json()
        mdat_dirs = parent_json['services']

        #loop through mdat service *parent* directory array
        for directory in mdat_dirs:
            print "***** Entering %s *****" % directory['name']
            #defaults for parent directories
            parent_defaults = { 
                'name':directory['name'], 
                'layer_type':'checkbox',
            }
            #does layer exist?
            try:
                obj = Layer.objects.get(themes=mdat, name=directory['name'])
            #create parent layer/directory - if not
            except Layer.DoesNotExist:
                print "***** Adding %s *****" % directory['name']
                obj = Layer.objects.create(**parent_defaults)
                obj.site = [1,2]
                obj.themes = [mdat_id]
                obj.save()

            #get pk for current layer
            layer_id = obj.pk

            #set path
            layer_path = mdat_rest_path+directory['name']+'/MapServer'

            #grab all layers of parent endpoint in the loop
            blob = requests.get(layer_path+'?f=json')
            layer_json = blob.json()
            mdat_layers = layer_json['layers']
            layer_url = layer_path + '/export'

            #loop through layers within parent directory array
            for layer in mdat_layers:
                print "***** Looping through %s *****" % layer['name']
                layer_defaults = {
                    'name':layer['name'],
                    'layer_type':'ArcRest',
                    'arcgis_layers':layer['id'],
                    'is_sublayer': 1,
                    'url':layer_url
                }

                try:
                    lyr = Layer.objects.get(themes=mdat, name=layer['name'], url=layer_url)
                #create layers of parent directory - if they don't exist
                except Layer.DoesNotExist:
                    print "***** Adding %s *****" % layer['name']
                    lyr = Layer.objects.create(**layer_defaults)
                    lyr.site = [1,2]
                    lyr.themes = [mdat_id]
                    lyr.sublayers = [layer_id]
                    lyr.save()
                    #sublayer fields need to be filled in for parent dir
                    obj.sublayers = [layer_id]
                    obj.save()


