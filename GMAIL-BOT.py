import base64
import httplib2
import string
import random
from email.mime.text import MIMEText

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run


# Path to the client_secret.json file downloaded from the Developer Console
CLIENT_SECRET_FILE = 'client_secret.json'

# Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'

# Location of the credentials storage file
STORAGE = Storage('gmail.storage')

# Start the OAuth flow to retrieve credentials
flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
http = httplib2.Http()

# Try to retrieve credentials from storage or run the flow to generate them
credentials = None
if credentials is None or credentials.invalid:
  credentials = run(flow, STORAGE, http=http)

# Authorize the httplib2.Http object with our credentials
http = credentials.authorize(http)

# Build the Gmail service from discovery
gmail_service = build('gmail', 'v1', http=http)
emailtosend = raw_input("Who would like to send the email to? \n")
subject = raw_input("What is the subject of your email? \n")
text = raw_input("What is the message you would like to send? \n")
number = input("How many times would you like to send this email?")
warning = raw_input("If you choose a number 500 or above Google may disable your account from \n sending emails for the next 24 hours.(Press enter to continue)")
# create a message to send
for _ in " "*number:
	message = MIMEText(text)
	message['to'] = emailtosend
	message['from'] = "you@go.here"
	message['subject'] = subject + "       " + 
	body = {'raw': base64.b64encode(message.as_string())}
	try:
		message = (gmail_service.users().messages().send(userId="me", body=body).execute())
		print('Message Id: %s' % message['id'])
		print(message)
		print "Message has been sent!"
	except Exception as error:
		print('An error occurred: %s' % error)
