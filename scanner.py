import cv2
import imutils
from skimage.filters import threshold_local
from transform import perspective_transform

imageName = "sample4"
# Passing the image path

original_img = cv2.imread(f'./{imageName}.jpg')
copy = original_img.copy()

# The resized height in hundreds
ratio = original_img.shape[0] / 500.0
img_resize = imutils.resize(original_img, height=500)
cv2.imwrite(f'./{imageName}_resized.jpg', img_resize)

gray_image = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
cv2.imwrite(f'./{imageName}_gray.jpg', gray_image)

blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
edged_img = cv2.Canny(blurred_image, 75, 200)
cv2.imwrite(f'./{imageName}_edge.jpg', edged_img)

cnts, _ = cv2.findContours(edged_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    if len(approx) == 4:
        doc = approx
        break
    
p = []

for d in doc:
    tuple_point = tuple(d[0])
    cv2.circle(img_resize, tuple_point, 3, (0, 0, 255), 4)
    p.append(tuple_point)

cv2.imwrite(f'./{imageName}_corner.jpg', img_resize)

warped_image = perspective_transform(copy, doc.reshape(4, 2) * ratio)
warped_image = cv2.cvtColor(warped_image, cv2.COLOR_BGR2GRAY)

T = threshold_local(warped_image, 11, offset=10, method="gaussian")
warped = (warped_image > T).astype("uint8") * 255
cv2.imwrite(f'./{imageName}_warped.jpg', warped)