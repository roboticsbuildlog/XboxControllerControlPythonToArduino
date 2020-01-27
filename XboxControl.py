#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Created on Wed Jan 15 18:47:58 2020

import serial
import time
import os
import subprocess


#https://www.roboticsbuildlog.com/hardware-control/xbox-one-controller-with-nvidia-jetson-nano


# ls -l /dev/ttyUSB0
#sudo usermod -a -G <userid>
#sudo chmod a+rw /dev/ttyUSB0

# Connect Xbox controller to Nano

#Enter the following commands to disable ertm, then go into Bluetooth settings on desktop.
#Succesful when light on controller is solid.

## Use xbox controller
#1. cat /sys/module/bluetooth/parameters/disable_ertm
#2. sudo bash -c "echo 1 > /sys/module/bluetooth/parameters/disable_ertm"
#3. cat /sys/module/bluetooth/parameters/disable_ertm
#4. Now go to Bluetooth settings on Desktop and add xbox controller.

## pip install evdev to read xbox
#https://python-evdev.readthedocs.io/en/latest/install.html
#sudo pip3 install evdev

##Find event file for xbox controller.
#cd /dev/input
#ls
#cat event<event no.>
#Move controller, data should show, if not check other events.



print('-------------------')
print('Disbale ERTM to enable bluetooth.')
print('-------------------')

output = subprocess.check_output("cat /sys/module/bluetooth/parameters/disable_ertm", shell=True)
print('Current value is :',output)

if output == b'N\n':
    print('ERTM Value is N, Attempting to change value.')
    os.system('sudo bash -c "echo 1 > /sys/module/bluetooth/parameters/disable_ertm"')
    print('Attempting to change ERTM value.')
    output = subprocess.check_output("cat /sys/module/bluetooth/parameters/disable_ertm", shell=True)
    print('New value is :', output)
    if output == b'Y\n':
        print('ERTM Value is Yes, Success.')
    else:
        print('ERTM Value is No, Something went wrong.')
elif output == b'Y\n':
    print('ERTM Value is Yes, no need to change.')


serialcomm = serial.Serial('/dev/ttyUSB0', 115200)

serialcomm.timeout = 1

def SendString():
    while True:

        i = input("Enter Input: ").strip()

        if i == "done":

            print('finished')

            break

        print('this printed')
        print('data entered :', i)
        print('data sent', i.encode())

        serialcomm.write(i.encode())

        time.sleep(0.1)

 #       print('data recv from arduino :',serialcomm.readline().decode('ascii'))

    serialcomm.close()


def ConnectXboxBT():
    print('----------------')
    print('Connecting xbox contoller...')

    from evdev import InputDevice

    try:
        dev = InputDevice('/dev/input/event3')
        print('----------')
        print(dev)
        print('----------')
        print(dir(dev))
        print('----------')
        print(dev.capabilities())
        print('----------')
        print(dev.capabilities(verbose=True))
        print('----------')
        print(dev.info)
        print('----------')
        print(dev.leds)
        print('----------')
        print(dev.name)
        print('----------')
        print(dev.path)
        print('----------')
        print(dev.phys)
        print('----------')

        #return dev
    except:
        print('----------------')
        print('The xbox controller was not detected. Is it turned on?')
        print('----------------')
        dev = 'False'

    return dev

def ReadXboxBT(dev):
    print('Press any button on Xbox. Y to EXIT.')
    while 1:
        try:
            xkey = dev.read_one()
            #print('key :', xkey)
            if xkey is not None:
                print('new command-----------------------------------------------')
                print('key :', xkey)
                print('key code :', xkey.code)
                print('key value :', xkey.value)
                print('key type :', xkey.type)
                if xkey.code == 304 and xkey.value == 1:
                    print('A button was pressed')
                elif xkey.code == 304 and xkey.value == 0:
                    print('A button was released')
                elif xkey.code == 305 and xkey.value == 1:
                    print('B button was pressed')
                elif xkey.code == 305 and xkey.value == 0:
                    print('B button was released')
                elif xkey.code == 307 and xkey.value == 1:
                    print('X button was pressed')
                elif xkey.code == 307 and xkey.value == 0:
                    print('X button was released')
                elif xkey.code == 308 and xkey.value == 1:
                    print('Y button was pressed')
                elif xkey.code == 308 and xkey.value == 0:
                    print('Y button was released')
                    break
                elif xkey.code == 315 and xkey.value == 1:
                    print('Start button was pressed')
                elif xkey.code == 315 and xkey.value == 0:
                    print('Start button was released')
                elif xkey.code == 17 and xkey.value == 1:
                    print('D Pad down button was pressed')
                elif xkey.code == 17 and xkey.value == 0:
                    print('D Pad button was released')   
                elif xkey.code ==  17 and xkey.value == -1:
                    print('D Pad up button was pressed')
                elif xkey.code == 16 and xkey.value == 1:
                    print('D Pad right button was pressed')
                elif xkey.code == 16 and xkey.value == 0:
                    print('D Pad button was released')   
                elif xkey.code ==  16 and xkey.value == -1:
                    print('D Pad Left button was pressed')
                elif xkey.code == 311 and xkey.value == 1:
                    print('Right Trigger upper was pressed')
                elif xkey.code == 311 and xkey.value == 0:
                    print('Right Trigger upper was released')
                elif xkey.code == 313 and xkey.value == 1:
                    print('Right Trigger lower was pressed')
                elif xkey.code == 313 and xkey.value == 0:
                    print('Right Trigger lower was released')
                elif xkey.code == 310 and xkey.value == 1:
                    print('Left Trigger upper was pressed')
                elif xkey.code == 310 and xkey.value == 0:
                    print('Left Trigger upper was released')
                elif xkey.code == 0 and xkey.type == 3:  # Left joystick, left and right.
                    print('----------')
                    print('Left joystick - X axis')
                    print('value', xkey.value)
                    print('----------')
                elif xkey.code == 1 and xkey.type == 3:  # Left joystick, up and down.
                    print('----------')
                    print('Left joystick - Y axis')
                    print('value', xkey.value)
                    print('----------')
                elif xkey.code == 2 and xkey.type == 3:  # Right joystick, left and right.
                    print('----------')
                    print('Right joystick - X axis')
                    print('value', xkey.value)
                    print('----------')
                elif xkey.code == 5 and xkey.type == 3:  # Right joystick, left and right.
                    print('----------')
                    print('Right joystick - Y axis')
                    print('value', xkey.value)
                    print('----------')
                elif xkey.code == 9 and xkey.type == 3:  #
                    print('----------')
                    print('Right Trigger Lower.')
                    print('value', xkey.value)
                    print('----------')
                elif xkey.code == 10 and xkey.type == 3:  #
                    print('----------')
                    print('Left Trigger Lower.')
                    print('value', xkey.value)
                    print('----------')
                elif xkey.code == 17 and xkey.value == 0:
                    print('Select was released')
        except:
            print('----------------')
            print('The xbox controller was not detected. Is it turned on?')
            print('Also check eventX is correct')
            print('----------------')
            break

def DriveManualXbox(dev):
    print('Y to stop, Left joystick fwd/rev, Right joystick left/right. Right Upper Trigger to Bump. Left Upper Trigger to take 25 images to video. Right trigger lower to increase bump pwm by 25.')

    i = 'Z'
    ilast = i
    while 1:
        if dev is not None:
            xkey = dev.read_one()
            #print('key :', xkey)
            if xkey is not None:
                #print('key :',xkey)
                print('key code :',xkey.code)
                print('key value :',xkey.value)
                #print('key type :',xkey.type)
                if xkey.code == 304 and xkey.value == 1:
                    print('A button was pressed')
                    i = 'J'
                elif xkey.code == 304 and xkey.value == 0:
                    print('A button was released')
                elif xkey.code == 305 and xkey.value == 1:
                    print('B button was pressed')
                    i = 'C'
                elif xkey.code == 305 and xkey.value == 0:
                    print('B button was released')
                elif xkey.code == 307 and xkey.value == 1:
                    print('X button was pressed')
                    i = 'G'
                elif xkey.code == 307 and xkey.value == 0:
                    print('X button was released')
                elif xkey.code == 308 and xkey.value == 1:
                    print('Y button was pressed')
                    print('Closing Arduino connection.')
                    serialcomm.close()
                    break
                elif xkey.code == 308 and xkey.value == 0:
                    print('Y button was released - Exiting manual mode')
                elif xkey.code == 17 and xkey.value == 1:
                    print('D Pad down button was pressed')
                    i = 'E'
                elif xkey.code == 17 and xkey.value == 0:
                    print('D Pad button was released')   
                elif xkey.code ==  17 and xkey.value == -1:
                    print('D Pad up button was pressed')
                    i = 'A'
                elif xkey.code == 16 and xkey.value == 1:
                    print('D Pad right button was pressed')
                    i = 'B'
                elif xkey.code == 16 and xkey.value == 0:
                    print('D Pad button was released')   
                elif xkey.code ==  16 and xkey.value == -1:
                    print('D Pad Left button was pressed')
                    i = 'H'
                elif xkey.code == 315 and xkey.value == 1:
                    print('Start button was pressed')
                    i = 'Z'
                elif xkey.code == 315 and xkey.value == 0:
                    print('Start button was released')
                elif xkey.code == 311 and xkey.value == 1:
                    print('Right Trigger upper was pressed - Bump car')
                elif xkey.code == 311 and xkey.value == 0:
                    print('Right Trigger upper was released')
                elif xkey.code == 313 and xkey.value == 1:
                    print('Right Trigger Lower.')
                elif xkey.code == 313 and xkey.value == 0:
                    print('Right Trigger lower was released')
                elif xkey.code == 310 and xkey.value == 1:
                    print('Left Trigger upper was pressed - Recording video')
                elif xkey.code == 310 and xkey.value == 0:
                    print('Left Trigger upper was released')
                elif xkey.code == 0 and xkey.type == 3:  # Left joystick, left and right.
                    print('Left joystick - X axis')
                elif xkey.code == 1 and xkey.type == 3:  # Left joystick, left and right.
                    print('Left joystick - Y axis')
                    print('value', xkey.value)
                    # Convert value to pwm
                    #Thrpwm = int(((-1100 / (65535)) * xkey.value) + 1800)
                    #print('Thrpwm before :', Thrpwm)
                    #Thrpwm = min(max(Thrpwm, 950), 1350) #Manual Max speed limits # New limits set in ESCServo def
                    #print('Thrpwm after :',Thrpwm)
                    #ESCservo(Thrpwm)
                    #print('----------')
                elif xkey.code == 2 and xkey.type == 3:  # Left joystick, left and right.
                    #print('----------')
                    print('Right joystick - X axis')
                    #print('value', xkey.value)
                    #SteeringValue = int((xkey.value/65535) * 320)
                    #Steeringservo(SteeringValue)
                elif xkey.code == 5 and xkey.type == 3:  # Left joystick, left and right.
                    #print('----------')
                    print('Right joystick - Y axis')
                elif xkey.code == 9 and xkey.type == 3:  # Left joystick, left and right.
                    #print('----------')
                    print('Right Trigger lower was pressed.')
                    #print('value', xkey.value)
                    #print('----------')
                elif xkey.code == 10 and xkey.type == 3:  # Left joystick, left and right.
                    #print('----------')
                    print('Left Trigger Lower.')
                    #print('value', xkey.value)
                    #print('----------')
                elif xkey.code == 17 and xkey.value == 0:
                    print('Select was released')

                #Send data to Arduino
                #i = input("Enter Input: ").strip()
                #if i == "done":
                #    print('finished')
                #    break
                print('----------')
                print('Data entered via Xbox :', i)
                if i != ilast:
                    print('Data sent to Arduino', i.encode())
                    serialcomm.write(i.encode())
                   # time.sleep(0.025)
                    ilast=i
        else:
            print('xbox not connected')
            break


if __name__ == "__main__":

    print('-------------------')
    print('Available disk space.')
    print('-------------------')

    print(os.system('df -h'))

    print('-------------------')
    print('Available events (xbox is 4/6).')
    print('-------------------')

    print(os.system('ls /dev/input/'))

    print('-------------------')
    print('Starting Main Menu loop.')
    print('-------------------')

    print('-------------------')
    print('Turn on Xbox controller now. (if required).')
    print('-------------------')

    dev = 'False'

    while 1:

        inp = int(input('1. Send String.\
        \n2. Drive car in Manual with Xbox\
        \n3. Connect Xbox via Bluetooth.\
        \n4. Read Xbox via Bluetooth.\
        \n5. Exit.\n'))

        # inp = 4

        if inp == 1:
            SendString()
        elif inp == 2:
            dev = ConnectXboxBT()
            if dev == 'False':
                print('---------------')
                print('The xbox was not detected. Is it turned on?')
                print('---------------')
            else:
                DriveManualXbox(dev)
        elif inp == 3:
            dev = ConnectXboxBT()
        elif inp == 4:
            if dev is not 'False':
                ReadXboxBT(dev)
            else:
                print('---------------')
                print('The xbox was not detected. Is it turned on?')
                print('---------------')
                dev = ConnectXboxBT()
                if dev is not 'False':
                    ReadXboxBT(dev)
        elif inp == 5:
            break

    print('----------------')
    print('Program End.')
    print('----------------')
