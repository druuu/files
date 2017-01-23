import time, sys
import random
from subprocess import check_output, check_call
from PIL import Image as pil_image


home_dir = (check_output('echo $HOME', shell=True)).strip('\n')
activity_dir = home_dir+'/.microtrack'
project_name = sys.argv[1]
while True:
    check_call(['python', 'screen_shot.py', project_name, activity_dir])

    try:
        resize_img = pil_image.open('123456.png')
    except:
        pass
    else:
        resize_img = resize_img.resize((533, 300), pil_image.ANTIALIAS)
        resize_img.save('%s/%d_%s.png' % (activity_dir, int(time.time()), project_name))
        check_call('rm 123456.png', shell=True)
    #requests.post(upload_url, data={'project_name': project_name}, \
    #        files={'ss': open(activity_dir+'123456.png', 'rb')}, \
    #        headers={'Authorization': authorization})
    time.sleep(random.randint(60, 300))
