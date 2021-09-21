"""
The main module of the client application.
"""

from initialize_app import init_user, init_task_storage
from handle_users import switch_user
from worker import execute_task

user = init_user()
init_task_storage()
while True:
    action = input('please enter what action to take: ')
    if action == 'user':
        user = switch_user()
    if action == 'task':
        execute_task(user)