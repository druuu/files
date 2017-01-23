import sys, os
import time
import re
import subprocess
import json
import requests


script_dir = '/opt/microtrack/'
home_dir = subprocess.check_output('echo $HOME', shell=True).strip('\n')+'/'
activity_dir = home_dir+'.microtrack/'

api_url = 'http://mt.micropyramid.com/'
activity_url = api_url + 'api/user_activity/'


with open(activity_dir+'request_data.json', 'r') as rdf:
    authorization = json.load(rdf)['authorization']

upload_url = api_url + 'api/store_screen/'
comment_url = api_url + 'api/user_comments/'
def post_activity_func():
    files = os.listdir(activity_dir)
    screen_shot_r = re.compile(r'(\d+)_(.*?)\.png')
    comment_r = re.compile(r'c_(\d+)_(.*)')
    for ad_file in files:
        project_name_m = screen_shot_r.match(ad_file)
        comment_m = comment_r.match(ad_file)
        if project_name_m:
            project_name = project_name_m.group(2)
            project_ts = project_name_m.group(1)
            print(ad_file, project_name, project_ts)
            image_rp = requests.post(upload_url, data={'project_name': project_name, \
                    'project_ts': project_ts}, files={'ss': open(activity_dir+ad_file, 'rb')}, \
                    headers={'Authorization': authorization})
            os.remove(activity_dir+ad_file)
        elif comment_m:
            project_name = comment_m.group(2)
            comment_ts = comment_m.group(1)
            with open(activity_dir+ad_file, 'r') as af:
                comment_c = af.read()
                requests.post(comment_url, data={'project_name': project_name, 'comment': comment_c, \
                        'comment_ts': comment_ts}, headers={'Authorization': authorization})
                        
            os.remove(activity_dir+ad_file)

    cp_cmd = 'cp %sactivity.txt %sactivity1.txt' % (activity_dir, activity_dir)
    subprocess.check_call(cp_cmd, shell=True)
    with open(activity_dir+'activity1.txt', 'r') as activity_file:
        activity_list = activity_file.readlines()
        activity_list = [line for line in activity_list if line.strip()]
        activity_set = set(activity_list)
        af_str = ''
        for act in activity_set:
            project_name = act[11:-1]
            activity_date = act[:10]
            active_time = activity_list.count(act)
            #TODO what if line is in wrong format
            af_str += '%s#$*%s#$*%s\n' % (activity_date, project_name, active_time)
        with open(activity_dir+'act_file', 'w') as af:
            af.write(af_str)

    rp = requests.post(activity_url, \
            files={'activity': open(activity_dir+'act_file', 'r')}, \
            headers={'Authorization': authorization})


post_activity_func()
