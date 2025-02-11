# Caterpillar


## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Wifi Access point](#Wifi_Access_point)
- [Contact](#contact)

## Introduction
In this repository you will find the setup steps and basic code to use the Rasberry Pi zero 2 w along side the Adafruit motor bonnets. There will also be code to handle the wifi communication between the Pi's and a publisher. Finally this setup guide will also show how to setup one of the Pi's as a wifi access point for use when now routers are available.



## Installation
To get started with the Pi's and the bonnets, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/Diego-Galleguillos/Caterpillar.git
    ```

2. Navigate to the project directory:
    ```bash
    cd Caterpillar
    ```

3. Install dependencies:
    ```bash
    sudo apt-get update

    sudo apt-get install -y python3-pip

    sudo apt-get install python3-rpi.gpio

    sudo apt-get install python3-gpiozero

    pip3 install adafruit-circuitpython-motorkit
    ```

When installing the adafruit-circuitpython-motorkit package an error might pop up, to solve this you can either create an enviroment and install it on said enviroment, or break system packages which will force the download:

    ```bash
    pip3 install adafruit-circuitpython-motorkit --break-system-packages
    ```

## Usage
In the example code, the publisher.py file will act as a server either on a PC or a Pi, and the pi.py file will run on the Pi's recieving commands and moving the motors on the robot.

To get everything going you must first get the publisher up
```bash
# Example command
python .\publisher.py
```
Then after selecting the amount of clients that will connect to the publisher, you can begin runing the code on the Pi's


```bash
# Example command
python .\pi.py
```