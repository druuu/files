from __future__ import print_function
import subprocess
import json
import requests


api_url = 'http://mt.micropyramid.com/'
login_url = api_url + 'api/user/login/'

script_dir = '/opt/microtrack/'
home_dir = (subprocess.check_output('echo $HOME', shell=True)).strip('\n')+'/'
try:
    subprocess.check_call('ls '+home_dir+'.microtrack > /dev/null', shell=True)
except Exception as e:
    subprocess.check_call('mkdir '+home_dir+'.microtrack && touch '+home_dir+'.microtrack/activity.txt', shell=True)
activity_dir = home_dir+'.microtrack/'

with open(home_dir+'.mtrc', 'r') as mtrc_file:
    mtrc_list = mtrc_file.readlines()
email_addr = mtrc_list[0].strip('\n')
password = mtrc_list[1].strip('\n')

login_response = requests.post(login_url, data={'email': email_addr, 'password': password})
authorization = "token "+login_response.json()['data']['auth_token']

projects_json = login_response.json()['data']['assigned_projects']
request_data = [project['project']['name'] for project in projects_json]
projects = '|'.join(request_data)

print('%s  %s' % (projects, authorization))

#request_data = {'authorization': authorization, 'projects': projects_json}
#with open(activity_dir+'request_data.json', 'w') as rdf:
#    json.dump(request_data, rdf)
#print(request_data)
