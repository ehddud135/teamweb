import os
import pickle
import pandas as pd
from django.conf import settings
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']


class EmailContactsList():
    def __init__(self):
        self.ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
        self.service = self.authenticate()
        self.contacts = self.get_contacts(self.service)
        self.contact_groups = self.get_contact_groups(self.service)

    def authenticate(self):
        """Authenticate the user and return the service object."""
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(f'{self.ROOT_PATH}/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        service = build('people', 'v1', credentials=creds)
        return service

    def get_contacts(self, service):
        """Retrieve contacts from the Google People API."""
        results = service.people().connections().list(
            resourceName='people/me',
            personFields='names,emailAddresses,organizations,memberships',
            pageSize=1000
        ).execute()
        connections = results.get('connections', [])
        return connections

    def get_contact_groups(self, service):
        """Retrieve contact groups from the Google People API."""
        results = service.contactGroups().list(
            pageSize=1000,
        ).execute()
        group_data = results.get('contactGroups', [])
        group_data = {group['resourceName']: group['name'] for group in group_data}
        return group_data

    def get_data(self):
        """Process contacts to extract desired fields."""
        data = []
        for person in self.contacts:
            emails = person.get('emailAddresses', [])
            memberships = person.get('memberships', [])

            names = person.get('names', [])
            organizations = person.get('organizations', [])

            name = names[0].get('displayName') if names else 'No Name'
            org_name = organizations[0].get('name') if organizations else 'No Organization'
            if emails:
                label_names = []
                contact_emails = []
                for email in emails:
                    contact_emails.append(email.get('value'))
                for membership in memberships:
                    group_id = membership['contactGroupMembership']['contactGroupResourceName']
                    label_name = self.contact_groups.get(group_id, 'Unknown')
                    label_names.append(label_name)
                data.append({
                    'Name': name,
                    'Email': ', '.join(contact_emails),
                    'Organization': org_name,
                    'Labels': ', '.join(label_names)
                })
        return data


em = EmailContactsList()
df = pd.DataFrame(em.get_data())
print(df)
