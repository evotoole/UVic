class ViewScreen:
    def __init__(self, near, left, right, bottom, top, res_x, res_y):
        self.near = near
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        self.res_x = res_x
        self.res_y = res_y


class Sphere:
    def __init__(self, sphere_data):
        self.name = sphere_data[1]
        self.pos_x = sphere_data[2]
        self.pos_y = sphere_data[3]
        self.pos_z = sphere_data[4]
        self.scl_x = sphere_data[5]
        self.scl_y = sphere_data[6]
        self.scl_z = sphere_data[7]
        self.r = sphere_data[8]
        self.g = sphere_data[9]
        self.b = sphere_data[10]
        self.ka = sphere_data[11]
        self.kd = sphere_data[12]
        self.ks = sphere_data[13]
        self.kr = sphere_data[14]
        self.n = sphere_data[15]

class Light:
    def __init__ (self, light_data):
        self.name = light_data[1]
        self.pos_x = light_data[2]
        self.pos_y = light_data[3]
        self.pos_z = light_data[4]
        self.ir = light_data[5]
        self.ig = light_data[6]
        self.ib = light_data[7]

class Background:
    def __init__(self, bg_data):
        self.r = bg_data[1]
        self.g = bg_data[2]
        self.b = bg_data[3]

class Ambient:
    def __init__(self, amb_data):
        self.ir = amb_data[1]
        self.ig = amb_data[2]
        self.ib = amb_data[3]