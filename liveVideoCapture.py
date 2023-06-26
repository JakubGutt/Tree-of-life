import cv2
import numpy as np
import json

# Load data from the "color_boundaries.json" file
with open('color_boundaries.json', 'r') as file:
    json_data = file.read()

data = json.loads(json_data)

# Initialize the camera
cap = cv2.VideoCapture(0)

# Set the window size
window_width = 1200
window_height = 900

# Create a window to display the results
cv2.namedWindow("Color Detection", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Color Detection", window_width, window_height)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to the HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Initialize a list to store the result images (colors + original frame)
    results = []

    # Add the original frame to the results list
    results.append(frame)

    # Iterate over the colors
    for color_name, color_data in data.items():
        # Get the HSV boundaries for the color
        hsv_min = np.array(color_data["range"]["min"], dtype=np.int32)
        hsv_max = np.array(color_data["range"]["max"], dtype=np.int32)

        # Create a mask for the color
        mask_color = cv2.inRange(hsv_frame, hsv_min, hsv_max)

        # Perform bitwise AND operation between the frame and the mask
        result_color = cv2.bitwise_and(frame, frame, mask=mask_color)

        # Add the result image to the list
        results.append(result_color)

    # Create a 2x2 grid configuration
    grid = np.zeros((2 * frame.shape[0], 2 * frame.shape[1], 3), dtype=np.uint8)

    # Fill the grid with the result images
    grid[0:frame.shape[0], 0:frame.shape[1]] = results[0]  # Original frame
    grid[0:frame.shape[0], frame.shape[1]:] = results[1]  # First color
    grid[frame.shape[0]:, 0:frame.shape[1]] = results[2]  # Second color
    grid[frame.shape[0]:, frame.shape[1]:] = results[3]  # Third color

    # Display the result in the window
    cv2.imshow("Color Detection", grid)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the windows
cap.release()
cv2.destroyAllWindows()