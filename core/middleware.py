from datetime import datetime
from pymongo import MongoClient
from django.contrib.auth.signals import user_logged_in
import os

# TODO there is a problem here
print("before client connection")
client = MongoClient('mongodb://host.docker.internal:27017/')
print("client connection done")
print(client)
db = client['admin_activity_db']
print(f"DATABASE ITEMS: {db}")


class AdminActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        user_logged_in.connect(self.handle_user_logged_in)

    def __call__(self, request):
        print(f"REQUEST: {request}")
        if '/admin/' in request.path and not request.method == "GET":
            if '/delete' in request.path:
                # deleted_ids = os.path.split(os.path.split(request.path)[0])[2]
                second_path, action = os.path.split(os.path.split(request.path)[0])
                delete_id = os.path.split(second_path)[1]
                user_id = request.user.id if request.user.is_authenticated else 'Anonymous'
                activity = {
                    'user_id': user_id,
                    'action': action,
                    'path': request.path,
                    'deleted_ids': delete_id,
                    'time': str(datetime.utcnow())
                }
                print(f'before inserting:\n{activity}')
                db['admin_activity'].insert_many([activity, ])
                print("insertion complete")
            elif request.POST.get('title'):
                user_id = request.user.id if request.user.is_authenticated else 'Anonymous'
                action = "created an item" if not os.path.split(os.path.split(request.path)[0])[1] == "change" \
                    else "modified and item"
                activity = {
                    'user_id': user_id,
                    'action': action,
                    'task_name': request.POST.get('title'),
                    'assigned_to': request.POST.get('user'),
                    'path': request.path,
                    'time': str(datetime.utcnow())
                }
                print(f'before inserting:\n{activity}')
                db['admin_activity'].insert_many([activity, ])
                print("insertion complete")
            elif request.POST.get('action') and request.POST.get('post'):
                action = request.POST.get('action')
                user_id = request.user.id if request.user.is_authenticated else 'Anonymous'
                action_on_ids = request.POST.getlist('_selected_action') or []
                activity = {
                    'user_id': user_id,
                    'action': action,
                    'action_on_ids': action_on_ids,
                    'path': request.path,
                    'time': str(datetime.utcnow())
                }
                print(f'before inserting:\n{activity}')
                db['admin_activity'].insert_many([activity, ])
                print("insertion complete")

            # activity = {
            #     'user_id': user_id,
            #     'action': action,
            #     'path': request.path,
            #     'time': str(datetime.utcnow())
            # }

            print(f"REQUEST POST: {request.POST}")

        response = self.get_response(request)
        return response

    def handle_user_logged_in(self, sender, user, request, **kwargs):
        # Code to be executed after a user is successfully logged in
        print(f"Login Detected for user {user.id}")
        user_id = user.id
        activity = {
            'user_id': user_id,
            'action': "Logged In",
            'path': request.path,
            'time': str(datetime.utcnow())
        }
        db['admin_activity'].insert_many([activity, ])
        # Do something with the user_id, such as logging it or storing it in a database
