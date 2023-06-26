import cv2
import argparse
import numpy as np
import sys
import json
import time

def set_resolution(camera, width, height):
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

def convert_rgb_to_hsv(rgb):
    b, g, r = rgb
    bgr = np.array([[[b, g, r]]], dtype=np.uint8)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_RGB2HSV)[0][0]
    return hsv

W, H = 560, 800
offsetX = -0.05 * W
offsetY = -0.01 * H
safety_padding = 20

default_colors = [
    "podatne_na_choroby: original=[147,107,76]\n",
    "parch: original=[212,159,65]\n",
    "maczniak: original=[249,246,227]\n"
]

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL", help="type of ArUCo tag to generate")
ap.add_argument("--image", type=str, required=True)
ap.add_argument("--input_file", type=str, default='./inputColors.txt')
ap.add_argument("--adjust", type=int, default=20, help="offset")
ap.add_argument('-c', '--camera', type=int, default=0, help='Index of the camera (default: 0)')
ap.add_argument('-o', '--output', type=str, default='image.png', help='Output file name (default: "Calibration.png")')
ap.add_argument('-W', '--width', type=int, default=640, help='Image width (default: 640)')
ap.add_argument('-H', '--height', type=int, default=480, help='Image height (default: 480)')
args = ap.parse_args()

args = vars(ap.parse_args())

#Initialize camera
camera = cv2.VideoCapture(args['camera'])

#Setting camera resolution
set_resolution(camera, args['width'], args['height'])

#Reading image
ret, frame = camera.read()

# Checking if the image is correct
if ret:
    # Savinf image as a PNG
    cv2.imwrite(args['output'], frame)
    

    camera.release()
    cv2.destroyAllWindows()
else:
    print("Błąd podczas pobierania obrazu z kamery.")

image = cv2.imread(args['image'])

if image is not None:
    cv2.imshow('Calibration', image)
    print("If you see the Calibration image, please press q")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Błąd podczas wczytywania obrazu.")


ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL
}
#Detecting aruco markers and getting perspective transofrm
if ARUCO_DICT.get(args["type"], None) is None:
    print("[INFO] ArUCo tag of '{}' is not supported".format(
        args["type"]))
    sys.exit(0)

arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
arucoParams = cv2.aruco.DetectorParameters_create()
(corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict,
    parameters=arucoParams)

if len(corners) != 4:
    print("Cannot detect right amount of markers!")
    exit()

ids = ids.flatten()

ids, corners = zip(*sorted(zip(ids, corners)))
detected_points = np.zeros((4, 2), dtype=np.float32)

cv_custom_point_order = [1, 0, 2, 3]

for i, (markerCorner, markerID) in enumerate(zip(corners, ids)):
    corners = markerCorner.reshape((4, 2))

    detected_points[i][0] = int(corners[cv_custom_point_order[i]][0])
    detected_points[i][1] = int(corners[cv_custom_point_order[i]][1])

target_points = np.float32([[offsetX, offsetY], [W-offsetX, offsetY], [offsetX, H-offsetY], [W-offsetX, H-offsetY]])

matrix = cv2.getPerspectiveTransform(detected_points, target_points)

img = cv2.warpPerspective(image, matrix, (W, H), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))

cv2.imwrite("output.jpg", img)

detected_avg_colors = []
n_colors = 0


with open(args['input_file'], "w") as file:
    file.writelines(default_colors)

with open(args['input_file'], 'r') as f:
    for line in f.readlines():
        if '[' in line:
            n_colors += 1

jump = int(H / n_colors)
for i in range(n_colors):
    cropped_color = img[i * jump + safety_padding:(i + 1) * jump - safety_padding]
    mean_color = cv2.mean(cropped_color)
    detected_avg_colors.append((mean_color[2], mean_color[1], mean_color[0]))

with open(args['input_file'], 'r') as f:
    lines = f.readlines()
    for i, color in enumerate(detected_avg_colors):
        if len(lines[i].split(' ')) != 2:
            print("Wrong input file")
            exit()
        lines[i] = lines[i].strip() + " detected=[" + (str(round(color[0])) + "," + str(round(color[1])) + "," + str(round(color[2])) + "]\n")

with open(args['input_file'], "w") as f:
    for line in lines:
        f.write(line)

with open("colors.txt", "r") as file:
    lines = file.readlines()

converted_colors = []
original_rgb_values = []

for line in lines:
    line = line.strip()
    color_name, colors = line.split(":")
    original_rgb = colors.split("original=")[1].split("]")[0]
    detected_rgb = colors.split("detected=")[1].split("]")[0]

    original_rgb = [int(x) for x in original_rgb.replace("[", "").replace("]", "").split(",")]
    detected_rgb = [int(x) for x in detected_rgb.replace("[", "").replace("]", "").split(",")]

    # Convert RGB to HSV
    original_hsv = convert_rgb_to_hsv(original_rgb)
    detected_hsv = convert_rgb_to_hsv(detected_rgb)

    original_hsv_str = f"[{','.join(map(str, original_hsv))}]"
    detected_hsv_str = f"[{','.join(map(str, detected_hsv))}]"

    converted_colors.append(f"{color_name}: original={original_hsv_str} detected={detected_hsv_str}")
    original_rgb_values.append(original_rgb)

    with open("colorshsv.txt", "w") as file:
        for color in converted_colors:
            file.write(color + "\n")

# Read the file "colorshsv.txt"
with open("colorshsv.txt", "r") as file:
    lines = file.readlines()

# Initialize detected vectors
detected_vectors = []

# Process lines in the file
for line in lines:
    line = line.strip()
    _, detected_values = line.split("detected=")
    detected_values = detected_values.replace("[", "").replace("]", "").split(",")
    detected_values = [int(value) for value in detected_values]

    # Add values to the detected vectors
    detected_vector = np.array(detected_values)
    detected_vectors.append(detected_vector)

# Convert BGR to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Initialize color boundaries dictionary
color_boundaries = {}

# Define range of colors in HSV
for i, color_name in enumerate(["brown", "gold", "white"]):
    #I use if to better adjust white color
    if color_name == "white":
        lower_color = detected_vectors[i] - args['adjust'] - 3
        upper_color = detected_vectors[i] + args['adjust'] + 3
    elif color_name == "gold":
        lower_color = detected_vectors[i] - args['adjust'] + 1
        upper_color = detected_vectors[i] + args['adjust'] - 1
    else:
        lower_color = detected_vectors[i] - args['adjust'] 
        upper_color = detected_vectors[i] + args['adjust']

    # Threshold the HSV image to get only the color
    mask_color = cv2.inRange(hsv, lower_color, upper_color)
    result_color = cv2.bitwise_and(image, image, mask=mask_color)

    color_boundaries[color_name] = {
        "real_rgb": original_rgb_values[i],
        "range": {
            "min": lower_color.tolist(),
            "max": upper_color.tolist()
        }
    }

    # Display the result in a separate window
    cv2.imshow(color_name, result_color)

    # Adjust the position of the window
    window_x = i * result_color.shape[1]  # Set the x coordinate based on the window index
    window_y = 1  # Set the y coordinate as desired
    cv2.moveWindow(color_name, window_x, window_y)

# Wait for a key event and then close all windows
cv2.waitKey(0)
cv2.destroyAllWindows()


# Save the color boundaries to a JSON file with each value on a separate line
with open("color_boundaries.json", "w") as json_file:
    json.dump(color_boundaries, json_file, indent=4, separators=(", ", ": "))

print("Calibration finished! Go to the liveCapture.py to see the results.")

cv2.waitKey(0)
cv2.destroyAllWindows()
