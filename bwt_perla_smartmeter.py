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
import configparser

configParser = configparser.RawConfigParser()   
configFilePath = r'./perla.cfg'
configParser.read(configFilePath)

#print('from config: '+configParser.get('bwt','bwt_ipaddress'))

bwt_ipaddress=configParser.get('bwt','bwt_ipaddress')
bwt_password=configParser.get('bwt','bwt_password')
mqtt_address=configParser.get('mqtt','mqtt_address')
mqtt_user=configParser.get('mqtt','mqtt_user')
mqtt_pass=configParser.get('mqtt','mqtt_pass')
mqtt_topic=configParser.get('mqtt','mqtt_topic')

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

def send_capture(var_name, regex_exp, x_pos, y_pos, x_size, y_size):
    vncclient.captureRegion(var_name+'.png', x_pos, y_pos, x_size, y_size)
    output_file=pytesseract.image_to_string(Image.open(var_name+'.png'), lang = 'eng', config = '-c page_separator=""')
    #print(output_file)
    output_regex=re.search('(.*)'+regex_exp,output_file)
    old_value = globals()[var_name+'_old']
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

    #print("bwt value ", var_name)
    #print("old output ",old_value)
    #print("new output ",output_regex)
    if output_regex!=old_value and output_regex is not None:
        try:
            mqttclient.publish(mqtt_topic + var_name, payload=output_regex, qos=1, retain=False)
            print("+++ MQTT: Publish "+var_name+": ", output_regex)
        except:
            print("--- MQTT: Publish "+var_name+" failed!")
    globals()[var_name+'_old']=output_regex

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
    send_capture("throughput", "[Il1\|]*./[bh]", 60, 70, 75, 25)
    send_capture("volume", "[Il1\|]", 60, 148, 65, 25)
    send_capture("NaCl", "%", 198, 108, 45, 25)
    #print("### next sequence ###\n")
    
    # Keep VNC connection alive
    vncclient.mouseMove(400,0)
    vncclient.mouseDown(1)
    vncclient.mouseUp(1)
