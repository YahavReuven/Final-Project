"""
Module used to define constants.
"""

from datetime import timedelta
from enum import Flag, auto

PORT = 8000

DEVICES_DIRECTORY = 'devices'
DEVICES_DATABASE_NAME = 'devices_database.json'
DEVICES_DATABASE_KEY = 'devices'


PROJECTS_DIRECTORY = 'projects'
PROJECTS_DATABASE_NAME = 'projects_database.json'
ACTIVE_PROJECTS_DB_KEY = 'active'
FINISHED_PROJECTS_DB_KEY = 'finished'
WAITING_TO_RETURN_PROJECTS_DB_KEY = 'waiting'


PROJECT_STORAGE_PROJECT = 'project'
PROJECT_STORAGE_RESULTS = 'results'

PROJECT_STORAGE_JSON_PROJECT = 'project.json'

JSON_PROJECT_BASE64_SERIALIZED_CLASS = 'base64_serialized_class'
JSON_PROJECT_BASE64_SERIALIZED_ITERABLE = 'base64_serialized_iterable'
JSON_PROJECT_TASK_SIZE = 'task_size'


SENT_TASK_VALIDITY = timedelta(days=1)
SENT_TASK_DATE_KEY = 'sent_date'
DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S'


RETURNED_TASK_TEMP_ZIPPED_RESULTS_FILE = 'temp_results.zip'
RETURNED_TASK_RESULTS_DIRECTORY = 'results'
RETURNED_TASK_ADDITIONAL_RESULTS_DIRECTORY = 'additional_results'
RESULTS_FILE = 'results.json'

TEMP_PROJECT_ADDITIONAL_RESULTS_DIRECTORY = 'temp'
PROJECT_ADDITIONAL_RESULTS_DIRECTORY = 'results'


UPDATE_DB_DELAY = 60*0.1


class DatabaseType(Flag):
    devices_db = auto()
    active_projects_db = auto()
    finished_projects_db = auto()
    waiting_to_return_projects_db = auto()
    projects_db = (active_projects_db | finished_projects_db |
                   waiting_to_return_projects_db)




# class ProjectsDatabaseType(str, Enum):
#     active_projects_db = 'active_db'
#     waiting_to_return_projects_db = 'waiting_db'
#     finished_projects_db = 'finished_db'
#     all = 'all'






