import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Env variables for data access
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

SPIRE_TOKEN = os.getenv('SPIRE_TOKEN')
SPIRE_USER = os.getenv('SPIRE_USER')
SPIRE_PASSWORD = os.getenv('SPIRE_PASSWORD')

MB_USERNAME = os.getenv('USERNAME')
MB_ACCESS_TOKEN = os.getenv('MAPBOX_ACCESS_TOKEN')
MP_DATASET_ID = os.getenv('DATASET_ID')
NEW_DATA_FILE = os.getenv('NEW_DATA_FILE')

# input tables
NAME_TB_INPUT   = 'seaimpact.vessel_data_extract'            # Input schema.table


# boolean for including mmsi validation on run
is_validate_mmsi = False


