import time
import base64
from collections.abc import Iterable
import json

import requests
import dill

import consts
from errors import ParallelFunctionNotFound
from utils import validate_user_name, create_path_string


class Distribute:
    def __init__(self, user_name: str, iterable: Iterable, task_size: int):
        self.user_name = user_name
        validate_user_name(self.user_name)
        self.iterable = iterable
        self.task_size = task_size

    def __call__(self, cls):
        print('in __call__ decorator factory')
        return self.Decorator(cls, self.user_name, self.iterable, self.task_size)



    class Decorator:

        def __init__(self, cls, user_name, iterable: Iterable, task_size: int):
            self.cls = cls
            self.user_name = user_name
            self.iterable = iterable
            self.task_size = task_size

            self._check_parallel_function()

        def __call__(self):
            """
            Requests the server to create a new project.

            Returns:
                An instance of the decorator

            """
            self.device_id = self._get_device_id(self.user_name)
            serialized_class = dill.dumps(self.cls)
            serialized_iterable = dill.dumps(self.iterable)

            encoded_class = base64.b64encode(serialized_class).decode('utf-8')
            encoded_iterable = base64.b64encode(serialized_iterable).decode('utf-8')
            self.project = requests.post('http://127.0.0.1:8000/upload_new_project',
                                     json={'creator_id': self.device_id,
                                           'task_size': self.task_size,
                                           'base64_serialized_class': encoded_class,
                                           'base64_serialized_iterable': encoded_iterable})
            print(self.project.text[1:-1])

            # TODO: deal with imports
            print(1)
            return self

        def _check_parallel_function(self):
            """
            Checks if a parallel function is present in the given class.

            Raises:
                ParallelFunctionNotFound: if a parallel function is not
                    present in the class.
            """
            for attribute in dir(self.cls):
                if callable(attribute) and not attribute.startswith("__"):
                    if attribute == consts.PARALLEL_FUNCTION_NAME:
                        return
            raise ParallelFunctionNotFound

        def _get_device_id(self, user_name: str) -> str:
            data_file_path = create_path_string(consts.USERS_DIRECTORY, self.user_name,
                                                consts.JSON_EXTENSION)

            with open(data_file_path, 'r') as file:
                data = json.load(file)

            return data[consts.DATA_DEVICE_ID_KEY]


        def get_results(self):
            """
            Once called, the function requests the project's results from the server.

            Note:
                  The function blocks until the results are received.
                  This function shouldn't be called until the results are required.

            Returns:
                dict {iteration_number: result}: a dictionary containing the results with
                their corresponding iteration number.

            """
            # results = None
            # i = 0
            # while not results:
            #     if i == 10:
            #         results = 1
            #         break
            #     print('asking server')
            #
            #     time.sleep(1)
            #     i += 1
            # print("done asking server")
            # return results

            results = None
            while not results:
                response = requests.get(f'http://127.0.0.1:8000/get_project_results?device_id={self.device.text[1:-1]}&project_id={self.project.text[1:-1]}')
                results = response.text
                time.sleep(1)
            print("done asking server")
            return results


# @Distribute(range(100), 10)
# class A:
#     @staticmethod
#     def a():
#         return 'a'
#
#     @staticmethod
#     def b():
#         return 'b'
#
#
# # A = Distribute(range(100), 10)(A)
# project = A()
# project.get_results()


# import os
# import json
# import base64
#
# returned_project = json.loads(c)
# temp_results_file = './results.zip'
# results_path = './results'
# os.makedirs(results_path, exist_ok=True)
# with open(temp_results_file, 'wb') as file:
#     file.write(base64.b64decode(returned_project['base64_zipped_additional_results']))
# with zipfile.ZipFile(temp_results_file) as zip_file:
#     zip_file.extractall(results_path)
