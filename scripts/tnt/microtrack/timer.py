import time
import sys
import datetime, subprocess
import requests
import argparse

# try with python3, if error, fallback to python2
script_dir = '/opt/microtrack/'
home_dir = (subprocess.check_output('echo $HOME', shell=True)).strip('\n')+'/'
activity_dir = home_dir+'.microtrack/'
api_url = 'http://mt.micropyramid.com/'
#api_url = 'http://127.0.0.1:8000/'
activity_url = api_url + 'api/user_activity/'

#font_size = int(sys.argv[1])
#font_family = sys.argv[2]
font_size = 12
font_family = 'Ubuntu Condensed'

try:
    import tkinter as tk
except:
    import Tkinter as tk

root = tk.Tk()
root_width = 85
root_height = 30
root_x = 1265
root_y = 556+64+110

root.overrideredirect(1)
root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_x, root_y))
root.configure(bg='#f6f6f6')

def show_main(event):
    print('show_main')
root.bind('<Button-1>', show_main)

active_time_l = tk.Label(root, text='00:00:00', bg='#f6f6f6', font=(font_family, font_size+7))
active_time_l.place(x=1, y=-2)

#project_name = sys.argv[1]

#tt_cmd = 'grep -c %s ~/.microtrack/activity.txt | cat' % (time.strftime('%Y_%m_%d'))
#at_cmd = 'grep -c "%s %s" ~/.microtrack/activity.txt | cat' % (time.strftime('%Y_%m_%d'), project_name)
#total_time = int(subprocess.check_output(tt_cmd, shell=True))
#active_time = int(subprocess.check_output(at_cmd, shell=True))
parser = argparse.ArgumentParser()
options = ['--total_time', '--active_time', '--idle_time']
for option in options:
    parser.add_argument(option, required=True)
args = parser.parse_args()

total_time = int(args.total_time)
active_time = int(args.active_time)
idle_time = int(args.idle_time)

def hms_func(seconds):
    hours = seconds//3600
    seconds %= 3600
    minutes = seconds//60
    seconds %= 60
    return '%02i:%02i:%02i' % (hours, minutes, seconds)

#def post_activity_func():
#    try:
#    	cp_cmd = 'cp %sactivity.txt %sactivity1.txt' % (activity_dir, activity_dir)
#    	subprocess.check_call(cp_cmd, shell=True)
#    	with open(activity_dir+'activity1.txt', 'r') as activity_file:
#    	    activity_list = activity_file.readlines()
#    	    activity_list = [line for line in activity_list if line.strip()]
#    	    activity_set = set(activity_list)
#    	    af_str = ''
#    	    for act in activity_set:
#    	        project_name = act[11:-1]
#    	        activity_date = act[:10]
#    	    	active_time = activity_list.count(act)
#    	    	af_str += '%s#$*%s#$*%s\n' % (activity_date, project_name, active_time)
#    	    with open(activity_dir+'act_file', 'w') as af:
#    	        af.write(af_str)
#
#    	rp = requests.post(activity_url, \
#    	        files={'activity': open(activity_dir+'act_file', 'r')}, headers={'Authorization': authorization})
#    	print('status: ', rp)
#    except Exception as e:
#        print('postact', str(e))
#    root.after(300000, post_activity_func)

def timer():
    global active_time, idle_time, total_time

    #xpi = int(subprocess.check_output(['xprintidle']).strip())
    #save_activity_cmd = 'echo "%s %s" >> %sactivity.txt' % (time.strftime('%Y_%m_%d'), project_name, activity_dir)
    #subprocess.check_call(save_activity_cmd, shell=True)

    active_time += 1
    idle_time -= 1
    total_time += 1
    print(time.strftime('%Y_%m_%d'))

    #if xpi < 300000:
    #    active_time += 1
    #    idle_time -= 1
    #    total_time += 1
    #    print(time.strftime('%Y_%m_%d'))
    #else:
    #    active_time -= 300
    #    idle_time += 300
    #    total_time -= 300
    #    subprocess.call('echo "stop" > %smt_fifo' % (activity_dir), shell=True)

    active_time_l.config(text=hms_func(active_time))
    #total_time_l.config(text=hms_func(total_time))
    root.after(1000, timer)

timer()
#post_activity_func()
root.mainloop()
