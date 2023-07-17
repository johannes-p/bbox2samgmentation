import json
import os
from typing import List

from PIL import Image

from helper_functions import flatten_points

def create_polygon_annotation(image_filename: str, category: str, vertices: List[List[int]], image_directory: str, annotation_file: str = "annotations.json") -> None:
    """
    Create a polygon annotation for a provided image file name and category using COCO annotation format.
    
    Args:
    - image_filename (str): The filename of the image to be annotated.
    - category (str): The category of the object in the image.
    - vertices (List[List[int]]): A list of vertices that define the polygon in the image. Each vertex is a list of [x, y] coordinates.
    - annotation_file (str): The filename of the annotation file in COCO format. If the file does not exist, a new file will be created.
    """
    if not os.path.exists(annotation_file):
        # Create a new annotation file if it does not exist
        with open(annotation_file, "w", encoding="utf-8") as f:
            json.dump({"images": [], "annotations": [], "categories": []}, f)

    # Load the annotation file
    with open(annotation_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Add the image to the annotation file if it does not exist
    image_id = None
    for image in data["images"]:
        if image["file_name"] == image_filename:
            image_id = image["id"]
            break

    if image_id is None:
        image = Image.open(os.path.join(image_directory, image_filename))
        width, height = image.size

        image_id = len(data["images"]) + 1
        
        data["images"].append({
            "id": image_id,
            "file_name": image_filename,
            "width": width,
            "height": height
        })

    # Add the category to the annotation file if it does not exist
    category_id = None
    for cat in data["categories"]:
        if cat["name"] == category:
            category_id = cat["id"]
            break

    if category_id is None:
        category_id = len(data["categories"])
        data["categories"].append({
            "id": category_id,
            "name": category
        })

    # Convert the vertices to the required format
    segmentation = [[int(x) for x in vertex] for vertex in vertices]
    segmentation = flatten_points(segmentation)

    # Add the polygon annotation to the annotation file
    annotation_id = len(data["annotations"]) + 1
    data["annotations"].append({
        "id": annotation_id,
        "image_id": image_id,
        "category_id": category_id,
        "segmentation": [segmentation],
        "iscrowd": 0,
        "area": 0,
        "bbox": [0, 0, 0, 0]
    })

    # Save the updated annotation file
    with open(annotation_file, "w", encoding="utf-8") as f:
        json.dump(data, f)
