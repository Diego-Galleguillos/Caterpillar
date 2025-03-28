import threading
from gpiozero import Button, RotaryEncoder
import time
from adafruit_motorkit import MotorKit
import socket
from pid import *


def steps_for_angle(steps_per_turn, angle):
    steps = (angle/360) * steps_per_turn
    return steps

class Pi_manager:
    def __init__(self, id):
        self.id = id
        self.kit = MotorKit()
        self.enc1 = RotaryEncoder(13, 16, max_steps=11400)
        self.enc2 = RotaryEncoder(19, 20, max_steps=300)
        self.previous_state = None
        self.count = 0
        self.start_time = time.time()
        self.previous_state2 = None
        self.count2 = 0
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('192.168.0.101', 9999))
        self.message = "Initial message from server."
        self.steps_per_turn = 1140
        self.overshoot = 0
        self.controller = PIDController(kp=0.00048, ki=0.0000045, kd=0.0000000001, setpoint=1140)
    def move_angle(self, steps_per_turn, angle, motor_number, direction = -1):
        steps = steps_for_angle(steps_per_turn, angle)
        steps = steps - self.overshoot
        self.count = 0
        self.count2 = 0
        self.enc1.steps = 0
        self.controller.set_setpoint(steps)
        if motor_number == 1:
            while True:
                print(self.count, self.count2, "in loop", self.controller.compute(self.count))
                self.kit.motor1.throttle = direction*self.controller.compute(self.count)
                if   abs(steps - self.count) < 10:
                    self.kit.motor1.throttle = 0
                    self.overshoot = self.count - steps
                    break
            self.kit.motor1.throttle = 0
        else:
            while self.count2 < steps:
                print(self.count2)
                self.kit.motor2.throttle = (steps_per_turn - self.count2)/(steps_per_turn*2) * direction
                time.sleep(0.001)
            self.kit.motor2.throttle = 0
    def receive_message(self):
        while "exit" not in self.message:
            data = self.client_socket.recv(1024).decode()
            self.message = data
            print(self.message)

            if "exit" in self.message:
                self.stop()
                break
            if "gait" in self.message:
                self.take_steps(self.steps_per_turn, 1, 1)
                print(self.count)
                self.client_socket.send(f"{self.id} - step finished".encode())
            else:
                try:
                    if int(self.message[0]) == self.id or int(self.message[0]) == 0:
                        print("taking step")
                        self.take_steps(self.steps_per_turn, int(self.message[2]), 1)
                except:
                    print("message too short")


    def take_steps(self, steps_per_turn, number_of_steps, motor_number):
        self.move_angle(steps_per_turn, number_of_steps*360, motor_number)

    def enc1_rotated(self):
        self.count = self.enc1.steps
        
    def enc2_rotated(self):
        self.count2 = self.enc2.steps


    def start(self):
        self.enc1.when_rotated = self.enc1_rotated
        self.enc2.when_rotated = self.enc2_rotated

        self.client_handler = threading.Thread(target=self.receive_message)
        self.client_handler.start()

    def stop(self):
        self.client_socket.close()
        self.client_handler.join()


if __name__ == "__main__":
    id = int(input("Enter the id of the pi: "))
    pi = Pi_manager(id)
    pi.start()

    while True:
        try:
            pass
        except KeyboardInterrupt:
            pi.stop()
            break

