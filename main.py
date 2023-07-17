import os

import click
import cv2
from segment_anything import SamPredictor, sam_model_registry
import numpy as np
from PIL import Image
from shapely.geometry import Polygon
from tqdm import tqdm

from contour_to_polygons import get_polygons
from create_annotation import create_polygon_annotation
from helper_functions import calculate_middle, find_annotation_file_by_name
from parsing import parse

@click.command()
@click.option("-c", "--class_name", "class_name", required=True, help="The name of the annotated object")
@click.option("-i", "--images", "image_directory", default="images", help="Path to image folder")
@click.option("-a", "--annotations", "annotation_directory", default="annotations", help="Path to annotation folder")
@click.option("-m", "--model", "sam_checkpoint", \
     default="models/sam_vit_b_01ec64.pth", help="Path to SAM model")
@click.option("-o", "--out", "output_file", default="annotations.json", help="Path to output file")
@click.option("-b", "--use_bbox", \
     help="Use boundingbox coordinates instead of boundingbox center", is_flag=True)
@click.option("-t", "--threshold", default=3.0, help="Threshold value to identify outlier vertices (default: 3.0)")

def main(class_name, image_directory, annotation_directory, sam_checkpoint, output_file, use_bbox, threshold):
    model_type = os.path.basename(sam_checkpoint)[4:9]
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    predictor = SamPredictor(sam)

    for filename in tqdm(os.listdir(image_directory)):

        image_file = os.path.join(image_directory, filename)
        annotation_file = find_annotation_file_by_name(os.path.splitext(filename)[0], annotation_directory)
        if annotation_file is None:
            continue

        bboxes = parse(annotation_file)

        image = cv2.imread(image_file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        predictor.set_image(image)

        for i, bbox in enumerate(bboxes):
            input_point = np.array([calculate_middle(bbox)])
            input_label = np.array([1])
            input_box = np.array(bbox[0:4])

            masks, scores, _ = predictor.predict(
                point_coords= None if use_bbox else input_point,
                point_labels=input_label,
                box=input_box if use_bbox else None,
                multimask_output=True,
                )

            # Get mask with highest score
            max_index = scores.argmax()
            Image.fromarray(masks[max_index]).save(f'masks/{filename}-mask-{i}.png')

            polygons = get_polygons(masks[max_index], threshold)

            area = 0
            for i, polygon in enumerate(polygons):
                if(area == 0 or area < Polygon(polygon).area):
                    area = Polygon(polygon).area
                    index_biggest_area = i

            create_polygon_annotation(filename, class_name, polygons[index_biggest_area], image_directory, output_file)

if __name__ == '__main__':
    main()
