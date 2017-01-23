import time
import sys
from subprocess import check_call
try:
    import tkinter as tk
except:
    import Tkinter as tk

#while True:
try:
    check_call('scrot -z 123456.png', shell=True)
except Exception as e:
    check_call(['maim', '--format', 'png', '123456.png'])

#subprocess.check_call('epeg --width=13% --height=13% screen_shot.jpg screen_shot_thumb.jpg', shell=True)

#upload file
#file_name = home_dir + '1234567.png'
#file_post = requests.post(url, data={'project_name': project_name}, files={'ss': open(file_name, 'rb')}, headers={'Authorization': token})

root = tk.Tk()
root.overrideredirect(1)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

screen_shot_width = 194
screen_shot_height = 115
screen_shot_border_width = 177
screen_shot_border_height = 124

screen_shot_x = (screen_width) - (screen_shot_border_width)
screen_shot_y = (screen_height) - (screen_shot_border_height)

photo_image = tk.PhotoImage(file='123456.png')
img = photo_image.subsample(8, 8)

frame = tk.Frame(root, bg='gray')
frame.pack(fill='both', expand='yes')
image_label = tk.Label(frame, image=img)
image_label.place(x=2, y=23)

project_label = tk.Label(frame, text=sys.argv[1]) 
project_label.place(x=2, y=3)

def quit(event):
    root.destroy()
quit_button = tk.Label(frame, text='X')
quit_button.place(x=165, y=2)
quit_button.bind('<Button-1>', quit)

up = screen_height
def animate_up():
    global up
    up -= 2
    root.geometry('%dx%d+%d+%d' % (screen_shot_border_width, screen_shot_border_height, screen_shot_x, up))
    root.update()
    if up == screen_shot_y:
        root.after(2000, animate_down)
    else:
        root.after(10, animate_up)

down = screen_shot_y 
def animate_down():
    global down
    down += 2
    root.geometry('%dx%d+%d+%d' % (screen_shot_border_width, screen_shot_border_height, screen_shot_x, down))
    root.update()
    if down == screen_height:
        root.destroy()
    else:
        root.after(10, animate_down)

root.after(100, animate_up)
root.mainloop()
