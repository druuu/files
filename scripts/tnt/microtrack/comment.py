from sys import exit, argv
import time
try:
    import tkinter as tk
except:
    import Tkinter as tk
from requests import post


activity_dir = '/root/.microtrack'
font_family = 'Ubuntu Condesed'
font_size = 12

comment_win = tk.Tk()
#comment_win.overrideredirect(1)
comment_win.geometry('%dx%d+%d+%d' % (350, 120, 563, 330))
comment_box = tk.Text(comment_win, width=49, height=4, font=(font_family, font_size))
comment_box.place(x=0, y=1)

def comment_sf():
    timestamp = int(time.time())
    project_name = argv[1]
    with open('%s/c_%d_%s' % (activity_dir, timestamp, project_name), 'w') as cf:
        cf.write(comment_box.get("1.0",'end-1c'))
    exit(0)
comment_sb = tk.Button(comment_win, text='Send', \
        font=(font_family, font_size), command=comment_sf)
comment_sb.place(x=288, y=85)

comment_win.mainloop()
