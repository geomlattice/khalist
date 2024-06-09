from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Attachment, Comment, Task
import sys

with open("api.token", "r") as key_in:
	api = TodoistAPI(str(key_in.readlines()[0].split('\n')[0]))

def tasks_from_proj_id(t_id):
	try:
		tasks = api.get_tasks(project_id=t_id)
		return [c.content for c in tasks]
	except Exception as error:
		print(error)

#This should be the filesystem anchor
print('\n'.join(tasks_from_proj_id(sys.argv[1])))
