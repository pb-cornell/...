


import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import numpy as np
import argparse
from time import sleep
from PIL import Image
import cv2
import pygame
import os
import subprocess
import sys
import pigpio
import subprocess


GPIO.setmode(GPIO.BCM)  

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  
GPIO.setup(5, GPIO.IN)
GPIO.setup(26, GPIO.IN)

camera = PiCamera()
# os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
# os.putenv('SDL_FBDEV', '/dev/fb1')
# os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
# os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
pygame.init()#pygame initialization
pygame.mouse.set_visible(False)
#RGB color
WHITE = 255, 255, 255
BLACK = 0,0,0
RED = 255,0,0
GREEN = 0,255,0
start_time=time.time()#tiem when program start
screen = pygame.display.set_mode((320, 240))




def noiseRemoval():

  global start_time
  start_time=time.time()
  # Reading Image
  img = cv2.imread("image.jpg")

  # RGB to Gray scale conversion
  img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

  noise_removal = cv2.bilateralFilter(img_gray,9,75,75)

  equal_histogram = cv2.equalizeHist(noise_removal)

  kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
  morph_image = cv2.morphologyEx(equal_histogram,cv2.MORPH_OPEN,kernel,iterations=15)

  sub_morp_image = cv2.subtract(equal_histogram,morph_image)

  # Thresholding
  ret,thresh_image = cv2.threshold(sub_morp_image,0,255,cv2.THRESH_OTSU)

def edgeDetect():

  # Applying Canny Edge detection
  canny_image = cv2.Canny(thresh_image,250,255)

  canny_image = cv2.convertScaleAbs(canny_image)
  kernel = np.ones((4,4), np.uint8)
  dilated_image = cv2.dilate(canny_image,kernel,iterations=10)

  # Finding Contours
  contours, hierarchy = cv2.findContours(dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  contours= sorted(contours, key = cv2.contourArea, reverse = True)[:10]
  screenCnt = None
  


  mask = np.zeros(img_gray.shape,np.uint8)
  new_image = cv2.bitwise_and(img,img,mask=mask)

# Applying histogram equalisation
def histoEqual():

  y,cr,cb = cv2.split(cv2.cvtColor(new_image,cv2.COLOR_BGR2YCR_CB))
  y = cv2.equalizeHist(y)
  
  final_image = cv2.cvtColor(cv2.merge([y,cr,cb]),cv2.COLOR_YCR_CB2BGR)
  final_new_image = new_image[top_idx:bottom_idx,left_idx:right_idx ]
  print(final_new_image.shape)

  im = final_new_image
  im[np.where((im <[20,20,20]).all(axis = 2))] = [255,255,255]

  gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
  open_out = cv2.morphologyEx(binl, cv2.MORPH_OPEN, kernel)
  cv2.bitwise_not(open_out, open_out)
  
  cv2.imwrite('output.jpg', open_out)


# main function starts here

flag=True
while flag:
    screen.fill(BLACK) 
    time.sleep(0.2) 
    rect = text_surface.get_rect(center=(160,60))
    screen.blit(text_surface, rect)
    pygame.display.flip()

    if ( not GPIO.input(19) ):#when button pressed pin connected to ground, GPIO.input(17)=0;
       
        
		  camera.resolution = (2592, 1944)
		  camera.framerate = 15
		  camera.start_preview()
		  camera.brightness = 50
		  camera.rotation=0
		  time.sleep(2)
		  camera.capture('capture.jpg')
		  camera.stop_preview()

        noiseRemoval() 
        edgeDetect()
        histoEqual()
        
        cmd="tesseract output2.jpg file -l eng -psm 7" 
    
        print subprocess.check_output(cmd, shell=True)
        

        f = open("file.txt","r")
        text = f.readline()
        f.close()


          time_servo=time.time()
  flag=1
  count=0
  try:
    while flag:
      time.sleep(0.2)

      screen.fill(BLACK) # Erase the Work space
      time.sleep(0.2)  # Without sleep, no screen output!
      text_surface = my_font.render(display, True, WHITE)#display Left servo History coloum
      rect = text_surface.get_rect(center=(160,30))
      screen.blit(text_surface, rect)

      #dispaly the captured image on piTFT
      imRec = imDisplay.get_rect()
      screen.blit(imDisplay, imRec) # Combine surface with workspace surface
      
    
      if((text=='BP424') 
        display="Success" 
        text_surface = my_font.render(display, True, WHITE)#display Left servo History coloum
        rect = text_surface.get_rect(center=(160,210))
        screen.blit(text_surface, rect)
        pygame.display.flip()#dispaly on actual screen 

      
        elif ( not GPIO.input(27) ):
          print (" ") 
          print "Button 27 has been pressed"
          flag=False

      else:
        display="Please charge"
        text_surface = my_font.render(display, True, WHITE)#display Left servo History coloum
        rect = text_surface.get_rect(center=(160,210))
        screen.blit(text_surface, rect)
        pygame.display.flip()
        if((time.time()-time_servo)>5):
          flag=False

        
    screen.fill(BLACK) # Erase the Work space
    pygame.display.flip()#dispaly on actual screen
  except KeyboardInterrupt:
      pass

  pi_hw.stop() 

                                                                                                                
    if ( not GPIO.input(27) ):
        print (" ") 
        print "Button 27 has been pressed system out"
        flag=False


GPIO.cleanup()