import cv2
import numpy as np
import math
import sys
import os
# Load the image
show_result_image = 1
result_image_path = ''
n = len(sys.argv)
for p0 in range(1, n):   # skip first exe name
    s = sys.argv[p0]
    print(s)
    colon_index = s.index(':')
    s0 = s[:colon_index]
    if s0 == "s" or s0 == 'S':  # show,save image or not
        i0 = int(s[colon_index + 1:])
        print("s parameter found")
        print("t=", i0, "ms")
        show_result_image = i0
    if s0 == "P" or s0 == 'p':   # path
        result_image_path = s[colon_index + 1:]
        print("P parameter found")
        print("Result_image_path: ", result_image_path)
        if not os.path.exists(result_image_path):
            # Create the directory if it does not exist
            os.makedirs(result_image_path)
            print(f"Created directory: {result_image_path}")
        else:
            print(f"Directory already exists: {result_image_path}")


# show_result_image = 1  #  0  no show, none >0 :show n mS
# 設定目錄路徑

dut_path = './DUT/'  # dut 圖片位置
dir_path_0 = os.path.dirname(os.path.dirname(dut_path))

if not os.path.exists(dut_path):
    # Create the directory if it does not exist
    os.makedirs(dut_path)
    print(f"Created directory: {dut_path}")
else:
    print(f"Directory already exists: {dut_path}")


image = cv2.imread("input.jpg")  # Replace with your image file path
height, width, _ = image.shape

# Calculate the center of the image
center_x, center_y = width // 2, height // 2
print(f"Center of the image: ({center_x}, {center_y})")

# Convert image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply threshold to isolate color blocks
_, thresh = cv2.threshold(gray_image, 80, 255, cv2.THRESH_BINARY)

# Find contours of the color blocks
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Define the font for labeling
font = cv2.FONT_HERSHEY_SIMPLEX
#font = cv2.FONT_HERSHEY_TRIPLEX
font_scale = 0.5
#font_color = (255, 0, 0)  # Blue color for labels
font_color = (0,255,0)  # Green color for labels
line_type = 1

for i, contour in enumerate(contours):
    x, y, w, h = cv2.boundingRect(contour)
    top_left = (x, y)
    bottom_right = (x + w, y + h)
    
    #Diagonal= (w^2+h^2)^0.5
    Diagonal=math.sqrt(w**2 + h**2)
    #idea circle area
    area=math.pi*(Diagonal/2/1.414)**2
     
    # Count the number of pixels in the color block
    pixel_count = cv2.contourArea(contour)  # Number of pixels in the color block
    circle_similarity=1- abs(pixel_count-area)/area 
   
    # Print color block information
    print(f"Color block {i+1}, UL, {top_left},LR, {bottom_right}, Pixel Count, {int(pixel_count)},circle:Similarity,{circle_similarity}")
    
    # Draw rectangle around each color block
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
    
    # Label each color block with an ID and pixel count
    label0 = f"ID: {i+1}, Pixels: {int(pixel_count)}"
    label1 = f"UL{top_left}, LR: {bottom_right}"
    label2 = f"CircleSimilarity: {circle_similarity}"
    
    # Position the label on the side or above each block
    
    # Put the text label on the image
    text_position = (x + w + 5, y + 20)  # Offset to the right of the block
    cv2.putText(image, label0, text_position, font, font_scale, font_color, line_type)
    text_position = (x + w + 5, y + 40)  # Offset to the right of the block
    cv2.putText(image, label1, text_position, font, font_scale, font_color, line_type)
    text_position = (x + w + 5, y + 60)  # Offset to the right of the block
    cv2.putText(image, label2, text_position, font, font_scale, font_color, line_type)


# Display the result
cv2.imshow("Color Blocks with Center", image)
image_file_name = result_image_path + "output.jpg"
cv2.imwrite(image_file_name, image)
cv2.waitKey(show_result_image)
cv2.destroyAllWindows()