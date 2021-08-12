from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse


class ServerError(Exception):
    """Error raised for a general error in the server"""
    message = 'internal server error'
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR


class BadRequestError(ServerError):
    """Error raised when a bad request is received"""
    message = 'bad request'
    status_code = HTTPStatus.BAD_REQUEST


class IDNotFoundError(BadRequestError):
    """Error raised if the received ID is not present in the database."""
    message = 'id not found'


class DeviceNotFoundError(IDNotFoundError):
    """Error raised if the received device id is not present in devices database."""
    message = 'device not found'
    pass


class ProjectNotFoundError(IDNotFoundError):
    """Error raised if the received project id is not present in projects database."""
    message = 'project not found'


class ProjectFinishedError(ProjectNotFoundError):
    """Error raised if a client tries to upload a new task to an already finished project."""
    message = 'project is finished'


class UnnecessaryTaskError(ProjectFinishedError):
    """Error raised if a client tries to upload a task which is no longer needed
    (mainly do to a stop number being set)"""
    message = 'task is no longer needed'


class WorkerNotAuthenticatedError(IDNotFoundError):
    """Error raised if a worker is not authenticated to upload results to the task"""
    message = 'worker is not authenticated'


async def handle_server_error(request: Request, exc: ServerError) -> JSONResponse:

    return JSONResponse(status_code=exc.status_code,
                        content={'message': exc.message})

