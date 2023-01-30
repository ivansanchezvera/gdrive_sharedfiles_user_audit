from __future__ import print_function

import os.path

import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/drive.activity.readonly']
# SCOPES = ['https://www.googleapis.com/auth/drive.activity', 'https://www.googleapis.com/auth/contacts.readonly', "https://www.googleapis.com/auth/contacts", "https://www.googleapis.com/auth/user.emails.read", "https://www.googleapis.com/auth/profile.emails.read", "https://www.googleapis.com/auth/directory.readonly"]
SCOPES =    ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.activity', 
            'https://www.googleapis.com/auth/contacts.readonly', "https://www.googleapis.com/auth/contacts", 
            "https://www.googleapis.com/auth/user.emails.read", "https://www.googleapis.com/auth/directory.readonly"]


creds = None

def main():
    """Shows basic usage of the Drive Activity API.

    Prints information about the last 10 events that occured the user's Drive.
    """
    creds = None
    # # The file token.json stores the user's access and refresh tokens, and is
    # # created automatically when the authorization flow completes for the first
    # # time.
    # if os.path.exists('credentials.json'):
    #     # creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    #     creds = Credentials.from_authorized_user_file('credentials.json', SCOPES)

    # # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open('token.json', 'w') as token:
    #         token.write(creds.to_json())


	# Check if file token.pickle exists
    if os.path.exists('token.pickle'):

		# Read the token from the file and
		# store it in the variable creds
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

	# If no valid credentials are available,
	# request the user to log in.
    if not creds or not creds.valid:

		# If token is expired, it will be refreshed,
		# else, we will request a new one.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

		# Save the access token in token.pickle
		# file for future usage
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)


    #First lets filter the files
    # Connect to the API service
    service_drive = build('drive', 'v3', credentials=creds)

	# request a list of first N files or
	# folders with name and id from the API.
    resource = service_drive.files()
    shared_files_results = resource.list(pageSize=50, q="(visibility != 'limited') AND (modifiedTime <= \"2022-06-01T00:00:00-05:00\")", fields="files(id, name, shared, trashed, createdTime, modifiedTime)").execute()
    print(shared_files_results)

    #Now the drive Activity code.
    service = build('driveactivity', 'v2', credentials=creds)

    if(shared_files_results is not None):
        for shared_file in shared_files_results.get("files"):
            print("********FILE IS:********")
            print(shared_file)
            print(f"fileId is: {shared_file.get('id')}")
            print("Activities are:")
            activities = queryFileActivity(itemName=shared_file.get('id'), service=service)
            print(activities)
            print("********END OF THIS FILE********")
            print()

    # #Now the drive Activity code.
    # service = build('driveactivity', 'v2', credentials=creds)

    # # Call the Drive Activity API
    # try:
    #     results = service.activity().query(body={
    #         'pageSize': 3,
    #         # "filter": "time <= \"2015-06-01T00:00:00-05:00\" AND actor != """,
    #         "filter": "time <= \"2015-06-01T00:00:00-05:00\"",
    #     }).execute()
    #     activities = results.get('activities', [])

    #     if not activities:
    #         print('No activity.')
    #     else:
    #         print('Recent activity:')
    #         for activity in activities:
    #             time = getTimeInfo(activity)
    #             action = getActionInfo(activity['primaryActionDetail'])
    #             actors = map(getActorInfo, activity['actors'])
    #             targets = map(getTargetInfo, activity['targets'])
    #             actors_str, targets_str = "", ""
    #             actor_name = actors_str.join(actors)
    #             target_name = targets_str.join(targets)

    #             # Print the action occurred on drive with actor, target item and timestamp
    #             print(u'{0}: {1}, {2}, {3}'.format(time, action, actor_name, target_name))

    # except HttpError as error:
    #     # TODO(developer) - Handleerrors from drive activity API.
    #     print(f'An error occurred: {error}')

#Query activity by file
def queryFileActivity(itemName, service):
    # Call the Drive Activity API
    # service = build('driveactivity', 'v2', credentials)
    try:
        results = service.activity().query(body={
            'pageSize': 200,
            # "filter": "time <= \"2015-06-01T00:00:00-05:00\" AND actor != """,
            "filter": "time <= \"2022-06-01T00:00:00-05:00\"",
            "itemName": f"items/{itemName}",

        }).execute()
        activities = results.get('activities', [])
        print(activities)

        if not activities:
            print('No activity.')
        else:
            print('Recent activity:')
            for activity in activities:
                time = getTimeInfo(activity)
                action = getActionInfo(activity['primaryActionDetail'])
                actors = map(getActorInfo, activity['actors'])
                targets = map(getTargetInfo, activity['targets'])
                actors_str, targets_str = "", ""
                actor_name = actors_str.join(actors)
                target_name = targets_str.join(targets)

                # Print the action occurred on drive with actor, target item and timestamp
                print(u'{0}: {1}, {2}, {3}'.format(time, action, actor_name, target_name))

    except HttpError as error:
        # TODO(developer) - Handleerrors from drive activity API.
        print(f'An error occurred: {error}')

# Returns the name of a set property in an object, or else "unknown".
def getOneOf(obj):
    for key in obj:
        return key
    return 'unknown'


# Returns a time associated with an activity.
def getTimeInfo(activity):
    if 'timestamp' in activity:
        return activity['timestamp']
    if 'timeRange' in activity:
        return activity['timeRange']['endTime']
    return 'unknown'


# Returns the type of action.
def getActionInfo(actionDetail):
    return getOneOf(actionDetail)


def printUserName(knownUser):
    try:
            # Check if file token.pickle exists
        if os.path.exists('token.pickle'):

            # Read the token from the file and
            # store it in the variable creds
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials are available,
        # request the user to log in.
        if not creds or not creds.valid:

            # If token is expired, it will be refreshed,
            # else, we will request a new one.
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the access token in token.pickle
            # file for future usage
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        # print(creds)
        service = build('people', 'v1', credentials=creds)

        # Call the People API
        # print('List 10 connection names')
        # results = service.people().connections().list(
        #     resourceName='people/me',
        #     pageSize=10,
        #     personFields='names,emailAddresses').execute()
        # connections = results.get('connections', [])


        # names = service.people().get(resourceName=knownUser,personFields="emailAddresses", requestMask_includeField="person.names").execute()
        person_fetched = service.people().get(resourceName=knownUser,personFields="emailAddresses,names,metadata").execute()
        print(person_fetched)
        print(type(person_fetched))
        if person_fetched:
            if "names" in person_fetched.keys():
                print(f'This person has a name: {person_fetched["names"][0]["displayName"]}')
            if "emailAddresses" in person_fetched.keys():
                print(f'This person has also email: {person_fetched["emailAddresses"][0]["value"]}')

    except HttpError as err:
        print(err)


# Returns user information, or the type of user if not a known user.
def getUserInfo(user):
    if 'knownUser' in user:
        knownUser = user['knownUser']
        isMe = knownUser.get('isCurrentUser', False)
        if(not isMe):
            print(knownUser)
            printUserName(knownUser['personName'])
            print()
        # return u'people/me' if isMe else knownUser['personName']
        return u'people/me' if isMe else knownUser['personName']
    return getOneOf(user)


# Returns actor information, or the type of actor if not a user.
def getActorInfo(actor):
    if 'user' in actor:
        return getUserInfo(actor['user'])
    return getOneOf(actor)


# Returns the type of a target and an associated title.
def getTargetInfo(target):
    if 'driveItem' in target:
        title = target['driveItem'].get('title', 'unknown')
        return 'driveItem:"{0}"'.format(title)
    if 'drive' in target:
        title = target['drive'].get('title', 'unknown')
        return 'drive:"{0}"'.format(title)
    if 'fileComment' in target:
        parent = target['fileComment'].get('parent', {})
        title = parent.get('title', 'unknown')
        return 'fileComment:"{0}"'.format(title)
    return '{0}:unknown'.format(getOneOf(target))


if __name__ == '__main__':
    main()
