from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Attachment, Comment, Task
import sys

with open("api.token", "r") as key_in:
	api = TodoistAPI(str(key_in.readlines()[0].split('\n')[0]))

def comments_from_task_id(t_id):
	try:
		comments = api.get_comments(task_id=t_id)
		return [c.content for c in comments]
	except Exception as error:
		print(error)

#This should be the filesystem anchor
print('\n\n'.join(comments_from_task_id(sys.argv[1])))
