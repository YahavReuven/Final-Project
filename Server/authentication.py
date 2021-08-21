"""
Module used for the authentication of id's sent to the server from the client.
"""

from db import DBUtils
from consts import DatabaseType
from errors import DeviceNotFoundError, ProjectNotFoundError


# TODO: check docstring
def authenticate_device(device_id: str) -> bool:
    """
    Checks if a device with the given device_id is present in the database.

    Args:
        device_id (str): the device id of the desired device.

    Returns:
        True: if the device with the given device_id is present in the database.

    Raises:
        DeviceNotFoundError: if the is no device with the given device_id in the database.
    """

    device = DBUtils.find_in_db(device_id, DatabaseType.devices_db)
    if not device:
        raise DeviceNotFoundError

    return True



def authenticate_creator(device_id: str, project_id: str) -> bool:

    authenticate_device(device_id)

    device = DBUtils.find_in_db(device_id, DatabaseType.devices_db)

    for project in device.projects:
        if project.project_id == project_id:
            return True

    raise ProjectNotFoundError
