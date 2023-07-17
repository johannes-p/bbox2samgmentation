"""

"""

import cv2
import numpy as np
from scipy import stats

def get_polygons(img, threshold=3.0):
    # Convert the binary array to uint8
    img = img.astype(np.uint8) * 255

    # Find the contours in the binary image
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Initialize the list of polygons
    polygons = []

    # Iterate over each contour
    for contour in contours:
        # Convert the contour to a polygon with 4-sided approximation
        epsilon = 0.01 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Convert the polygon to a list of (x, y) coordinates
        polygon = []
        for point in approx:
            x, y = point[0]
            polygon.append([x, y])

        # Add the polygon to the list of polygons
        polygons.append(polygon)

    # Remove outliers from the vertices of the polygons using the z-score method
    for polygon in polygons:
        x = [point[0] for point in polygon]
        y = [point[1] for point in polygon]
        z_scores = stats.zscore(x + y)
        polygon_filtered = [point for i, point in enumerate(polygon) if abs(z_scores[i]) < threshold]
        polygon[:] = polygon_filtered

    return polygons
