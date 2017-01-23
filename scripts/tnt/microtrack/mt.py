import os
import sys
import time
from subprocess import Popen, check_output, PIPE, check_call
from textwrap import dedent


app_dir = '/opt/microtrack'
pid_dir = '%s/pid_dir' % app_dir
activity_file = '/root/.microtrack/activity.txt' 

rd = check_output('python %s/request_data.py' % app_dir, shell=True)
projects, authorization = rd.strip().split('  ')

project_name = projects[0]
tt_cmd = 'grep -c %s ~/.microtrack/activity.txt | cat' % (time.strftime('%Y_%m_%d'))
at_cmd = 'grep -c "%s %s" ~/.microtrack/activity.txt | cat' % (time.strftime('%Y_%m_%d'), project_name)
total_time = check_output(tt_cmd, shell=True).strip()
active_time = check_output(at_cmd, shell=True).strip()
ideal_time = '0'

run_main = r"""echo $$ > %s/main.pid && exec stdbuf -i0 -e0 -o0 python main.py 12 'Ubuntu Condensed' \
        '%s %s %s' '%s' > mt_fifo""" % (pid_dir, total_time, active_time, ideal_time, projects)
        
Popen(run_main, shell=True)

run_timer_cmd = r'echo $$ > %s/timer.pid && exec stdbuf -i0 -e0 -o0 python /opt/microtrack/timer.py \
        --total_time %s --active_time %s --idle_time %s > %s/timer_fifo' % \
        (pid_dir, total_time, active_time, ideal_time, app_dir)
        
save_timer_cmd = r'echo $$ > %s/save_timer.pid && \
        exec bash %s/save_timer.sh' % (pid_dir, app_dir)

xpi_cmd = r'echo $$ > %s/xpi.pid && \
        exec bash %s/xprintidle.sh' % (pid_dir, app_dir)

ss_cmd = r'echo $$ > %s/ss.pid && \
        exec python %s/screen_shot_ctl.py' % (pid_dir, app_dir)

comment_cmd = r'echo $$ > %s/comment.pid && \
        exec python %s/comment.py' % (pid_dir, app_dir)


def kill(pid_file):
    with open(pid_file, 'r') as pf:
        pid = pf.read().strip()
    check_call('kill -9 %s' % pid, shell=True)
    try:
        check_call('rm %s' % pid_file, shell=True)
    except:
        pass

if os.listdir(pid_dir) != []:
    msg = '''
    Last session didn't end properly, track the processes with pids in %s
    directory, kill them if they are microtrack processes and clear directory''' % pid_dir
    print(dedent(msg))
            
    sys.exit()


mf_proc = Popen('cat mt_fifo', shell=True, stdout=PIPE)
while True:
    mf_output = mf_proc.stdout.readline()
    if 'start' in mf_output:
        action, project_name = mf_output.split(' ')
        rt_proc = Popen(run_timer_cmd, shell=True)
        st_proc = Popen('%s %s' % (save_timer_cmd, project_name), shell=True)
        xpi_proc = Popen(xpi_cmd, shell=True)
        ss_proc = Popen('%s %s' % (ss_cmd, project_name), shell=True)

    elif 'stop' in mf_output:
        kill('%s/timer.pid' % pid_dir)
        kill('%s/save_timer.pid' % pid_dir)
        kill('%s/xpi.pid' % pid_dir)
        kill('%s/ss.pid' % pid_dir)
        if os.path.exists('%s/comment.pid' % pid_dir):
            kill('%s/comment.pid' % pid_dir)

    elif 'quit' in mf_output:
        if os.path.exists('%s/timer.pid' % pid_dir):
            kill('%s/timer.pid' % pid_dir)
        if os.path.exists('%s/save_timer.pid' % pid_dir):
            kill('%s/save_timer.pid' % pid_dir)
        if os.path.exists('%s/xpi.pid' % pid_dir):
            kill('%s/xpi.pid' % pid_dir)
        if os.path.exists('%s/ss.pid' % pid_dir):
            kill('%s/ss.pid' % pid_dir)
        if os.path.exists('%s/comment.pid' % pid_dir):
            kill('%s/comment.pid' % pid_dir)
        if os.path.exists('%s/main.pid' % pid_dir):
            kill('%s/main.pid' % pid_dir)
        break

    elif 'comment' in mf_output:
        action, project_name = mf_output.split(' ')
        comment = Popen('%s %s' % (comment_cmd, project_name), shell=True)

    else:
        break
