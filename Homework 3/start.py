import numpy
import cv2

def get_affine_transform(source, destination):
    X = np.matrix([[source[0][0],source[0][1],1,0,0,0],
         [0,0,0,source[0][0],source[0][1],1],
         [source[1][0],source[1][1],1,0,0,0],
         [0,0,0,source[1][0],source[1][1],1],
         [source[2][0],source[2][1],1,0,0,0],
         [0,0,0,source[2][0],source[2][1],1]])
    
    a = np.matrix([2,3])
    x_prime = np.matrix([[destination[0][0]],[destination[0][1]],
               [destination[1][0]],[destination[1][1]],
               [destination[2][0]],[destination[2][1]]])
            
    a = np.linalg.lstsq(X, x_prime)[0]
    new_row = np.matrix([0,0,1])
    transform_matrix = np.concatenate((a,new_row), axis=0)
    return np.float32(transform_matrix)


def affine_transformed(source, sourceTriangle, destTriangle, size):
    warp_matrix = get_affine_transform(np.float32(sourceTriangle), np.float(destTriangle))
    #dest = warp_affine(source, warp_matrix, (size[0] size[1]))
    dest = cv2.warpAffine( source, warp_matrix, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    return dest


def triangulation_delaunay(filename):
    points = []
    counter = 0
    with open("points1.txt") as file:
        for row in file:
            x,y = row.split()
            points.append((int(x),int(y)))
            counter = counter + 1
    
    img = cv2.imread(filename);
    size = img.shape
    rect = (0, 0, size[1], size[0]) # or width, height
    subdiv  = cv2.Subdiv2D(rect);
    
    for p in points:
        print(p)
        subdiv.insert(p) # on a for loop for all the points
        
    tri_list = subdiv.getTriangleList()
    return tri_list


def morph_images_triangle(image1, image2, image, triang1, triang2, triang, alpha):
    rect1 = cv2.boundingRect(np.float32([triang1]))
    rect2 = cv2.boundingRect(np.float32([triang2]))
    rect = cv2.boundingRect(np.float32([triang]))

    t1Rect = []
    t2Rect = []
    tRect = []

    for i in xrange(0, 3):
        tRect.append(((triang[i][0] - rect[0]),(triang[i][1] - rect[1])))
        t1Rect.append(((triang1[i][0] - rect1[0]),(triang1[i][1] - rect1[1])))
        t2Rect.append(((triang2[i][0] - rect2[0]),(triang2[i][1] - rect2[1])))

    mask = np.zeros((rect[3], rect[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(tRect), (1.0, 1.0, 1.0), 16, 0);

    img1Rect = image1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    img2Rect = image2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]

    size = (r[2], r[3])
    img_warp1 = affine_transformed(img1Rect, t1Rect, tRect, size)
    img_warp2 = affine_transformed(img2Rect, t2Rect, tRect, size)

    imgRect = (1.0 - alpha) * img_warp1 + alpha * img_warp2

    image[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = image[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] * ( 1 - mask ) + imgRect * mask

def write_points(x,y):
    x
        

#def warp_affine(source, warp_matrix, size):
    
