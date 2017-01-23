import time
import sys
import datetime, subprocess
import functools, random
import socket
import pickle
import json
import requests
from threading import Thread
try:
    import tkinter as tk
except:
    import Tkinter as tk

# try with python3, if error, fallback to python2
script_dir = '/opt/microtrack/'
home_dir = (subprocess.check_output('echo $HOME', shell=True)).strip('\n')+'/'
try:
    subprocess.check_call('ls '+home_dir+'.microtrack > /dev/null', shell=True)
except Exception as e:
    subprocess.check_call('mkdir '+home_dir+'.microtrack && touch '+home_dir+'.microtrack/activity.txt', shell=True)
activity_dir = home_dir+'.microtrack/'

font_size = int(sys.argv[1])
font_family = sys.argv[2]
total_time, active_time, idle_time = [int(t) for t in sys.argv[3].split(' ')]
#TODO project with | char will break
projects1 = sys.argv[4].split('|')

root = tk.Tk()

root_width = 120
root_height = 210
root_x = 1245
root_y = 506

root.overrideredirect(1)
root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_x, root_y))
root.configure(bg='#ffffff')
root.title('mt_8ca0681d11ae4e0c9e9fd6d2ba038104')

frame = tk.Frame(root, bg='white')
frame.grid(row=0, column=0)
frame.pack(fill='both', expand='yes')

frame_project = tk.Frame(root, bg='white')
frame_project.pack_forget()

frame_login = tk.Frame(root, bg='white')
frame_login.pack_forget()

close_image = tk.PhotoImage(file=script_dir+'close_4.png')
quit_label = tk.Label(root, image=close_image, bg='white')
quit_label.config(cursor='X_cursor')
quit_label.place(x=root_width-18, y=7)

withdraw_image = tk.PhotoImage(file=script_dir+'withdraw.png')
withdraw_label = tk.Label(root, image=withdraw_image, bg='white')
withdraw_label.place(x=root_width-37, y=7)

def withdraw_func(event):
    root.state('withdrawn')
withdraw_label.bind('<Button-1>', withdraw_func)

def quit(event):
    print('quit %s' % project_name)
    #root.destroy()
quit_label.bind('<Button-1>', quit)

projects = []
for project in projects1:
    spaces = 41 - len(project)
    if spaces > 0:
        projects.append(project+' '*spaces)
    else:
        projects.append(project)

project_name = projects1[0]
project_label = tk.Label(frame, text=projects1[0], font=(font_family, font_size), bg='#ffffff')
pl_x = (root_width-(len(projects1[0])*6.8))/2.0
project_label.place(x=pl_x, y=root_height*0.20)

def comment(event):
    print('comment %s' % project_name)

project_label.bind('<Button-1>', comment)


def hm_func(seconds):
    hours = seconds//3600
    seconds %= 3600
    minutes = seconds//60
    return '%02i:%02i' % (hours, minutes)

active_time_label = tk.Label(frame, text='Active: '+hm_func(active_time), font=(font_family, font_size), bg='white')
active_time_label.place(x=20, y=root_height*0.33)
total_time_label = tk.Label(frame, text='Today: '+hm_func(total_time), font=(font_family, font_size), bg='white')
total_time_label.place(x=20, y=root_height*0.44)

active_time_label.config(text='Active: '+hm_func(active_time))
total_time_label.config(text='Today: '+hm_func(total_time))

image_start = tk.PhotoImage(file=script_dir+'power.png')
def stop(event=None):
    power_label.config(image=image_start)
    power_label.unbind('<Button-1>')
    power_label.bind('<Button-1>', start)

    print('stop %s' % project_name)


image_stop = tk.PhotoImage(file=script_dir+'red.png')
def start(event):
    active_time_label.config(text='Active: '+hm_func(active_time))
    total_time_label.config(text='Today: '+hm_func(total_time))

    power_label.unbind('<Button-1>')
    power_label.bind('<Button-1>', stop)
    power_label.config(image=image_stop)

    print('start %s' % project_name)
    

power_label = tk.Label(frame, image=image_start, bg='white')
power_label.bind('<Button-1>', start)
power_label.config(cursor='hand2')
power_label.place(x=17, y=125)





### tabbed stuff #######
home_image = tk.PhotoImage(file=script_dir+'home.png')
tl_home = tk.Label(root, image=home_image, bg='white')
tl_home.place(x=1, y=7)
def tf_home(event):
    frame_login.pack_forget()
    frame_project.pack_forget()
    frame.grid()
    frame.pack(fill='both', expand='yes')
tl_home.bind('<Button-1>', tf_home)

list_image = tk.PhotoImage(file=script_dir+'list.png')
tl_projects = tk.Label(root, image=list_image, bg='white')
tl_projects.place(x=25, y=7)

project_label1_list = []
def select_project1(event, project):
    global project_name
    stop()
    project = project.rstrip()
    frame_project.pack_forget()
    frame.grid(row=0, column=0)
    frame.pack(fill='both', expand='yes')
    project_label.config(text=project)
    pl_x = (root_width-(len(project)*6.8))/2.0
    project_label.place(x=pl_x)
    project_name = project
    
    active_time_label.config(text='Active: '+hm_func(active_time))
    total_time_label.config(text='Today: '+hm_func(total_time))

def tf_projects(event, page):
    global project_label1_list

    for project_label in project_label1_list:
        project_label.place_forget()

    frame.pack_forget()
    frame_login.pack_forget()
    frame_project.grid(row=0, column=0)
    frame_project.pack(fill='both', expand='yes')

    y = 35
    project_label1_list = []
    for project in projects[(page-1)*6:page*6]:
        pf_line = tk.Frame(frame_project, width=200, height=1, bg='#A0A0A0')
        pf_line.place(x=0, y=y)
        project_label1 = tk.Label(frame_project, text=project, font=(font_family, font_size-1), bg='#ffffff')
        project_label1.pack(fill='both', expand='yes')
        project_label1.place(x=2, y=y+2)
        project_label1_list.append(project_label1)
        project_label1_list.append(pf_line)
        y += 24
        project_label1.bind('<Button-1>', functools.partial(select_project1, project=project))
        project_label1.bind('<Enter>', lambda event, h=project_label1: h.configure(bg='#3399ff'))
        project_label1.bind('<Leave>', lambda event, h=project_label1: h.configure(bg='#ffffff'))
    pf_line = tk.Frame(frame_project, width=200, height=1, bg='#A0A0A0')
    pf_line.place(x=0, y=y)
    project_label1_list.append(pf_line)

    tl_next.place(x=root_width*0.8, y=root_height*0.9)
    tl_prev.place_forget()

page = 1
def tf_projects0(event):
    global page
    page = 1
    tf_projects(event, page)
tl_projects.bind('<Button-1>', tf_projects0)

def tf_projects1(event, page):
    global project_label1_list

    for project_label1 in project_label1_list:
        project_label1.place_forget()

    y = 35
    for project in projects[(page-1)*6:page*6]:
        pf_line = tk.Frame(frame_project, width=200, height=1, bg='#A0A0A0')
        pf_line.place(x=0, y=y)
        project_label1 = tk.Label(frame_project, text=project, font=(font_family, font_size-1), bg='#ffffff')
        project_label1.pack(fill='both', expand='yes')
        project_label1.place(x=2, y=y+2)
        project_label1_list.append(project_label1)
        project_label1_list.append(pf_line)
        y += 24
        project_label1.bind('<Button-1>', functools.partial(select_project1, project=project))
        project_label1.bind('<Enter>', lambda event, h=project_label1: h.configure(bg='#3399ff'))
        project_label1.bind('<Leave>', lambda event, h=project_label1: h.configure(bg='#ffffff'))
        #row += 1
    pf_line = tk.Frame(frame_project, width=200, height=1, bg='#A0A0A0')
    pf_line.place(x=0, y=y)
    project_label1_list.append(pf_line)

next_image = tk.PhotoImage(file=script_dir+'next.png')
tl_next = tk.Label(frame_project, image=next_image, bg='white')
def tf_next(event):
    global page
    page += 1
    tf_projects1(event, page)
    tl_prev.place(x=0, y=root_height*0.9)
    if page > len(projects)/7:
        tl_next.place_forget()
tl_next.bind('<Button-1>', tf_next)

prev_image = tk.PhotoImage(file=script_dir+'prev.png')
tl_prev = tk.Label(frame_project, image=prev_image, bg='white')
def tf_prev(event):
    global page
    page -= 1
    tf_projects1(event, page)
    tl_next.place(x=root_width*0.8, y=root_height*0.9)
    if page == 1:
        tl_prev.place_forget()
tl_prev.bind('<Button-1>', tf_prev)
#### end of tabs #########



root.mainloop()
