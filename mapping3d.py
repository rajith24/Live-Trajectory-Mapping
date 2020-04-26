#!/usr/bin/env python

# Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import glob
import os
import sys

try:
    sys.path.append(glob.glob('C:\Temp\CARLA_0.9.5\PythonAPI\carla\dist\carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla
import random
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style 
from mpl_toolkits.mplot3d import axes3d


def main():
    actor_list=[]
    vehicle_list=[]
    style.use('fivethirtyeight')
    client = carla.Client('localhost', 2000) ##### Connect to the IP address of System in which Carla is Running
    client.set_timeout(5.0) ###### 5 seconds time limit for waiting to connect to host IP
    world = client.get_world()  ##### Gets the town running in Carla Environment (example: Town1 or Town3 or ...)
    map=world.get_map()
    spawnpoints = map.get_spawn_points() ##### Get available vehicle spawn points in a given Carla Environment

    #### Destroys available actors that is already exist in Carla environment before launching
    for a in world.get_actors().filter("vehicle*"):
        if a.is_alive:
            a.destroy()
    for a in world.get_actors().filter("sensor*"):
        if a.is_alive:
            a.destroy()


    blueprint_library = world.get_blueprint_library()
    car = random.choice(blueprint_library.filter('vehicle.tesla.model3'))  #### Chooses a Vehicle model available in Carla as "Tesla"
    spawn_point = carla.Transform(carla.Location(7.603518,-43.829613,1.843102),carla.Rotation(0,-88.586418,0)) #### Point at which we need the vehicle to spawn
    vehicle2=world.spawn_actor(car, spawn_point) #### Spawns our vehicle model at the given location

    weather = carla.WeatherParameters(
        cloudyness=0.0,
        precipitation=0.0,
        sun_altitude_angle=60.0)
    world.set_weather(weather)  ##### Sets the Carla environment weather as needed for better visualization
    world.wait_for_tick()
    vehicle2.set_autopilot(True)
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    '''a=vehicle2.get_location()
    #plt.plot(a.x,a.y)
    print(a.x)
    plt.plot(a.x, a.y, color='green', linestyle='dashed', linewidth = 3, 
         marker='o', markerfacecolor='blue', markersize=12)
    plt.show()'''
    #time.sleep(2)
    def talker(i):
        a=vehicle2.get_location()
        xp=[]
        yp=[]
        zp=[]
        #plt.plot(a.x,a.y)
        '''plt.plot(a.x, a.y, color='green', linestyle='dashed', linewidth = 3, 
         marker='o', markerfacecolor='blue', markersize=12) 
        #plt.show()
        print(a.x)'''
        xp.append(a.x)
        yp.append(a.y)
        zp.append(np.array([[a.z],[a.z]]))
        #ax1.clear()
        #ax1.plot_wireframe(xp[0],yp[0],zp[0], color='green', linestyle='dashed', linewidth = 3)
        ax1.scatter(xp[0],yp[0],zp[0], c='g', marker='o')
        #ax1.plot(xp[0],yp[0],zp[0], rstride=2, cstride=2)
    
    #talker()
    ani = animation.FuncAnimation(fig, talker, interval=10)
    plt.show()
    #time.sleep(1)

if __name__ == '__main__':

    main()


