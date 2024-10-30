import os
DATA_MANAGER_BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_MANAGER_ADMIN = True

DATA_CATALOG_ENABLED = True

DATA_CATALOG_NAME_FIELD = 'title'

CATALOG_TECHNOLOGY = 'default'

CATALOG_SOURCE = None

ELASTICSEARCH_INDEX = 'metadata'

ELASTICSEARCH_SEARCH_FIELDS = [
    'title',
]

CATALOG_PROXY = ''

ESPIS_ENABLED = False

NATIVE_LAND_API_KEY = None #set this in local settings
