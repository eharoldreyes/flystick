import pygame.joystick


class Ch(object):
    """Implements channel mixing.

    Mix examples:

        Reverse:
            -stick.axis(0)

        Offset:
            stick.axis(0) - 0.1

        Weight:
            stick.axis(0) * 0.5

        Mixing:
            stick.axis(0) - stick.axis(1) * 0.5

        Trim:
            stick.axis(0) - Switch(..) * 0.5

        Reverse + offset + weight + trim:
            (-stick.axis(0) + 0.1) * 0.7 - Switch(..) * 0.5

    Also a shortcut to scale the output to range [0..1]
    instead of the normal [-1..1]:
        +stick.axis(0)
    """
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, evts):
        return self.fn(evts)

    def __neg__(self):
        return Ch(lambda evts: -self.fn(evts))

    def __add__(self, x):
        if isinstance(x, float):
            return Ch(lambda evts: self.fn(evts) + x)
        elif isinstance(x, Ch):
            return Ch(lambda evts: self.fn(evts) + x(evts))
        else:
            raise ValueError("Invalid positive offset %r" % (x,))

    def __sub__(self, x):
        if isinstance(x, float):
            return Ch(lambda evts: self.fn(evts) - x)
        elif isinstance(x, Ch):
            return Ch(lambda evts: self.fn(evts) - x(evts))
        else:
            raise ValueError("Invalid negative offset %r" % (x,))

    def __mul__(self, x):
        if isinstance(x, float):
            return Ch(lambda evts: self.fn(evts) * x)
        elif isinstance(x, Ch):
            return Ch(lambda evts: self.fn(evts) * x(evts))
        else:
            raise ValueError("Invalid weight %r" % (x,))

    def __pos__(self):
        return Ch(lambda evts: .5 + self.fn(evts) / 2)


class Joystick(object):
    """A base class for setting up mapping of different axes and buttons
    of a joystick.
    """
    def __init__(self, joy_id):
        pygame.joystick.init()
        self._joy = pygame.joystick.Joystick(joy_id)
        self._joy.init()

    def axis(self, axis):
        return Ch(lambda evts: self._joy.get_axis(axis))

    def button(self, button):
        return Ch(lambda evts: 1. if self._joy.get_button(button) else -1.)

    def hat_switch(self, hat, axis, **switch):
        def hat_values(hats):
            for evt in hats:
                if evt.joy == self._joy.get_id() \
                   and evt.hat == hat:
                    yield evt.value[axis]
        return Ch(Switch(evt_map=lambda (clicks, hats): hat_values(hats),
                         **switch))


class Switch(object):
    """Models a virtual multi-position switch. Excellent for example
    trims and flight mode control.
    """
    def __init__(self, evt_map, positions, initial=0):
        self.evt_map = evt_map
        self.positions = positions
        self.pos = initial

    def __call__(self, evts):
        for value in self.evt_map(evts):
            if value > 0:
                self.pos = (self.pos + 1) % self.positions
            elif value < 0:
                self.pos -= 1
                if self.pos < 0:
                    self.pos += self.positions
            # ignore zero
        return 2. * self.pos / (self.positions - 1) - 1
