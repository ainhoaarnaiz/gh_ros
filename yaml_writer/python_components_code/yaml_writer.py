# inputs > name/typehint/access 
#   > file_path/string/item
#   > write_yaml/boolean/item
#   > origin/plane/item
#   > planes/plane/tree 
# 
# planes list must structured so that each branch 
# contains 1(Lin) or 2(Circ)


import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import ghpythonlib.treehelpers as th
import math

# rhino mm -> ros m
SCALE = 0.001
# euler conversion
UNIT_TOL = float(0.000001)

def pose(frame_origin, frame, frame_id):
    pose = ['%s' % frame_id,
                set_pose_point(frame_origin,frame),
                # set_pose_euler(frame_origin, frame)
                set_pose_quaternion(frame_origin, frame)]
    return pose

def set_pose_point(frame_origin, frame):
    frame.Origin = frame.Origin - frame_origin.Origin 
    point = [str(frame.OriginX * SCALE), str(frame.OriginY * SCALE),
                str(frame.OriginZ * SCALE)]
    return point

def set_pose_euler(frame_origin, frame):
    matrix = rg.Transform.PlaneToPlane(frame_origin, frame)
    a = math.atan2(-matrix.M10, matrix.M00)
    mult = 1.0 - matrix.M20 * matrix.M20

    if abs(mult) < UNIT_TOL:
        mult = 0.0
    b = math.atan2(matrix.M20, math.sqrt(mult))
    c = math.atan2(-matrix.M21, matrix.M22)
    if matrix.M20 < (-1.0 + UNIT_TOL):
        a = math.atan2(matrix.M01, matrix.M11)
        b = -math.pi / 2
        c = 0
    elif matrix.M20 > (1.0 - UNIT_TOL):
        a = math.atan2(matrix.M01, matrix.M11)
        b = math.pi / 2
        c = 0
    return [str(a), str(b), str(c)]

def set_pose_quaternion(frame_origin, frame):
    matrix = rg.Transform.PlaneToPlane(frame_origin, frame).Transpose()
    trace = matrix.M00 + matrix.M11 + matrix.M22

    q = rg.Quaternion()

    if trace > 0.0:
        s = math.sqrt(trace + 1.0)
        q.A = s * 0.5
        s = 0.5 / s
        q.B = (matrix.M12 - matrix.M21) * s
        q.C = (matrix.M20 - matrix.M02) * s
        q.D = (matrix.M01 - matrix.M10) * s
    else:
        if matrix.M00 >= matrix.M11 and matrix.M00 >= matrix.M22:
            s = math.sqrt(1.0 + matrix.M00 - matrix.M11 - matrix.M22)
            inv_s = 0.5 / s
            q.B = 0.5 * s
            q.C = (matrix.M01 + matrix.M10) * inv_s
            q.D = (matrix.M02 + matrix.M20) * inv_s
            q.A = (matrix.M12 - matrix.M21) * inv_s
        elif matrix.M11 > matrix.M22:
            s = math.sqrt(1.0 + matrix.M11 - matrix.M00 - matrix.M22)
            inv_s = 0.5 / s
            q.B = (matrix.M10 + matrix.M01) * inv_s
            q.C = 0.5 * s
            q.D = (matrix.M21 + matrix.M12) * inv_s
            q.A = (matrix.M20 - matrix.M02) * inv_s
        else:
            s = math.sqrt(1.0 + matrix.M22 - matrix.M00 - matrix.M11)
            inv_s = 0.5 / s
            q.B = (matrix.M20 + matrix.M02) * inv_s
            q.C = (matrix.M21 + matrix.M12) * inv_s
            q.D = 0.5 * s
            q.A = (matrix.M01 - matrix.M10) * inv_s

    return [str(q.B), str(q.C), str(q.D), str(q.A)]

def path_to_str(_origin, frames):
    path_str = ''
    for idx, frame in enumerate(frames):
        if len(frame) == 1:
            frame = plane_to_pose_str(_origin,frame[0],str(idx))
            path_str += frame
        elif len(frame) == 2:
            frame = plane_pair_to_pose_str(_origin,frame[0],frame[1],str(idx))
            path_str += frame
        else:
            print 'branches should contain 1 or 2 items'
            return
    return path_str[:-1]

def plane_to_pose_str(frame_origin, frame, idx):
    frame = pose(frame_origin,frame,str(idx))
    frame = ' - pose_id: %s\n   position: [%s, %s , %s]\n   quaternion: [%s, %s, %s, %s]\n' % (frame[0],
    frame[1][0], frame[1][1], frame[1][2],
    frame[2][0], frame[2][1], frame[2][2], frame[2][3])

    return frame

def plane_pair_to_pose_str(frame_origin, frame0, frame1, idx):
    frame0 = pose(frame_origin,frame0,str(idx))
    frame1 = pose(frame_origin,frame1,str(idx))

    frame0 = ' - pose_pair_id: %s\n   position: [%s, %s , %s]\n   quaternion: [%s, %s, %s, %s]\n' % (frame0[0],
    frame0[1][0], frame0[1][1], frame0[1][2],
    frame0[2][0], frame0[2][1], frame0[2][2], frame0[2][3])

    frame1 = '   centre_position: [%s, %s , %s]\n   centre_quaternion: [%s, %s, %s, %s]\n' % (frame1[1][0], 
    frame1[1][1], frame1[1][2],
    frame1[2][0], frame1[2][1], frame1[2][2], frame1[2][3])

    return frame0+frame1

def write_yaml(file_path,string):
    with open(file_path,"w") as file:
            file.write(string)

def main(origin, planes):
    planes.SimplifyPaths()
    planes = th.tree_to_list(planes, retrieve_base=None)
    path = path_to_str(origin, planes)
    header = 'path:\n'
    toolpath = header+path
    yaml = toolpath
    write_yaml(file_path,toolpath)
    print('yaml file generated')

if writeYaml:
    main(origin, planes)