"""
Module used to handle all the actions needed for a worker.
"""
#import importer
import importlib

import base64
import dill

from handle_requests import request_get_new_task, request_upload_task_results
from handle_users_data import UsersDataHandler

from itertools import islice

from worker_utils import (has_stop_function, results_to_file, get_results, has_additional_results,
                          get_zip_additional_results, get_task_cls, get_task_iterable,
                          init_task_result_storage, clean_results_directory)
import consts
from consts import ReturnTypes
from data_models import ReceivedTask, ReturnedTask



def execute_task(user: UsersDataHandler):
    return_type = TaskExecUtils.run_task_code(user)
    response = TaskExecUtils.return_task(user, return_type)
    clean_results_directory()
    return response

# def decorator(func):
#     def foo(*args, **kwargs):
#         math = importlib.import_module('math')
#         globals().update({'math': math})
#         func(*args, **kwargs)
#     return foo

class TaskExecUtils:

    task = None

    @classmethod
    def run_task_code(cls, user: UsersDataHandler):
        cls.task = request_get_new_task(user.user.ip, user.user.port, user.user.device_id)

        # load the necessary code
        # parallel_cls = get_task_cls(cls.task)
        parallel_cls = cls.task.base64_serialized_class
        parallel_cls = base64.b64decode(parallel_cls)
        # parallel_cls.__module__ = '__main__'
        parallel_cls = dill.loads(parallel_cls)
        # parallel_cls.parallel_func = decorator(parallel_cls.parallel_func)
        # parallel_cls.__module__ = 'worker'
        # print(parallel_cls.__module__)

        iterable = get_task_iterable(cls.task)

        # init the task storage for the results
        init_task_result_storage()

        # TODO: maybe move to server
        # slice the iterable
        start = cls.task.task_number * cls.task.task_size
        end = start + cls.task.task_size
        iterable = islice(iterable, start, end)

        # TODO: maybe add has_parallel_function
        # TODO: maybe change to try - more pythonic?
        has_stop_func = has_stop_function(parallel_cls)

        iteration_index = start
        results = {}

        # mod = ['math']
        # for i in mod:
        #     b = importlib.import_module(i)
        #     globals().update({i: b})
        # print(globals())
        #
        # func = getattr(parallel_cls, consts.PARALLEL_FUNCTION_NAME)
        fn = parallel_cls.parallel_func

        for i in parallel_cls.modules:
            module = importlib.import_module(i)
            fn.__globals__.update({i: module})

        for param_value in iterable:
            return_value = fn(param_value)
            # return_value = parallel_cls.parallel_func(param_value)
            if has_stop_func:
                write_result = getattr(parallel_cls, consts.STOP_FUNCTION_NAME)(return_value)
                if write_result:
                    # TODO: maybe write to an object and write to the file at the end
                    # TODO: maybe create a designd object for result
                    results[iteration_index] = return_value
                    results_to_file(results)
                    return ReturnTypes.stopped
                iteration_index += 1
                continue

            results[iteration_index] = return_value
            iteration_index += 1

        results_to_file(results)

        if iteration_index < end - 1:
            return ReturnTypes.exhausted

        return ReturnTypes.normal

    # TODO: handle response
    @classmethod
    def return_task(cls, user: UsersDataHandler, return_type: ReturnTypes):

        returned_task = ReturnedTask(worker_id=user.user.device_id, project_id=cls.task.project_id,
                                     task_number=cls.task.task_number, results=get_results())

        if has_additional_results():
            returned_task.base64_zipped_additional_results = get_zip_additional_results()

        if return_type == ReturnTypes.stopped:
            returned_task.stop_called = True
        elif return_type == ReturnTypes.exhausted:
            returned_task.is_exhausted = True

        return request_upload_task_results(user.user.ip, user.user.port, returned_task)
