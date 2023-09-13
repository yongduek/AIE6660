# 2023-09-13
# yndk@sogang.ac.kr
# a rectangle, rotating the world center, self-rotating about its center of mass.
import numpy as np 
import cv2 

def R(deg):
    c = np.cos(np.deg2rad(deg))
    s = np.sin(np.deg2rad(deg))

    return np.array([ [c, -s, 0], [s, c, 0], [0, 0, 1]])
    
def T(a,b):
    m = np.eye(3)
    m[0,2] = a 
    m[1,2] = b
    return m

def main():
    im = np.zeros((1200, 1800,3), dtype="uint8")

    p0 = np.array([800, 600]) # center of the system: (x0, y0)

    w = 200
    h = 40
    X = np.array([ [0, 0], [w, 0], [w, h], [0, h] ], dtype=np.int32)

    theta = 0
    phi = 0
    length = 400
    while True:

        im[:,:] = 0  # black

        theta += 2
        phi   += 10

        H_1 = T(p0[0], p0[1]) @ R(theta) @ T(length, 0) @ R(-theta) 
        H = H_1 @ R(phi) @ T(-w/2, -h/2)

        centerloc = H_1[:2, 2].astype(np.int32) # = H_1 @ [0, 0, 1]  # Yellow color
        cv2.ellipse(im, centerloc, axes=(15,15), angle=0, startAngle=0, endAngle=0, color=(0,255,255), thickness=10,)

        # rigid transformation of the bar
        pts = H[:2,:2] @ X.T 
        pts = pts.T + H[:2, 2]
        
        # origin of the object
        q0 = H[:2,2].astype(np.int32).reshape(2)
        cv2.ellipse(im, q0, axes=(15,15), angle=0, startAngle=0, endAngle=0, color=(0,0,255), thickness=10,)

        # center of the system
        cv2.ellipse(im, p0, axes=(15,15), angle=0, startAngle=0, endAngle=0, color=(0,0,255), thickness=10,)
        # print(pts)
        # the rectangluar shape, rotating and rotating
        pts = pts.astype(np.int32)  # White
        cv2.polylines(im, [pts], isClosed=True, color=(255, 255, 255), thickness=4)

        cv2.imshow("display", im)
        if cv2.waitKey(30) == 27:
            break

if __name__ == "__main__":
    main()