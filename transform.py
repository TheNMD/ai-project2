import numpy as np
import cv2

def order_points(pts):
    # Initializing the list of coordinates to be ordered
    rect = np.zeros((4, 2), dtype = "float32")

    s = pts.sum(axis = 1)
    # Top-left point will have the smallest sum
    rect[0] = pts[np.argmin(s)]
    # Bottom-right point will have the largest sum
    rect[2] = pts[np.argmax(s)]


    diff = np.diff(pts, axis = 1)    
    # Top-right point will have the smallest difference
    rect[1] = pts[np.argmin(diff)]
    # Bottom-left point will have the largest difference
    rect[3] = pts[np.argmax(diff)]

    return rect

def perspective_transform(image, pts):
    rect = order_points(pts)
    # 4 corners of old image
    (tl, tr, br, bl) = rect

    # New width = max(|br - bl|, |tr - tl|)
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # New height = max(|tr - br|, |tl - bl|)
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # 4 corners of warped image
    dst = np.array([[0, 0],
                    [maxWidth - 1, 0],
                    [maxWidth - 1, maxHeight - 1],
                    [0, maxHeight - 1]], dtype = "float32")

    # Compute and apply the perspective transform matrix
    transform_mat = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, transform_mat, (maxWidth, maxHeight))

    return warped