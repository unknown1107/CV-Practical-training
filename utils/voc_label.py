"""
transform the xml file to txt file in the format of VOC
"""
import xml.etree.ElementTree as ET
import os
from os import getcwd
from PIL import Image
DATASET_ROOT = '../dataset'
 
sets = ['train', 'val', 'test']
classes = ['two_wheeler','helmet','without_helmet']
abs_path = os.getcwd()
print(abs_path)
 
def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h
 
def convert_annotation(image_id):
    print('images_id', image_id)
    in_file = open(os.path.join(DATASET_ROOT, 'Annotations/%s.xml' % (image_id)), encoding='UTF-8')
    out_file = open(os.path.join(DATASET_ROOT, 'labels/%s.txt' % (image_id)), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    
    img = Image.open(os.path.join(DATASET_ROOT, 'images/%s.jpg' % (image_id)))
    w, h = img.size

    for obj in root.iter('object'):
        # difficult = obj.find('difficult').text
        # difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes:
        # if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        b1, b2, b3, b4 = b
        # 标注越界修正
        if b2 > w:
            b2 = w
        if b4 > h:
            b4 = h
        b = (b1, b2, b3, b4)
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
 
wd = getcwd()
for image_set in sets:
    if not os.path.exists(os.path.join(DATASET_ROOT, 'labels/')):
        os.makedirs(os.path.join(DATASET_ROOT, 'labels/'))
    image_ids = open(os.path.join(DATASET_ROOT, 'ImageSets/%s.txt' % (image_set))).read().strip().split()
    list_file = open(os.path.join(DATASET_ROOT, '%s.txt' % (image_set)), 'w')
    for image_id in image_ids:
        list_file.write(os.path.join(abs_path, DATASET_ROOT, 'images/%s.jpg\n' % (image_id)))
        convert_annotation(image_id)
    list_file.close()