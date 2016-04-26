import RPi.GPIO as GPIO, time, os
import paho.mqtt.client as mqtt
GPIO.setmode(GPIO.BCM)

configfile = '/Users/Rii/Documents/cmpe296A/LabAssignment/lab/RasPi/PiConfig.config'

TRIG = 23
ECHO = 24
LIGHT = 4
LED = 22
devicestate = 'true'
threshold = '100'

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))  

client = mqtt.Client()
client.on_connect = on_connect

client.connect(host="54.153.75.253", port=1883, keepalive=60, bind_address="")


print "Distance Measurement running..."

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(LED,GPIO.OUT)
GPIO.output(TRIG, True)


while True:
    
    config_file = open(configfile, 'r')
    lines = config_file.readlines()
    thresholdtemp = lines[0].split("=")
    devicestatestring = lines[1].split("=")
    threshold = str(thresholdtemp[1].strip())
    devicestate = str(devicestatestring[1].strip())
    print 'threshold : ' + str(threshold)
    print 'devicestate : ' + str(devicestate)        
    if devicestate == 'true':
        reading = 0
        GPIO.output(LED,GPIO.HIGH)
        GPIO.setup(LIGHT, GPIO.OUT)
        GPIO.output(LIGHT, GPIO.LOW)
        time.sleep(0.1)
        GPIO.setup(LIGHT, GPIO.IN)
    
        while (GPIO.input(LIGHT) == GPIO.LOW):
            reading += 1
    
        GPIO.output(TRIG, False)
        print "Waiting For Sensor To stabalize"
        time.sleep(1)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
    
        while GPIO.input(ECHO)==0:
            pulse_start = time.time()
    
        while GPIO.input(ECHO)==1:
            pulse_end = time.time()
    
        pulse_duration = pulse_end - pulse_start
    
        distance = pulse_duration * 17150
    
        distance = round(distance, 2)
        light_value = reading
    
        print "Distance is:",distance,"cm"
        print "Light value :" ,light_value      
            
        
        piMessage = '{"Dist_Value": ' + str(distance) + ', "Light_Value": ' + str(light_value) + '}'
        
        notifmsg = '{"message": "Entity is at ' + str(distance) + ' cm. Threshold value is ' + threshold + ' cm"}'
        client.publish("piData", piMessage)

        
        if int(distance) < int(threshold):
            client.publish("Notif", notifmsg)
    else:
        GPIO.output(LED,GPIO.LOW)
            
    sensorState = '{"PiState": '+ devicestate + ', "ThresVal": ' + threshold + '}'
    client.publish("State", sensorState)
    config_file.close()