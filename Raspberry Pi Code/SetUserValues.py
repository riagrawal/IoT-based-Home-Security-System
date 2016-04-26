import paho.mqtt.client as mqtt
import os

configfile_path = '/Users/Rii/Documents/cmpe296A/LabAssignment/lab/RasPi/PiConfig.config'



def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("SetUserThreshold")
    client.subscribe("SetUserSensorState")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    
    if msg.topic == "SetUserThreshold":
        tempThresholdValue = 'Threshold = ' + str(int(msg.payload)*100) + '\n'
        mode_value = 'a' if os.path.exists(configfile_path) else 'w'
        with open(configfile_path, mode_value) as f:
            replace_line(configfile_path, 0, tempThresholdValue)
            
    if msg.topic == "SetUserSensorState":
        tempSensorStateValue = 'SensorState = ' + str(msg.payload) + '\n'      
        mode_value = 'a' if os.path.exists(configfile_path) else 'w'
        with open(configfile_path, mode_value) as f:
            replace_line(configfile_path, 1, tempSensorStateValue)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("54.153.75.253", 1883, 60)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
