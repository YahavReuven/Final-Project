"""
The main module of the client application.
"""
import os

from initialize_app import init_user, init_task_storage
from handle_users import switch_user
from worker import task_menu

#old_mask = os.umask(0o777)
user = init_user()
init_task_storage()
while True:
    action = input('please enter what action to take: ')
    if action == 'user':
        user = switch_user()
    if action == 'task':
        task_menu(user)
    if action == 'exit':
        break

#os.umask(old_mask)