# Project Name

Tree of Life - Color Detection System

## Motivation

The motivation behind this project was to develop a solution for the identification of ground objects in the context of the "Tree of Life" competition at Droniada 2023. The goal was to create a system capable of detecting diseased plants and applying antibiotics using a custom-built paintball mechanism mounted on a drone. This code specifically focuses on color detection and image display from the drone after automatically applying generated masks. The project was developed by members of the student scientific association, High Flyers.

## Problem Statement

This project addresses the challenges posed by changing atmospheric conditions, which affect color recognition. Before drone deployment, the camera mounted on the unmanned aerial vehicle (UAV) is calibrated using a generated color board (board.png). This calibration enables the system to be independent of varying lighting conditions.

## Key Features

- Calibration: The system calibrates the camera by using a color board to ensure consistent color recognition under changing lighting conditions.
- Color detection: The code includes a comprehensive color calibration workflow and ArUCo tag generation procedure.
- Image display: After color detection, the code displays the captured image from the drone with automatically generated masks.

## Project Highlights

The High Flyers team achieved first place in the "Tree of Life" competition.

## Installation

1. Clone the repository or download the source code files.
2. Install the required Python libraries by running the following command:

```bash
pip install -r requirements.txt
```

## Generating Color Board

Before detecting colors, it is necessary to generate a color board. Follow the steps below:

1. Run the `generateBoard.py` file, providing the following arguments:
   - `--type`: Select a specific ArUCo dictionary from the given options.
   - `--input_file`: Declare the target colors in a file.

Example:

```bash
python3 generateBoard.py --type DICT_5X5_100 --input_file colors.txt
```

The `colors.txt` file should contain color definitions in the following format:

```
podatne_na_choroby: original=[147,107,76]
parch: original=[212,159,65]
maczniak: original=[249,246,227]
```

You can include as many colors as desired, separated by spaces and commas.

The `--type` argument accepts the following options:

- DICT_4X4_100
- DICT_4X4_250
- DICT_4X4_1000
- DICT_5X5_50
- DICT_5X5_100
- DICT_5X5_250
- DICT_5X5_1000
- DICT_6X6_50
- DICT_6X6_100
- DICT_6X6_250
- DICT_6X6_1000
- DICT_7X7_50
- DICT_7X7_100
- DICT_7X7_250
- DICT_7X7_1000
- DICT_ARUCO_ORIGINAL

The default value for `--type` is DICT_ARUCO_ORIGINAL. The generated color board will have the same width-to-height ratio as an A4 sheet for easy printing.

## Color Detection

The `colorDetection.py` file provides the following color calibration workflow:

1. Sets the camera resolution for consistent image capture.
2. Captures an image from the camera and saves it as a PNG file.
3. Loads the specified image for further processing.
4. Detects ArUCo markers in the image for identification.
5. Sorts the detected markers based on their IDs for analysis.
6. Extracts the corner points of the markers for accurate transformation.
7. Computes the transformation matrix for perspective correction.
8. Applies the transformation matrix to correct the image's perspective.
9. Segments the corrected image into distinct color regions for analysis.
10. Calculates the average color for each segment to capture their essence.
11. Retrieves the default color values from the input file for comparison.
12. Updates the detected color values in the input file based on the analysis.
13. Converts the detected colors from the RGB color space to the HSV color space.
14. Saves the converted colors to a new file for accessibility.
15. Converts the input image from the BGR color space to the HSV color space.
16. Establishes color ranges for the desired colors.
17. Applies color thresholding to extract regions representing the desired colors.
18. Displays the extracted color regions in separate windows for visual inspection.
19. Persists the color boundaries to a JSON file for future reference.
20. Notifies the user about the successful completion of the calibration process.

## Live Video Capture

The `liveVideoCapture.py` file utilizes OpenCV to detect colors in real-time video frames captured from a camera. The program reads color boundaries from a JSON file, applies color detection based on those boundaries, and displays the original frame and color detection results in a 2x2 grid configuration.

### Usage

Check the `color_boundaries.json` file, which stores color boundaries formatted and prepared by `colorDetection.py`. The file should follow this structure:

```json
{
  "color_name": {
    "real_rgb": [r, g, b],
    "range": {
      "min": [h_min, s_min, v_min],
      "max": [h_max, s_max, v_max]
    }
  }
}
```

Follow these steps to run the program:

1. Place the printed color board in front of the UAV and calibrate the camera.
2. Run the following command:

```bash
python3 colorDetection.py --type DICT_5X5_100 --image droneImage.png --input_file colors.txt -c 0 -o droneImage.png --adjust 20
```

You need to adjust color detection to the hardware you use. Change the `adjust` parameter when needed.

This command will calibrate the camera and save the image with automatically generated masks.

3. Open the `liveVideoCapture.py` file and execute the program to display the live video feed from the drone.

## Colaboration 
Krzysztof Połeć (krzysztofpolec) , Grzegorz Paleta (Grzetan)
