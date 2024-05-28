from django.core.management.base import BaseCommand
import sys, requests, os, json
from django.conf import settings

class Command(BaseCommand):
    help = "Import daily-built JSON for Native-Land.ca."

    def build_geojson_from_query(self, layer):
        print("---Attempting API for '{}'".format(layer))
        response = requests.get("https://native-land.ca/api/index.php?maps={}".format(layer))
        print("---Reading JSON from API...")
        features = json.loads(response.content)
        print("---Building GeoJSON from API Feature List")
        geojson = '{"type": "FeatureCollection","features": ['
        # for feature in features:
        #     if hasattr(feature, 'id'):
        #         del feature['id']
        geojson += ",".join([json.dumps(x) for x in features])
        geojson += "]}"
        print("---Writing GeoJSON to file...")
        with open(os.path.join(settings.MEDIA_ROOT, 'data_manager', 'nativeland', 'nld_{}.json'.format(layer)), "w") as out_file:
            out_file.write(geojson)
        print("--- API file created")


    def is_valid_geojson(self, layer_file):
        
        if os.path.isfile(layer_file):
            # I can't make a valid GeoJSON with at least one feature in less than 115 bytes
            if os.stat(layer_file).st_size > 100:
                try:
                    with open(layer_file) as f:
                        geojson = json.load(f)
                        if (
                            'type' in geojson.keys() and
                            'features' in geojson.keys() and
                            geojson['type'] == 'FeatureCollection' and
                            len(geojson['features']) > 0 and
                            'type' in geojson['features'][0].keys() and
                            geojson['features'][0]['type'] == 'Feature' and
                            'geometry' in geojson['features'][0].keys() and
                            'type' in geojson['features'][0]['geometry'].keys() and
                            'coordinates' in geojson['features'][0]['geometry'].keys() and
                            len(geojson['features'][0]['geometry']['coordinates']) > 0
                        ):
                            return True
                except Exception:
                    pass
        print("NOT VALID GEOJSON: {}".format(layer_file))
        return False

    def handle(self, *args, **options):
        
        # Attempt to scrape latest JSON
        from bs4 import BeautifulSoup as bs
        from shutil import copyfile
        
        from urllib.error import URLError

        territories_url = None
        languages_url = None
        treaties_url = None

        NLD_DATA_DIR = os.path.join(settings.MEDIA_ROOT, 'data_manager', 'nativeland')
        NLD_BACKUP_DIR = os.path.join(NLD_DATA_DIR, 'backups')

        print('Backing up old files...')
        for layer in ['territories', 'languages', 'treaties']:
            layer_file = os.path.join(NLD_DATA_DIR, 'nld_{}.json'.format(layer))
            if self.is_valid_geojson(layer_file):
                copyfile(layer_file, os.path.join(NLD_BACKUP_DIR, 'nld_{}.json'.format(layer)))

        print('Scraping API page for latest links...')
        nld_api_page = requests.get("https://native-land.ca/resources/api-docs/")
        content = bs(nld_api_page.content, 'html.parser')
        for link in content.find_all('a', href=True):
            if 'indigenousTerritories.json' in link.get('href') or 'Territories' == link.text:
                territories_url = link.get('href')
                print('Found: Territories link')
            if 'indigenousLanguages.json' in link.get('href') or 'Languages' == link.text:
                languages_url = link.get('href')
                print('Found: Languages link')
            if 'indigenousTreaties.json' in link.get('href') or 'Treaties' == link.text:
                treaties_url = link.get('href')
                print('Found: Treaties link')

        try:
            print('Downloading: Territories link')
            terr_file = requests.get(territories_url)
            with open(os.path.join(NLD_DATA_DIR, 'nld_territories.json'), 'wb') as outfile:
                outfile.write(terr_file.content)
        except Exception:
            print('Failed to download Territories. Attempting API...')
            self.build_geojson_from_query('territories')
        try:
            print('Downloading: Languages link')
            lang_file = requests.get(languages_url)
            with open(os.path.join(NLD_DATA_DIR, 'nld_languages.json'), 'wb') as outfile:
                outfile.write(lang_file.content)
        except Exception:
            print('Failed to download Languages. Attempting API...')
            self.build_geojson_from_query('languages')
        try:
            print('Downloading: Treaties link')
            treaties_file = requests.get(treaties_url)
            with open(os.path.join(NLD_DATA_DIR, 'nld_treaties.json'), 'wb') as outfile:
                outfile.write(treaties_file.content)
        except URLError:
            print('Failed to download Treaties. Attempting API...')
            self.build_geojson_from_query('treaties')

        print("COMPLETE")

        

                