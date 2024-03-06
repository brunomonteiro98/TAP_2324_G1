import pygame


# init joystick in pygame
def joystick_init():
    pygame.init()

    # 获取joystick个数
    pygame.joystick.init()
    num_of_joystick = pygame.joystick.get_count()
    return num_of_joystick


class Joystick(object):
    # create a joystick and get some key values (left axis, button A, B, LB, and RB)
    def __init__(self, index):
        self.joystick = pygame.joystick.Joystick(index)
        self.joystick.init()
        self.axis1 = 0
        self.axis2 = 0
        self.buttonA = 0
        self.buttonB = 0
        self.buttonLB = 0
        self.buttonRB = 0

    # updates key values everytime invoked
    def get_buttons(self):
        for event in pygame.event.get():
            pass

        self.axis1 = self.joystick.get_axis(0)
        self.axis2 = self.joystick.get_axis(1)

        self.buttonA = self.joystick.get_button(0)
        self.buttonB = self.joystick.get_button(1)
        self.buttonLB = self.joystick.get_button(4)
        self.buttonRB = self.joystick.get_button(5)

        return self.axis1, self.axis2, self.buttonA, self.buttonB, self.buttonLB, self.buttonRB
