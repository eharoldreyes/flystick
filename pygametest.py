import pygame

pygame.display.init()
pygame.joystick.init()
pygame.joystick.Joystick(0).init()

# Get the name of the joystick and print it
JoyName = pygame.joystick.Joystick(0).get_name()
print "Name of the joystick:"
print JoyName

# Get the number of axes
JoyAx = pygame.joystick.Joystick(0).get_numaxes()
print "Number of axis:"
print JoyAx

# Print the values for the axes
pygame.event.pump()
print pygame.joystick.Joystick(0).get_axis(0)
print pygame.joystick.Joystick(0).get_axis(1)
print pygame.joystick.Joystick(0).get_axis(2)
print pygame.joystick.Joystick(0).get_axis(3)