# flake8: noqa
import logging

import httplib2
from apiclient import errors
from apiclient.discovery import build
from ava_core.gather.gather_abstract.utils import load_local_test_data, create_local_test_data
from django.conf import settings

from ava_core.gather.gather_abstract.interface import DirectoryHelper

log = logging.getLogger(__name__)


class GoogleDirectoryHelper(DirectoryHelper):
    def __init__(self):
        pass

    DATA_SOURCE = 'google'

    DIRECTORY_SERVICE = None

    DATA_IMPORT_FILES = {
        'users': 'users',
        'groups': 'groups',
        'group_members': 'group_members',
    }


    def import_directory(self, credential):
        # Feature and testing toggle to allow developers to test GATHER locally
        # Uses an environment variable to decide whether to test against local JSON file or not
        # To test locally, ensure that the gather.py variable 'GATHER_USE_LOCAL' is set

        if settings.GATHER_USE_LOCAL['google']:
            return load_local_test_data(self.DATA_SOURCE, self.DATA_IMPORT_FILES)

        else:

            self.setup(credential)

            groups = self.get_groups()

            results = {
                'users': self.get_users(),
                'groups': groups,
                'group_members': self.get_group_members(groups),
            }

            # Feature and testing toggle to allow developers to test export new test data from gather
            # Uses a settings variable to decide whether to dump the data to file or not
            # To toggle this feature on, ensure that the gather.py variable 'CREATE_LOCAL_DATA' is set
            if settings.GATHER_CREATE_LOCAL['google']:
                create_local_test_data(self.DATA_SOURCE, results)

        return results


    def setup(self, credential):
        http = httplib2.Http()
        http = credential.authorize(http)
        self.DIRECTORY_SERVICE = build('admin', 'directory_v1', http=http)


    def get_users(self):
        page_token = None

        params = {'customer': 'my_customer'}
        all_users = []
        while True:
            try:
                if page_token:
                    params['pageToken'] = page_token
                current_page = self.DIRECTORY_SERVICE.users().list(**params).execute()

                all_users.extend(current_page['users'])
                page_token = current_page.get('nextPageToken')
                if not page_token:
                    break

            except errors.HttpError as error:
                print('An error occurred: %s' % error)
                break

        return all_users


    def get_groups(self):
        page_token = None
        params = {'customer': 'my_customer'}
        all_groups = []
        while True:
            try:
                if page_token:
                    params['pageToken'] = page_token
                current_page = self.DIRECTORY_SERVICE.groups().list(**params).execute()

                all_groups.extend(current_page['groups'])
                page_token = current_page.get('nextPageToken')
                if not page_token:
                    break

            except errors.HttpError as error:
                print('An error occurred: %s' % error)
                break

        return all_groups


    def get_user_groups(self, all_users):
        page_token = None
        params = {}
        user_groups = {}

        for user in all_users:
            user_groups[user['primaryEmail']] = []

            while True:
                try:
                    if page_token:
                        params['pageToken'] = page_token

                    params['userKey'] = user['id']
                    current_page = self.DIRECTORY_SERVICE.groups().list(**params).execute()
                    curr_groups = []

                    if 'groups' in current_page:
                        curr_groups.extend(current_page['groups'])
                        # print current_page['groups']

                    page_token = current_page.get('nextPageToken')
                    if not page_token:
                        user_groups[user['primaryEmail']] = curr_groups
                        break

                except errors.HttpError as error:
                    print('An error occurred: %s' % error)
                    break

        return user_groups


    def get_group_members(self, all_groups):
        page_token = None
        params = {}
        group_members = {}

        for group in all_groups:
            group_members[group['id']] = []

            while True:
                try:
                    if page_token:
                        params['pageToken'] = page_token

                    params['groupKey'] = group['id']
                    current_page = self.DIRECTORY_SERVICE.members().list(**params).execute()
                    curr_members = []

                    if 'members' in current_page:
                        curr_members.extend(current_page['members'])

                    page_token = current_page.get('nextPageToken')
                    if not page_token:
                        group_members[group['id']] = curr_members
                        break

                except errors.HttpError as error:
                    print('An error occurred: %s' % error)
                    break

        return group_members
