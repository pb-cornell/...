
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import time

#configure output
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

#freq = 50HZ, so one blink per second
p1 = GPIO.PWM(5, 50)
p2 = GPIO.PWM(6, 50)

#duty cycle of 7.5%
p1.start(7.5)
p2.start(7.5)

#servos[0]=p1;servos[1]=p2
servos = [p1, p2]

#set a flag to change p1 or p2
flag = True

GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_UP)   
GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_UP)  
GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#definition the method in each callback function

def GPIO17_callback(channel):
	servos[flag].ChangeDutyCycle(0)
	
def GPIO22_callback(channel):
	servos[flag].ChangeDutyCycle(8.5)
	
def GPIO23_callback(channel):
	servos[flag].ChangeDutyCycle(6.5)

def GPIO27_callback(channel):
	global flag
	flag = not flag
	

GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=300)

try: 
	#running in the loop 
	while 1:
		pass
	
except KeyboardInterrupt:
	pass

finally:
	p1.stop()
	p2.stop()
	GPIO.cleanup()
