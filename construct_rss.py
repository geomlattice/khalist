import os

from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Attachment, Comment, Task
import sys

import convertdate
import pytz
import datetime


with open("api.token", "r") as key_in:
	api = TodoistAPI(str(key_in.readlines()[0].split('\n')[0]))

def comments_from_task_id(t_id):
	try:
		comments = api.get_comments(task_id=t_id)
		return [c for c in comments]
	except Exception as error:
		print(error)

def rss_item(nadi_stamp, mdlink, post_category):
  return f''' 
  <item>
    <title>{nadi_stamp}</title>
    <link>{mdlink}</link>
    <description>{post_category}</description>
  </item>

'''

def process_posts():
	pseudo_post_id = "8049968003"
	pseudo_posts = comments_from_task_id(pseudo_post_id)

	with open("./data/seen_posts.txt", "r") as postids_in:
		postid_lines = [l.split('\n')[0] for l in postids_in.readlines()]

	seen_postids = set()
	for postid in postid_lines:
		seen_postids.add(postid)
	xml_payload = ""
	new_posts = set()
	post_info = {}
	for pseudo_post in pseudo_posts:
		if pseudo_post.id not in seen_postids:
			new_posts.add(pseudo_post.id)
			date_info_e, time_info_e = pseudo_post.posted_at.split("T")
			gyear, gmonth, gday = date_info_e.split("-")
			lhour, lmin, lsec = time_info_e.split(".")[0].split(":")
			minutes_total = int(lhour)*60 + int(lmin)
			nadis = round(minutes_total / 24, 2)
			byear, bmonth, bday = convertdate.bahai.from_gregorian(int(gyear), int(gmonth), int(gday))
			nadistamp = str(nadis).replace(".","n") + "x" + str(bday) + str(bmonth) + str(bday) 
			marked_payload = ""
			marked_payload += f'''# {nadis} Nadis {bday} {bmonth} {byear}\n\n'''
			marked_payload += f'''{pseudo_post.content}\n'''
			markedout_path = "/posts/" + nadistamp + ".md"
			with open("." + markedout_path, "w") as marked_out:
				marked_out.write(marked_payload)
			post_category = pseudo_post.content.split("]")[0].split('[')[-1]
			siteurl = "https://geomlattice.github.io/khalist"
			xml_payload += rss_item(nadistamp, siteurl + markedout_path, post_category)

			#posts_info[pseudo_post.posted_at] = pseudo_post.content
	#take snapshot in case something odd happens 
	os.system("cp ./data/posts.xml ./data/posts.xml.snapshot")
	os.system("cp ./data/seen_posts.txt ./data/seen_posts.txt.snapshot")

	with open("./data/posts.xml", "r") as xml_in:
		xml_lines = [l.split('\n')[0] for l in xml_in.readlines()]
	
	#define with imaginary values until promoted	
	payload_prefix = "-1"
	payload_suffix = "-1"
	payload_construct = ""

	#search for end of feed
	for l_ind, line in enumerate(xml_lines):
		if "</channel>" in line:
			payload_prefix = xml_lines[:l_ind]
			payload_suffix = xml_lines[l_ind:]

	payload_construct += '\n'.join(payload_prefix)
	payload_construct += xml_payload
	payload_construct += "\n".join(payload_suffix)

	with open("./data/posts.xml", "w") as xml_out:
		xml_out.write(payload_construct + "\n")

	with open("./data/seen_posts.txt", "a") as posts_record:
		posts_record.write("\n".join(list(new_posts)) + "\n")

process_posts()
