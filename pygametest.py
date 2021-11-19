import pygame

pygame.display.init()
pygame.joystick.init()


js0 = pygame.joystick.Joystick(0)
js0.init()

# Prints the joystick's name
JoyName = js0.get_name()
print "Name of the joystick:"
print JoyName
# Gets the number of axes
JoyAx = js0.get_numaxes()
print "Number of axis:"
print JoyAx

# Prints the values for axis0
while True:
        pygame.event.pump()
        print(
        	"axis 0 " + str(js0.get_axis(0)) + 
        	" axis 1 " + str(js0.get_axis(1))  + 
        	" axis 2 " + str(js0.get_axis(2))  + 
        	" axis 3 " + str(js0.get_axis(3)) 
        )