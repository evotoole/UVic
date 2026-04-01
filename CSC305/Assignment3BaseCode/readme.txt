-I have completed all components and all seem to match with the given .png's.
-libraries used: sys, numpy
program can be run in the following way:

>python3 RayTracer.py <filename>.txt

-program component descriptions:
classes.py: file that contains class definitions for the parsed data from the input file including: ViewScreen, Sphere, Light, Background, Ambient, Ray

-No function/globally defined components: 
Max depth for recursive algorithm = 3. 
user input is recieved using sys and the file is then opened and read.
Each feature is added to a list or dict containing features for each object of that group. instances of these objects are then created.

-helper function components:
def get_pixel_data() returns the VCS position for the center of the given pixel

def get_mat_sphere() returns the matrix for a given sphere scaling and translation.

def get_inv_mat_sphere() returns the inverse of the spheres transformation matrix, letting us move into unit sphere coordinates to find the intersection with the sphere.

-primary backwards ray tracing components
def intersect_sphere() returns the point and scaler for the intersection with the sphere in world coordinates, given the sphere object, origin position and pixel position (or just any two points that define the direction of the ray).

def check_shadow_ray() takes the light, point we are looking at, the sphere we are looking at, and the sphere we want to see if is blocking as input. it checks if there is a shadow ray for the given light and sphere, returning true if it blocks it and false if it doesn't block it.

def ADS() uses Phong to calculate ambience, diffusion, and specularity for the given light and sphere object.

def ray_trace() is the main recursive algorithm that stops once max depth is reached. it is called for every pixel and calls each of the previously mentioned functions on the first pass for the given pixel. it checks if there is a sphere for the pixel or if it is just background. it then checks what lights hit it, ie if it is in a shadow or not, and what colors the light produces for the given light and surface color etc. for the sphere and light. This finds the RGB intensity for the given pixel (for ADS). The reflection is then calculated recursively if the sphere is refelctive. it has max depth = 3.

