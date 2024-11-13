import cv2
import numpy as np
import math
import os
import glob
# Load the image
image = cv2.imread("input.jpg")  # Replace with your image file path
height, width, _ = image.shape
# Calculate the center of the image
center_x, center_y = width // 2, height // 2
print(f"Center of the image: ({center_x}, {center_y})")

# Convert image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply threshold to isolate color blocks
_, thresh = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

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
    print(f"block,{i+1},x0, {x},y0,{y},x1,{x+w},y1,{y+h},Pixel Count,{int(pixel_count)},circle:Similarity,{circle_similarity}")
    
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
cv2.imwrite("output.jpg", image)
cv2.waitKey(1000)
cv2.destroyAllWindows()