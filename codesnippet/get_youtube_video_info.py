#!/usr/bin/python

import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow





#################  Configure your parameters here ########################
channels_list = {
'UCumyHvydNZ0lnLbdPQWecpw':'NBA Now',
}

playlist_list = {
'PLn3nHXu50t5zRhQRkdA_oxjaM50RUWuIO':'NBA on ESPN',
# 'PLn3nHXu50t5xwhC4Yhun5TWwTmo-bq8r1':'ESPN First Take (Very Good)',
}

CLIENT_SECRETS_FILE = "client_secrets.json"
##########################################################################



# This OAuth 2.0 access scope allows for full read/write access to the authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the APIs Console
https://console.developers.google.com

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),  CLIENT_SECRETS_FILE))





# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))



def list_playlist_videos(youtube, playlist_id):
	playlistitems_list_request = youtube.playlistItems().list(playlistId=playlist_id, part="snippet,contentDetails", maxResults=50)
	with open('./res.csv', 'a') as resFile:
		while playlistitems_list_request:
			playlistitems_list_response = playlistitems_list_request.execute()
			# Print information about each video.
			for playlist_item in playlistitems_list_response["items"]:
				# print(playlist_item)
				channel_title = playlist_item["snippet"]["channelTitle"]
				playlist_id   = playlist_item["snippet"]["playlistId"]
				title         = playlist_item["snippet"]["title"]
				video_id      = playlist_item["snippet"]["resourceId"]["videoId"]
				publishdate   = playlist_item["contentDetails"]["videoPublishedAt"]
				video_request = youtube.videos().list(part="snippet,contentDetails,status", id=video_id).execute()
				duration      = video_request["items"][0]["contentDetails"]["duration"]
				license       = video_request["items"][0]["status"]["license"]
				resFile.write('"'+channel_title+'","'+playlist_id+'","'+video_id+'","'+publishdate+'","'+duration+'","'+license+'","'+title+'"\n')
				print('"'+channel_title+'","'+playlist_id+'","'+video_id+'","'+publishdate+'","'+duration+'","'+license+'","'+title+'"')
			playlistitems_list_request = youtube.playlistItems().list_next(playlistitems_list_request, playlistitems_list_response)
		# print(' ')


def list_channel_videos(youtube, channel_id):
	channels_list_request = youtube.channels().list(part="id,contentDetails,snippet",  id=channel_id).execute()
	uploads_list_id = channels_list_request["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
	channel_title = channels_list_request["items"][0]["snippet"]["title"]
	list_playlist_videos(youtube, uploads_list_id)


def list_playlist_info(youtube, playlist_id):
	playlistitems_list_request = youtube.playlistItems().list(playlistId=playlist_id,part="snippet,contentDetails", maxResults=2).execute()
	print(playlistitems_list_request["items"])


def list_channel_info(yotuube, channel_id):  
	channels_list_request = youtube.channels().list(part="id,contentDetails,snippet",  id=channel_id).execute()
	print(channels_list_request["items"])





if __name__ == "__main__":
	# The "action" option specifies the action to be processed.
	argparser.add_argument("--action", help="Action")
	# The "channel_id" option specifies the ID of the selected YouTube channel.
	argparser.add_argument("--channel_id",
	  help="ID for channel for which the localization will be applied.")
	# The "default_language" option specifies the language of the channel's default metadata.
	argparser.add_argument("--default_language", help="Default language of the channel to update.",
	  default="en")
	# The "language" option specifies the language of the localization that is being processed.
	argparser.add_argument("--language", help="Language of the localization.", default="de")
	# The "description" option specifies the localized description of the chanel to be set.
	argparser.add_argument("--description", help="Localized description of the channel to be set.",
	  default="Localized Description")

	args = argparser.parse_args()
	youtube = get_authenticated_service(args)

	try: 
		for eachChannel in channels_list: 
			list_channel_info(youtube, eachChannel) 
			# list_channel_videos(youtube, eachChannel)
			print('------------------')
		for eachPlaylist in playlist_list:
			list_playlist_info(youtube, eachPlaylist) 
			# list_playlist_videos(youtube, eachPlaylist)
			print('------------------')
	except (HttpError):
		# print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
		print(HttpError)
		pass
	# else:
	# 	print("Set and retrieved localized metadata for a channel.")
