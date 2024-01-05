# original by d3monxxl 
# improved by drohhyn

from vncdotool import api
import time
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import re
import paho.mqtt.client as mqtt

bwt_ipaddress="192.168.0.mmm"
bwt_password="passwd"
mqtt_address="192.168.0.nnn"
mqtt_user="mqttuser"
mqtt_pass="mqttpass"
mqtt_topic="water/bwt/"

#def bwt_connect():
vncclient = api.connect(bwt_ipaddress, password=None)

def bwt_login():
    vncclient.mouseMove(160,105)
    vncclient.mouseDown(1)
    vncclient.mouseUp(1)
    vncclient.mouseMove(50,50)
    vncclient.mouseDown(1)
    vncclient.mouseUp(1)
    vncclient.keyPress(bwt_password[0])
    vncclient.keyPress(bwt_password[1])
    vncclient.keyPress(bwt_password[2])
    vncclient.keyPress(bwt_password[3])
    vncclient.keyPress(bwt_password[4])
    vncclient.keyPress(bwt_password[5])
    vncclient.mouseMove(295,215)
    vncclient.mouseDown(1)
    vncclient.mouseUp(1)
    vncclient.mouseMove(295,215)
    vncclient.mouseDown(1)
    vncclient.mouseUp(1)

def send_capture(var_name, var_name_old, regex_exp, x_pos, y_pos, x_size, y_size):
    vncclient.captureRegion(var_name+'.png',x_pos,y_pos,x_size,y_size)
    output_file=pytesseract.image_to_string(Image.open(var_name+'.png'),lang = 'eng',config = '-c page_separator=""')
    #print(output_file)
    output_regex=re.search('(.*)'+regex_exp,output_file)
    #print(var_name+" output_regex:",output_regex)
    if output_regex:
        output_regex=output_regex.group(1)
        output_regex=output_regex.strip()
        if output_regex=="O":
            output_regex=0
        #print(var_name+" output:",output_regex)
    else:
        print('OCR '+var_name+' failed')
        print('Trying to re-login')
        bwt_login()
    if output_regex!=var_name_old:
        #print("MQTT: Publish throughput: ",throughput)
        try:
            mqttclient.publish(mqtt_topic + var_name, payload=output_regex, qos=1, retain=False)
        except:
            print("MQTT: Publish throughput failed!")
        var_name_old=output_regex

bwt_login()

mqttclient=mqtt.Client()
mqttclient.username_pw_set(mqtt_user, mqtt_pass)
mqttclient.connect(mqtt_address, 1883, 20)
mqttclient.loop_start()
mqttclient.reconnect_delay_set(min_delay=1, max_delay=120)
throughput_old=-1
volume_old=-1
NaCl_old=-1
while True:
    # Capture regions
    send_capture("throughput", throughput_old, "[Il1\|]*./[bh]", 50, 70, 90, 25)
    send_capture("volume", volume_old, "[Il1\|]", 60, 150, 80, 25)
    send_capture("NaCl", NaCl_old, "%", 198, 108, 45, 25)
    
    # Keep VNC connection alive
    vncclient.mouseMove(400,0)
    vncclient.mouseDown(1)
    vncclient.mouseUp(1)
