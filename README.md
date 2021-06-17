# Autonomous-Car-Project
## Authors
Jonathan Chesney, Joshua Rossie, Paul Takhar through the University of California, Davis

## Introduction
Self-driving cars are an emerging technology that have gained worldwide attention and will likely forever change modern transportation.

#### How does a car drive itself?
The car has to have a way to know where it is and make decisions based on that knowledge. In essence, a Negative Feedback System. 

#### Goal:
To design an autonomous car that can follow a track within certain bounds, as well as recognize certain conditions, such as when to stop.

## Design Solution
In order to give the car the abilities described above, we used the Open MV Cam H7. This is a microcontroller with a mounted camera, giving us both parameters described: the ability to know its position (the mounted camera) and the ability to make decisions based on this knowledge (the microcontroller).

## Methodology
The first problem we tackled was making sure that the microcontroller had a way to control the motors of the car, so we designed a motor control PCB in Altium. After the PCB was set up and ready to go, COVID supply shortages required us to change car chassis at the last minute, rendering our PCB incompatible. Luckily, the Romi chassis has a motor control PCB of its own. Following that we worked on the camera detection, where we used white bundles of pixels (“blobs”) to identify a white line that acts as a track. Knowing the location of the “blobs,” we then were able to code a PI controller that adjusts the speeds of the chassis motors based on the Open MV’s self-identified position on the track. This allowed the car the ability to immediately respond to changes in the track (such as turns), using the proportional controller, and to gain steady state accuracy on straightaways on the track, using the integral controller. Also, the microcontroller would detect if there were three lines in parallel, signaling the stop condition.

## Results
After extensive testing and optimization, we achieved autonomous track times of 8, 23.3, and 34.6 seconds on the small carpeted, medium sized foam floored, and the large carpeted tracks, respectively.

Track Times:
Track Type | Time (seconds)
-----------|---------------
Small Carpeted | 8.0
Medium Foam | 23.3
Large Carpeted | 34.6
*Table 1: Track times by track type*

The obstacle detection and evasion feature allowed the car to successfully avoid obstacles, marginally impacting track times.

## Innovation Feature
Our innovation feature implemented an obstacle detection/evasion system. With data obtained from the HC-SR04 ultrasound sensor, we could determine the distance to obstacles in software. Obstacles detected at distances of less than 20 cm prompted the car to perform a 180 degree turn in the direction from which it came, successfully evading the obstacle.
