from subprocess import check_call
from sys import argv
try:
    import tkinter as tk
except:
    import Tkinter as tk

#while True:
try:
    check_call('scrot -z /tmp/123456.png', shell=True)
except Exception as e:
    check_call(['maim', '--format', 'png', '/tmp/123456.png'])

#subprocess.check_call('epeg --width=13% --height=13% screen_shot.jpg screen_shot_thumb.jpg', shell=True)

#upload file
#file_name = home_dir + '/tmp/1234567.png'
#file_post = requests.post(url, data={'project_name': project_name}, files={'ss': open(file_name, 'rb')}, headers={'Authorization': token})

root = tk.Tk()
root.overrideredirect(1)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

screen_shot_width = 194
screen_shot_height = 80
screen_shot_border_width = 144
screen_shot_border_height = 18

screen_shot_x = (screen_width) - (screen_shot_border_width)
screen_shot_y = 0 #(screen_height) - (screen_shot_border_height)

photo_image = tk.PhotoImage(file='/tmp/123456.png')
img = photo_image.subsample(8, 8)

frame = tk.Frame(root, bg='gray')
frame.pack(fill='both', expand='yes')
#image_label = tk.Label(frame, image=img)
image_label = tk.Label(frame)
#image_label.place(x=2, y=10)

msg = '%s %s, %s' % (argv[1], argv[2], argv[3])
project_label = tk.Label(frame, text=msg) #, font=('druuu', '8'))
project_label.place(x=1, y=1)

def quit(event):
    root.destroy()
quit_button = tk.Label(frame, text='X')
#quit_button.place(x=155, y=2)
#quit_button.bind('<Button-1>', quit)

left = screen_width
def animate_left():
    global left
    left -= 1
    root.geometry('%dx%d+%d+%d' % (screen_shot_border_width, screen_shot_border_height, left, screen_shot_y))
    root.update()
    if left == screen_shot_x:
        root.after(5000, animate_right)
    else:
        root.after(2, animate_left)

right = screen_shot_x
def animate_right():
    global right
    right += 1
    root.geometry('%dx%d+%d+%d' % (screen_shot_border_width, screen_shot_border_height, right, screen_shot_y))
    root.update()
    if right == screen_width:
        root.destroy()
    else:
        root.after(2, animate_right)

root.after(100, animate_left)
root.mainloop()
