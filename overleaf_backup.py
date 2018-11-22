#!/usr/bin/env python3

''' Download zip backups of Overleaf projects.

Author: Gabriel Pelouze
License: GNU GPL v3 or later (https://www.gnu.org/licenses/gpl-3.0.txt)

The OverleafClient class contains code from Todor Mihaylov’s Overleaf backup
tool (https://github.com/tbmihailov/overleaf-backup-tool).

'''

import getpass
import json
import re
import time

from bs4 import BeautifulSoup
import requests

class OverleafClient(object):
    def __init__(self):
        self.url_signin = 'https://www.overleaf.com/login'
        self.login_cookies = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
            }

    def login_with_user_and_pass(self, email, password):
        ''' Try to login to and sets the login cookie if successful.

        Parameters
        ==========
        email : str
            Overleaf login email
        password : str
            Overleaf password
        :return:
        '''

        is_successfull = False

        # get sign_in page html and get csrf token
        r_signing_get = requests.get(self.url_signin, headers=self.headers)
        if r_signing_get.status_code != 200:
            msg = 'Status code {0} when loading {1}'
            msg = err_msg.format(r_signing_get.status_code, self.url_signin)
            raise Exception(msg)

        html_doc = r_signing_get.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        authenticity_token = ''
        for tag in soup.find_all('input'):
            if tag.get('name', None) == '_csrf':
                authenticity_token = tag.get('value', None)
                break

        if len(authenticity_token) == 0:
            err_msg = 'CSRF token is empty'
            raise Exception(err_msg)

        # send login form
        login_json = {'_csrf': authenticity_token,
                      'email': email,
                      'password': password,
                      }
        r_signing_post = requests.post(
            self.url_signin,
            data=login_json,
            timeout=5,
            headers=self.headers,
            cookies=r_signing_get.cookies)

        if not r_signing_post.status_code == 200:
            err_msg = 'Status code {} when signing in {1} with user [{2}].'
            msg = err_msg.format(
                r_signing_post.status_code, self.url_signin, email)
            raise Exception(err_msg)

        try:
            response = json.loads(r_signing_post.text)
            if response['message']['type'] == 'error':
                msg = 'Login failed: {}'
                msg = msg.format(response['message']['text'])
                raise ValueError(msg)
        except json.JSONDecodeError:
            # this happens when the login is successful
            pass
        self.login_cookies = r_signing_post.cookies

    def download_zip(self, project, output=None):
        if project.startswith('http'):
            m = re.match('https?://v2\.overleaf\.com/project/([^/]+)', project)
            project_id = m.group(1)
        else:
            project_id = project
        url = 'https://v2.overleaf.com/project/{}/download/zip'.format(project_id)

        if output is None:
            output = 'overleaf_{}_{}.zip'.format(project_id, int(time.time()))

        r = requests.get(
            url, 
            headers=self.headers, cookies=self.login_cookies,
            stream=True)
        if r.status_code == 200:
            with open(output, 'wb') as f:
                for chunk in r:
                    f.write(chunk)

if __name__ == '__main__':
    
    import argparse

    parser = argparse.ArgumentParser(
        description='Download zip backups of Overleaf projects.')
    parser.add_argument(
        'project',
        type=str,
        nargs='+',
        help='project URL or ID')
    parser.add_argument(
        '-O', '--output',
        type=str,
        default=None,
        help='output zip file (only for a single project)')
    args = parser.parse_args()

    if len(args.project) > 1 and args.output is not None:
        raise ValueError('Cannot specify output for multiple projects')

    c = OverleafClient()
    c.login_with_user_and_pass(input('Email: '), getpass.getpass())
    for project in args.project:
        c.download_zip(project, output=args.output)
