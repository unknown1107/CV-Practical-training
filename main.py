import cv2
import numpy as np
import gradio as gr
import PIL.Image as Image

from ultralytics import ASSETS, YOLO

model = YOLO("runs/detect/train2/weights/best.pt")
class_dic = [
'two_wheeler',  # 二轮车主体
'helmet',       # 佩戴头盔的头部
'without_helmet'# 未戴头盔的头部
]

class_BGR = [
    (255, 0, 0),    # 二轮车主体      蓝
    (0, 255, 255),  # 佩戴头盔的头部  黄
    (0, 0, 255)     # 未戴头盔的头部  红
]

def predict_image(img, conf_threshold, iou_threshold):
    """Predicts objects in an image using a YOLOv8 model with adjustable confidence and IOU thresholds."""
    results = model.predict(
        source=img,
        conf=conf_threshold,
        iou=iou_threshold,
        show_labels=True,
        show_conf=True,
        imgsz=640,
    )

    for r in results:
        im_array = r.plot()
        im = Image.fromarray(im_array[..., ::-1])

    return im


def predict_count(img, conf_threshold, iou_threshold):
    image_array = np.array(img)
    # 将 RGB 转换为 BGR
    image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

    results = model.predict(
        source=image,
        conf=conf_threshold,
        iou=iou_threshold,
        show_labels=True,
        show_conf=True,
        imgsz=640,
    )

    # 4. 计数检测到的物体
    count = {}
    for result in results:
        for obj in result.boxes:
            cls = int(obj.cls[0])  # 获取类别索引
            count[cls] = count.get(cls, 0) + 1  # 统计数量


    # 在左上角绘制需要的信息
    # 设置初始文本位置
    x = 10
    y_start = 130  # 第一行的y坐标

    text_lines = []
    for i in range(3):
        text_lines.append(f'{class_dic[i]}: {count.get(i, 0)}')

    # 绘制每一行文本
    for i, line in enumerate(text_lines):
        y = y_start + i * 30
        cv2.putText(image, line, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    

    for obj in results[0].boxes:
        x1, y1, x2, y2 = map(int, obj.xyxy[0])  # 获取边界框坐标
        cls = int(obj.cls[0])  # 获取类别索引

        # 绘制矩形框
        cv2.rectangle(image, (x1, y1), (x2, y2), class_BGR[cls], 3)

        text = f'{class_dic[cls]}'
        
        # 获取文本的宽度和高度
        (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)

        # 计算背景矩形的坐标
        background_x1 = x1
        background_y1 = y1 - text_height - baseline - 7  # 文本上方留出一些空间
        background_x2 = x1 + text_width
        background_y2 = y1

        # 绘制红色背景矩形
        cv2.rectangle(image, (background_x1, background_y1), (background_x2, background_y2), class_BGR[cls], cv2.FILLED)

        # 在矩形上绘制文本
        cv2.putText(image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)


    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 将 NumPy 数组转换为 PIL 图像
    return Image.fromarray(rgb_image)
        


iface = gr.Interface(
    fn=predict_count,
    inputs=[
        gr.Image(type="pil", label="Upload Image"),
        gr.Slider(minimum=0, maximum=1, value=0.25, label="Confidence threshold"),
        gr.Slider(minimum=0, maximum=1, value=0.45, label="IoU threshold"),
    ],
    outputs=gr.Image(type="pil", label="Result"),
    title="Ultralytics Gradio",
    description="Upload images for inference. The Ultralytics YOLOv8n model is used by default.",
    examples=[
        [ASSETS / "/home/huangliang/CV-Practical-training/test/images/origin/test1.jpg", 0.25, 0.30],
        [ASSETS / "/home/huangliang/CV-Practical-training/test/images/origin/test4.png", 0.25, 0.30],
    ],
)

if __name__ == "__main__":
    iface.launch()