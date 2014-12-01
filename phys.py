from math import sin, cos

class launch(object):
    def __init__(self, angle, velocity, g=9.8):
        self.angle = angle
        self.velocity = velocity
        self.g = g
    @property
    def y_component(self):
        return self.velocity*sin(self.angle)
    @property
    def x_component(self):
        return self.velocity*cos(self.angle)
    @property
    def hang_time(self):
        return (self.y_component/-self.g) * 2
    @property
    def max_height(self):
        top = self.y_component/self.g
        return (self.velocity*top) + .5*-self.g*top**2
    def __repr__(self):
        return "a projectile launched at %s units per second %s units above the vertical" % (self.velocity, self.angle)
