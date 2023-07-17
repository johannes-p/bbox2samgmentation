import os

def calculate_middle(bbox):
    x1, y1, x2, y2, bbox_tl = bbox
    x_middle = int((x1 + x2) / 2)
    y_middle = int((y1 + y2) / 2)
    x_image = bbox_tl[0] + x_middle
    y_image = bbox_tl[1] + y_middle
    return [x_image, y_image]

def find_annotation_file_by_name(filename, directory):
    extensions = [".txt", ".csv", ".json", ".xml"]
    for file in os.listdir(directory):
        if any(file.endswith(ext) for ext in extensions):
            if os.path.splitext(file)[0] == filename:
                return os.path.join(directory, file)
    return None

def flatten_points(points):
    return [coord for point in points for coord in point]