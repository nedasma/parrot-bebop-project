# droneDemo.py
#!/usr/bin/python3
import sys,tty,termios
from pyparrot.Bebop import Bebop
#from pyparrot.DroneVision import DroneVision
#from pyparrot.DroneVisionGUI import DroneVisionGUI
from pyparrot.utils.colorPrint import color_print
import math
import threading
import cv2
import time

# Python class for utilising the camera in the drone. Has a constructor and a
# function for saving images
class UserVision:
   def __init__(self, vision):
       self.index = 0
       self.vision = vision

   def save_pictures(self, args):
       img = self.vision.get_latest_valid_picture()
       if img is not None:
           filename = "test_image_%06d.png" % self.index
           self.index += 1

try:
   # for Python2
   from Tkinter import *   ## notice capitalized T in Tkinter
except ImportError:
   # for Python3
   from tkinter import *   ## notice lowercase 't' in tkinter here

fields = 'Roll', 'Pitch', 'Yaw', 'Duration'
bebop = Bebop(drone_type='Bebop2')
print("Setting up a connection...")
success = bebop.connect(10)
if(success):
   print("Connection set:", success)
   # Turns on the camera (WIP)
   #bebopVision = DroneVision(bebop, is_bebop = True)
   #userVision = UserVision(bebopVision)
   #bebopVision.set_user_callback_function(userVision.save_pictures, user_callback_args = None)
   #print("Turning on the video...")
   #bebop.start_video_stream()
   #suc = bebopVision.open_video()
   #if suc:
   #    color_print("Vision successfully started", "SUCCESS")
   #else:
   #    color_print("Vision cannot start, try again", "ERROR")

   # Start the drone for take-off
   print("Sleeping...")
   bebop.smart_sleep(2)

   bebop.ask_for_state_update()

   print("Prepare for take-off...")

   # Set safe indoor/outdoor parameters
   print("Set indoor parameters...")
   max_tilt = 15
   vertical_speed = 2#1.5
   max_altitude = 1.5
   max_rotation_speed = 150
   tilt_speed = 200
   bebop.set_max_tilt(max_tilt)
   bebop.set_max_vertical_speed(vertical_speed)
   bebop.set_max_altitude(max_altitude)
   bebop.set_max_rotation_speed(max_rotation_speed)
   bebop.set_max_tilt_rotation_speed(tilt_speed)
   color_print("Indoor parameters set: OK", "SUCCESS")

   # Get initial sensor data_type
   print("--------- SENSOR DATA ----------")
   print("Battery: ", bebop.sensors.battery, "%")
   print("Flying state:", bebop.sensors.flying_state)
   print("Altitude: ", max_altitude, " m")
   print("Pitch/roll rotation speed (degrees): ", tilt_speed)
   print("Tilt (degrees): ", max_tilt)
   print("Vertical speed: ", vertical_speed, " m/s")
   print("Yaw rotation speed (degrees): ", max_rotation_speed)
   print("--------------------------------")

   # Take-off the ground
   color_print("Take-off set: OK", "SUCCESS")
   bebop.safe_takeoff(10)
else:
   color_print("Connection failed: program closing", "ERROR")
   exit()

# Executes the command for 1 second
def direction(rollvalue, pitchvalue, yawvalue, altitude):
  print("Flying direct: Slow move for indoors")
  print("Status: ", bebop.sensors.flying_state)
  bebop.fly_direct(roll=rollvalue, pitch=pitchvalue, yaw=yawvalue, vertical_movement=altitude, duration=1)


def fetch(entries):
  values = [];
  for entry in entries:
     field = entry[0]
     text  = entry[1].get()
     number  = int(float(text))
     values.append(number)
     print('%s: "%d"' % (field, number))

  # Hull protector parameters - set to 1 for a hull protection and 0 without
  # protection (only works for bebop 1)
  #bebop.set_hull_protection(1)

  print("Flying direct: Slow move for indoors")
  print("Status: ", bebop.sensors.flying_state)
  bebop.fly_direct(roll=values[0], pitch=values[1], yaw=values[2], vertical_movement=0, duration=values[3])

# Take-off function
def takeoff():
  print("Status: ", bebop.sensors.flying_state)
  bebop.smart_sleep(3)
  bebop.safe_takeoff(10)

# Landing function
def landing():
  print("Status: ", bebop.sensors.flying_state)
  bebop.smart_sleep(3)
  bebop.safe_land(10)

# Back-flip function
def backflip():
  print("Status: ", bebop.sensors.flying_state)
  bebop.flip("back")
  bebop.smart_sleep(1)

# Front-flip function
def frontflip():
  print ("Status: ", bebop.sensors.flying_state)
  bebop.flip("front")
  bebop.smart_sleep(1)

# Function to disconnect the laptop from the drone
def disconnect():
   print("DONE - disconnecting")
   bebop.stop_video_stream()
   bebop.smart_sleep(5)
   print(bebop.sensors.battery, "% battery left")
   print("Status: ", bebop.sensors.flying_state)
   bebop.disconnect()
   color_print("Disconnected from the drone successfully", "SUCCESS")

def makeform(root, fields):
  entries = []
  for field in fields:
     row = Frame(root)
     lab = Label(row, width=15, text=field, anchor='w')
     ent = Entry(row)
     row.pack(side=TOP, fill=X, padx=5, pady=5)
     lab.pack(side=LEFT)
     ent.pack(side=RIGHT, expand=YES, fill=X)
     entries.append((field, ent))
  return entries

# Function to get the character from the keyboard
class _Getch:
   def __call__(self):
           fd = sys.stdin.fileno()
           old_settings = termios.tcgetattr(fd)
           try:
               tty.setraw(sys.stdin.fileno())
               ch = sys.stdin.read(1)
           finally:
               termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
           return ch

# Decode the character from I/O into a drone command
def get():
       # Get the character
       inkey = _Getch()
       # Poll for character from keyboard until there is one
       while(1):
               k=inkey()
               if k!='':break
       # "Switch" statement for each of drone commands
       if k=='w':
               print ("Forwards")
               direction(0,10, 0, 0)
       elif k=='s':
               print ("Backwards")
               direction(0, -10, 0, 0)
       elif k=='d':
               print ("Right")
               direction(10, 0, 0, 0)
       elif k=='a':
               print ("Left")
               direction(-10, 0, 0, 0)
       elif k =='e':
               print ("Yaw right")
               direction(0, 0, 5, 0)
       elif k =='q':
               print ("Yaw left")
               direction(0, 0, -5, 0)
       elif k == 'l':
               print ("Landing")
               landing()
       elif k == 't' and bebop.sensors.flying_state is not "hovering" or not "flying":
               print("Taking-off")
               takeoff()
       elif k == 'r':
               print("Climbing")
               direction(0, 0, 0, 5)
       elif k == 'f':
               print("Descending")
               direction(0, 0, 0, -5)
       elif k == 'b':
               print("Do a back-flip")
               backflip()
       elif k == 'n':
               print("Do a front-flip")
               frontflip()
       # This is not secured, one person can press c or k
       # and we might lost connection with drone whereas
       # this is in the air maybe someone can make something with this

       # Update: safety added for disconnecting and exiting the program
       # by polling the user for yes/no answer
       elif k == 'i':
               print ("Do you want to disconnect from the drone? (Y(es) or N(o))")
               ans = input()
               if ans == 'Y' or ans == 'y' or ans == 'Yes' or ans == 'yes':
                   print ("Disconnecting (don't forget to exit (q))")
                   #bebopVision.close_video()
                   disconnect()
               elif ans == 'N' or ans == 'n' or ans == 'No' or ans == 'no':
                   pass
               else:
                   print ("Please give a sensible answer! (Y(es) or N(o))")
       elif k == 'p':
               print ("Do you want to close the program? (Y(es) or N(o))")
               ans = input()
               if ans == 'Y' or ans == 'y' or ans == 'Yes' or ans == 'yes':
                   print ("Closing the program")
                   #bebopVision.close_video()
                   disconnect()
                   exit()
               elif ans == 'N' or ans == 'n' or ans == 'No' or ans == 'no':
                   pass
               else:
                   print ("Please give a sensible answer! (Y(es) or N(o))")
       # If something goes wrong, press ctrl+c to land the drone immediately
       elif ord(k) == 0x03:
               color_print("PANIC: initiating emergency landing", "ERROR")
               bebop.emergency_land()
               disconnect()
               exit()
       else:
               print ("Not defined! (Have you turned on Caps lock?)")

# Loop indefinitely to poll for character input unless the program is forced
# to close
if __name__ == '__main__':
   while(True):
       get()
   """
  print ("arg:"), sys.argv[0]
  root = Tk()
  print ('k');
  ents = makeform(root, fields)
  root.bind('<Return>', (lambda event, e=ents: fetch(e)))
  b1 = Button(root, text='Send',
         command=(lambda e=ents: fetch(e)))
  b1.pack(side=LEFT, padx=5, pady=5)
  b2 = Button(root, text='Quit', command=root.quit)
  b2.pack(side=LEFT, padx=5, pady=5)
  b3 = Button(root, text='Land', command=landing)
  b3.pack(side=LEFT, padx=5, pady=5)
  b4 = Button(root, text='disconnect', command=disconnect)
  b4.pack(side=LEFT, padx=5, pady=5)
  root.mainloop()
  """
