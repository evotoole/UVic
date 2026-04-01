import sys
from classes import *
import numpy as np

plane_data = {}
sphere_list = []
light_list = []

MAX_DEPTH=3

if len(sys.argv) > 1:
    filename = sys.argv[1]
    print(f"filename recieved: \"{filename}\"")
else:
    print("no file name found")

with open(filename, 'r') as file:
    for i, line in enumerate(file):
        
        temp_arr = line.split()
        #print(temp_arr)
        if (temp_arr):
            if temp_arr[0] == "NEAR":
                plane_data["near"] = temp_arr[1]
            elif temp_arr[0] == "LEFT":
                plane_data["left"] = temp_arr[1]
            elif temp_arr[0] == "RIGHT":
                plane_data["right"] = temp_arr[1]
            elif temp_arr[0] == "BOTTOM":
                plane_data["bottom"] = temp_arr[1]
            elif temp_arr[0] == "TOP":
                plane_data["top"] = temp_arr[1]
            elif temp_arr[0] == "RES":
                plane_data["res_x"] = temp_arr[1]
                plane_data["res_y"] = temp_arr[2]
            elif temp_arr[0] == "SPHERE":
                sphere_list.append(Sphere(temp_arr))
            elif temp_arr[0] == "LIGHT":
                light_list.append(Light(temp_arr))
            elif temp_arr[0] == "BACK":
                background = Background(temp_arr)
            elif temp_arr[0] == "AMBIENT":
                ambience = Ambient(temp_arr)
            elif temp_arr[0] == "OUTPUT":
                output_name = temp_arr[1]
          
viewscreen = ViewScreen(
    plane_data["near"],
    plane_data["left"],
    plane_data["right"],
    plane_data["bottom"],
    plane_data["top"],
    plane_data["res_x"],
    plane_data["res_y"]
)


color_line1 = [0,0,0,255]



def get_pixel_data(i,j):
    near_y = 1-  (i + 0.5 )/int(viewscreen.res_y) #+0.5 to make sure we are refering to the center of the pixel
    near_x = (j + 0.5)/int(viewscreen.res_x)  #+0.5 to make sure we are refering to the center of the pixel

    view_x = float(viewscreen.left) + near_x * (float(viewscreen.right) - float(viewscreen.left))
    view_y = float(viewscreen.bottom) + near_y * (float(viewscreen.top) - float(viewscreen.bottom)) #map on to the near plane in world
    view_z = -float(viewscreen.near) #map on to the near plane in world
    return np.array([view_x,view_y,view_z,1])
            

def ray_trace(origin, direction, depth):
    if depth > MAX_DEPTH:
        return np.array([0,0,0])
    
    

    final = None
    for sphere in sphere_list:
        if depth > 0:
            temp = intersect_sphere(origin, origin + direction, sphere, True)
        else:
            temp = intersect_sphere(origin, origin + direction, sphere)
        
        if temp:
            if final is None or temp[0] < final[0]:
                final = [temp[0], temp[1], sphere]

    #nothing then do background
    if final is None:
        if depth == 0:
            return [background.r, background.g, background.b]
        else:
            return np.array([0,0,0])

    hit_point = final[1]
    hit_sphere = final[2]

    spec = np.array([0.0,0.0,0.0])
    diff = np.array([0.0,0.0,0.0])

    #calculat the ambience
    sphere_color = np.array([float(hit_sphere.r), float(hit_sphere.g), float(hit_sphere.b)])
    amb = sphere_color * float(hit_sphere.ka) * np.array([float(ambience.ir), float(ambience.ig), float(ambience.ib)])

    for light in light_list:
        in_shadow = False

        for sphere in sphere_list:
            if sphere == hit_sphere and hit_point[-1] != 2:
                continue
            
            shadow_hit = check_shadow_ray(light, hit_point, hit_sphere, sphere)  # <- changed
            if shadow_hit:
                in_shadow = True
                break

        if not in_shadow:
            t_spec, ignore, t_diff = ADS(hit_sphere, hit_point, light, origin)
            spec += t_spec
            diff += t_diff

    color = amb + spec + diff

    #compute reflection ray
    kr = float(hit_sphere.kr)
    Ir = np.array([0,0,0])
    if (kr > 0):
        inv_mat = get_inv_mat_sphere(hit_sphere)
        inv_transpose = np.transpose(inv_mat)
        
        P_obj = np.matmul(inv_mat, np.array([hit_point[0], hit_point[1], hit_point[2], 1]))
        if hit_point[-1] == 2:
            N_obj = np.array([-P_obj[0], -P_obj[1], -P_obj[2], 0])
        else:
            N_obj = np.array([P_obj[0], P_obj[1], P_obj[2], 0])
        N_world = np.matmul(inv_transpose, N_obj)
        n = N_world[:3] / np.linalg.norm(N_world[:3])

        v = -direction[:3] / np.linalg.norm(direction[:3])
        R = 2 * np.dot(n[:3], v) * n[:3] - v
        R_4d = np.array([R[0], R[1], R[2], 0])
        offset_origin = hit_point[:3] + 0.0001 * R
        offset_origin_4d = np.array([offset_origin[0], offset_origin[1], offset_origin[2], 1])
        print(f"R direction: {R_4d}, offset_origin: {offset_origin_4d}")
        Ir = ray_trace(offset_origin_4d, R_4d, depth + 1)
        print(f"Ir: {Ir}, hit_sphere: {hit_sphere.name}")
        print(f"n: {n[:3]}, v: {v}")
        #print(Ir)
 
            

    return np.clip(color + kr * Ir, 0, 1)



def ADS(sphere, point, light, origin): #input the point of intersection on the sphere to find the normal the surface. light finds the vector to the light. input origin to find direction of the eye.
    sphere_pos = np.array([float(sphere.pos_x),float(sphere.pos_y),float(sphere.pos_z)])
    light_pos = np.array([float(light.pos_x), float(light.pos_y), float(light.pos_z)])
    coord_point = point[-1]
    point = point[:3]
    origin = origin[:3]

    inv_mat = get_inv_mat_sphere(sphere)
    inv_transpose = np.transpose(inv_mat)

    P_obj = np.matmul(inv_mat, np.array([point[0], point[1], point[2], 1]))
    if coord_point == 2:
        N_obj = np.array([-P_obj[0], -P_obj[1], -P_obj[2], 0])
    else:
        N_obj = np.array([P_obj[0], P_obj[1], P_obj[2], 0])
    
    N_world = np.matmul(inv_transpose, N_obj)[:3]

    n = N_world / np.linalg.norm(N_world)

    L = light_pos - point
    l = L / np.linalg.norm(L)

    V = origin - point
    v = V / np.linalg.norm(V)

    R = 2 * np.dot(n, l) * n - l
    r = R / np.linalg.norm(R)

    na = np.array([0,0,0])
    if np.dot(n,l) <=0:
        return (na, na, na)

    sphere_color_intensity = np.array([float(sphere.r),float(sphere.g),float(sphere.b)])
    light_color_intensity = np.array([float(light.ir),float(light.ig),float(light.ib)])


    specular_intensity = light_color_intensity * float(sphere.ks) * (max(0, np.dot(v, r)) ** float(sphere.n))
    ambient_intensity = sphere_color_intensity * float(sphere.ka)
    diffuse_intensity = light_color_intensity * sphere_color_intensity * float(sphere.kd) * max(0, np.dot(n, l))
    
    
    return specular_intensity, ambient_intensity, diffuse_intensity


def intersect_sphere(origin_pos, pixel_pos, sphere: Sphere, is_shadow=False): #pixel pos should be 4D point coordinats homogenous.
    #origin_pos = np.array([int(origin.pos_x),int(origin.pos_y),int(origin.pos_z)])
    #origin_pos = np.array([0,0,0,1])
    ray_vec = pixel_pos - origin_pos #for camera to pixel direction

    inv_mat = get_inv_mat_sphere(sphere)
    trans_origin_pos = np.matmul(inv_mat, origin_pos)
    trans_ray_vec = np.matmul(inv_mat, ray_vec)

    a = np.dot(trans_ray_vec[:3], trans_ray_vec[:3])
    b = 2 * np.dot(trans_ray_vec[:3], trans_origin_pos[:3])
    c = np.dot(trans_origin_pos[:3], trans_origin_pos[:3]) - 1 

    quadratic = np.array([a,b,c])
    solution_arr = np.roots(quadratic)
    
    solution_arr = np.real(solution_arr[np.isreal(solution_arr)]) #make sure quadratic solution is real
    solution_arr = solution_arr[solution_arr > 0.0001] #filter such that the solution is positive.
    
    if len(solution_arr) == 0 or (np.min(solution_arr) < 1 and np.max(solution_arr)<1 and not is_shadow): #if there is no intersection with the sphere then move on.
        return None

    t = np.min(solution_arr)
    
    P = origin_pos + t * ray_vec #solve for point of intersection by plugging t into original equation
    P[-1] = 1
    if P[-2] > -1:
        t2 = np.max(solution_arr)
        p2 = origin_pos + t2 * ray_vec
        if (p2[-2] <= -1):
            p2[-1] = 2
            return (t2,p2)

    return (t, P) #return the point of intersection and the solved t value.




def get_mat_sphere(sphere):
    return np.array([
        [float(sphere.scl_x), 0, 0, float(sphere.pos_x)],
        [0, float(sphere.scl_y), 0, float(sphere.pos_y)],
        [0, 0, float(sphere.scl_z), float(sphere.pos_z)],
        [0, 0, 0, 1]
    ])


def get_inv_mat_sphere(sphere):
    sx = float(sphere.scl_x)
    sy = float(sphere.scl_y)
    sz = float(sphere.scl_z)
    tx = float(sphere.pos_x)
    ty = float(sphere.pos_y)
    tz = float(sphere.pos_z)

    return np.array([[1/sx, 0, 0, -tx/sx],
        [0, 1/sy, 0, -ty/sy],
        [0, 0, 1/sz, -tz/sz],
        [0, 0, 0, 1]
    ])


def check_shadow_ray(light, point, sphere, sphere2):
    light_pos = np.array([float(light.pos_x), float(light.pos_y), float(light.pos_z)])

    direction = light_pos - point[:3]
    dist_to_light = np.linalg.norm(direction)
    direction = direction / dist_to_light

    #avoid self intersection
    inv_mat = get_inv_mat_sphere(sphere)
    inv_transpose = np.transpose(inv_mat)

    P_obj = np.matmul(inv_mat, np.array([point[0], point[1], point[2], 1]))

    if point[-1] == 2:
        N_obj = np.array([-P_obj[0], -P_obj[1], -P_obj[2], 0])
    else:
        N_obj = np.array([P_obj[0], P_obj[1], P_obj[2], 0])

    N_world = np.matmul(inv_transpose, N_obj)[:3]

    n = N_world / np.linalg.norm(N_world)

    origin = point[:3] + 0.00001 * direction
   # origin = point[:3] + 0.0001 * direction

    #homogenous
    origin_4d = np.array([origin[0], origin[1], origin[2], 1])
    target_4d = np.array([origin[0] + direction[0], origin[1] + direction[1], origin[2] + direction[2], 1])

    hit = intersect_sphere(origin_4d, target_4d, sphere2, True) 

    if hit and hit[0] < dist_to_light:
        return True  #blocked

    return False



with open(output_name, "w") as f:
    f.write("P3\n")
    f.write(f"{viewscreen.res_x} {viewscreen.res_y}\n")
    f.write("255\n")
    for i in range(int(viewscreen.res_y)): #loop through the height pixels
        for j in range(int(viewscreen.res_x)): #loop through the width pixels
            # pixel to NDCS:
            pixel_data = get_pixel_data(i,j)
            origin = np.array([0,0,0,1])
            direction = pixel_data - origin
            color_data = ray_trace(origin, direction, 0)

            color_data[0] = float(color_data[0])
            color_data[1] = float(color_data[1])
            color_data[2] = float(color_data[2])
            color_data = np.clip(color_data, 0, 1)
            color_data = (color_data * 255).astype(int)

            f.write(f"{int(color_data[0])} {int(color_data[1])} {int(color_data[2])} ")

        f.write("\n")



'''
Recursive algorithm


Function Main
for each pixel (c,r) on screen
    determine ray rc,r from eye through pixel
    ray.setDepth(1)
    color(c,r) = raytrace(rc,r))


Function raytrace(r)
    if (ray.depth() > MAX_DEPTH) return black
    P = closest intersection of ray with all objects
    if( no intersection ) return backgroundColor
    clocal = Sum(shadowRays(P, Lighti))
    cre = raytrace(rre)
    cra = raytrace(rra)
    return (clocal + kre*cre + kra*cra)
'''
