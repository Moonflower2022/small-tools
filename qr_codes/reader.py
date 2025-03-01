import cv2

image = cv2.imread("image.png")
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
detector = cv2.QRCodeDetector()

result = detector.detectAndDecode(gray_image)
print(result[0])