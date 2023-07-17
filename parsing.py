import xml.etree.ElementTree as ET

def parse(annotation_file):
    tree = ET.parse(annotation_file)
    root = tree.getroot()
    annotation_format = detect_format(root)
    bboxes = []
    
    if annotation_format == 'pascal_voc':
        for obj in root.findall('object'):
            bbox = obj.find('bndbox')
            x1 = int(bbox.find('xmin').text)
            y1 = int(bbox.find('ymin').text)
            x2 = int(bbox.find('xmax').text)
            y2 = int(bbox.find('ymax').text)
            bbox_tl = (0, 0)
            bboxes.append((x1, y1, x2, y2, bbox_tl))
    
    return bboxes

def detect_format(root):
    if root.findall('object/bndbox/xmin') and \
        root.findall('object/bndbox/ymin') and \
        root.findall('object/bndbox/xmax') and \
        root.findall('object/bndbox/ymax'):
        return 'pascal_voc'

    else:
        raise ValueError('Unknown format')