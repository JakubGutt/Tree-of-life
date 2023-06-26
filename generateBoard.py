import numpy as np
import argparse
import cv2
import sys
import os
import shutil
import ast

padding = 50
W,H = 2480, 3508
TAG_SIZE = 300

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", type=str,
	default="DICT_ARUCO_ORIGINAL",
	help="type of ArUCo tag to generate")

ap.add_argument(
  "--input_file",
  type=str,
  required=False,
  default='./colors.txt'
)

args = vars(ap.parse_args())

colors = {}

with open(args['input_file'], 'r') as f:
	for line in f.readlines():
		splitted = line.split(' ')
		if len(splitted) > 2:
			print("Wrong input file")
			exit()
		colors[splitted[0][:-1]] = ast.literal_eval(splitted[1].split('=')[1])

# define names of each possible ArUco tag OpenCV supports
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

if os.path.exists('aruco_tags'):
	shutil.rmtree('aruco_tags')
	os.makedirs('aruco_tags')
else:
	os.makedirs('aruco_tags')

if ARUCO_DICT.get(args["type"], None) is None:
	print("[INFO] ArUCo tag of '{}' is not supported".format(
		args["type"]))
	sys.exit(0)

arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])

board = np.full((H, W, 3), 255, dtype="uint8")

# Draw colors from top to bottom
vertical_offset = (int)(H/len(colors))
for i, color in enumerate(colors):
	cv2.rectangle(board, (0,i*vertical_offset), (W,H), (colors[color][2], colors[color][1], colors[color][0]), -1)

corners = ['topleft', 'topright', 'bottomleft', 'bottomright']
corner_offsets = [(padding,padding), (padding, W-TAG_SIZE-padding), (H-TAG_SIZE-padding, padding), (H-TAG_SIZE-padding, W-TAG_SIZE-padding)]

for i in range(4):
	# Save tags to output folder in case we need to use them independly
    tag = np.zeros((TAG_SIZE, TAG_SIZE, 1), dtype="uint8")
    cv2.aruco.drawMarker(arucoDict, i+1, TAG_SIZE, tag, 1)
    cv2.imwrite("aruco_tags/" + corners[i] + ".png", tag)

	# Draw white rectangles to make tags more visible
    x1 = corner_offsets[i][1]-padding
    y1 = corner_offsets[i][0]-padding
    cv2.rectangle(board, (x1,y1), (x1+TAG_SIZE+2*padding,y1+TAG_SIZE+2*padding), (255,255,255), -1)

	# Draw tags on board
    color_tag = cv2.cvtColor(tag, cv2.COLOR_GRAY2RGB)
    board[corner_offsets[i][0]:corner_offsets[i][0] + TAG_SIZE, corner_offsets[i][1]:corner_offsets[i][1] + TAG_SIZE] = color_tag
	
cv2.imwrite("board.png", board)
