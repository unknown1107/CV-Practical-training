# 视觉实训小组 小组作业
组长：黄亮

组员：李肖洋，孙贺，冉鑫平，高庆，阳涵宇

***

小组分工

1. **模型训练**
   - **负责人**: 黄亮（组长）
   - **任务描述**: 负责模型的训练工作，并监督和协调整个项目开发过程。确保团队在预定时间内完成任务，及时解决训练中遇到的问题。
   - **具体任务**:
     - **加载预训练模型**: 加载 YOLOv8 的预训练模型，并配置训练脚本。
     - **训练参数设置**: 设置关键训练参数，包括 `BATCH_SIZE`、`epochs`、学习率等。
     - **训练过程监控**: 监控训练进度，记录每个 Epoch 的性能指标（如损失值、mAP、精度、召回率）。
     - **显存占用记录**: 监控并记录显存占用情况，确保训练过程中硬件资源的合理利用。
     - **训练日志维护**: 记录详细的训练日志，包含参数设置、性能指标、异常处理等，确保实验可重复性。

2. **项目配置**
   - **负责人**: 孙贺
   - **任务描述**: 负责项目的环境搭建和依赖配置，确保开发环境的稳定性和可移植性。确保所有成员的开发环境一致，减少环境配置对项目开发的影响。
   - **具体任务**:
     - **安装 `conda`**: 在 `Linux` 和 `Windows` 系统上安装 `conda`。
     - **创建开发环境**: 创建 `conda` 环境并安装 `pytorch`、`ultralytics YOLOv8` 以及其他所需的 Python 库。
     - **依赖配置**: 编写一键安装依赖的脚本，确保环境配置的高效性。
     - **文档撰写**: 编写环境配置文档，详细记录每一步操作，确保其他成员能顺利搭建环境。
     - **问题排查**: 解决成员在环境配置过程中遇到的问题，确保环境正常运行。

3. **数据集制作**
   - **负责人**: 李肖洋、冉鑫平
   - **任务描述**: 负责数据集的收集、处理和标注工作，确保数据集的完整性和准确性。分工合作，高效完成数据集的制作。
   - **具体任务**:
     - **数据集收集**: 收集电动车佩戴头盔检测数据集（TWHD），并扩展数据集以提高模型泛化能力。
     - **数据标注**: 使用 `labelimg` 工具对数据集进行详细标注，确保标注的一致性和准确性。
     - **数据集划分**: 按照标准流程将数据集划分为训练集、验证集、测试集，使用 `utils/split_train_val.py` 进行划分。
     - **标注文件转换**: 将 XML 格式的标注文件转换为 YOLO 所需的 TXT 格式，运行 `utils/voc_label.py` 完成转换。
     - **数据增强**: 进行数据增强操作（如翻转、旋转、亮度调整等），以提升模型的鲁棒性。
     - **数据集验证**: 验证数据集的完整性和一致性，确保数据集准备无误。

4. **结果与检验**
   - **负责人**: 高庆
   - **任务描述**: 负责模型的验证与预测工作，确保模型在测试集上的表现达标。深入分析模型的输出结果，提出调整建议以优化模型表现。
   - **具体任务**:
     - **模型验证**: 使用验证集对模型进行验证，记录验证损失、mAP等指标，与原始标签进行对比分析。
     - **结果分析**: 根据验证结果，分析模型的强项和弱项，识别需要调整的部分。
     - **模型调整**: 根据分析结果，对训练参数或模型架构进行调整，重新训练模型以提高性能。
     - **预测任务**: 处理测试图片和视频，生成训练后的预测结果。
     - **结果记录**: 记录预测结果，生成详细的对比报告，评估模型的实际应用效果。

5. **展示与报告**
   - **负责人**: 阳涵宇
   - **任务描述**: 负责项目最终成果的展示，包括结果可视化和报告编写。确保结果展示的清晰性和专业性，以便清楚地传达项目成果。
   - **具体任务**:
     - **结果视频制作**: 制作训练前后的视频对比，展示模型的实际应用效果。
     - **图片展示**: 生成预测结果的图片展示，包括对比原图与预测图。
     - **报告编写**: 编写详细的项目报告，内容涵盖项目背景、方法、结果分析、结论及未来工作展望。
     - **ppt制作**: 制作项目演示用的幻灯片，方便在汇报或展示时使用。
     - **反馈收集**: 收集其他成员对结果展示和报告内容的反馈，进行最终的修改和完善。



## 1. 安装环境

安装`conda`

> [linux](https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-x86_64.sh)
>
> [windows](https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-x86_64.sh)

创建`conda`环境

> ```shell
> conda create -n yolov8 python=3.8
> conda activate yolov8
> ```

一键安装依赖

> ```shell
> conda install -c pytorch -c nvidia -c conda-forge pytorch torchvision pytorch-cuda=11.8 ultralytics
> ```

## 2. 制作数据集

使用开源数据集[电动车佩戴头盔检测数据集（TWHD）](https://pan.baidu.com/share/init?surl=o9I4N4lORFGPD7ETm7C9_w&pwd=9xsz)

**TODO** 自己制作并且标记数据集

***

`dataset`数据集目录

> * `Annotations`文件夹：用来存放使用`labelimg`给每张图片标注后的xml文件。
> * `Images`文件夹：用来存放原始的需要训练的数据集图片，图片格式为jpg格式。
> * `ImageSets`文件夹：用来存放将数据集划分后的用于**训练**、**验证**、**测试**的文件。
> * `Labels`文件夹：用来存放将xml格式的标注文件转换后的txt格式的标注文件。

运行 `utils/split_train_val.py` 和 `utils/voc_label.py` 进行数据集划分

划分之后的结果

![Clip_2024-09-03_01-55-06](https://my-img-typora.oss-cn-chengdu.aliyuncs.com/img/Clip_2024-09-03_01-55-06.png)

## 3. 训练

> 训练环境 `Ultralytics YOLOv8.2.86 🚀 Python-3.8.19 torch-2.4.0 CUDA:0 (NVIDIA A10, 22513MiB)`
> 
> 在 `BATCH_SIZE=32` 的情况下 `100 epochs completed in 4.229 hours.` 

`train.ipynb`

```python
from ultralytics import YOLO

# Load a model
model = YOLO("model/yolov8n.pt")  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data="wheat.yaml", epochs=100， batch=32)
```

### 参数和加载

![image-20240903020007165](https://my-img-typora.oss-cn-chengdu.aliyuncs.com/img/image-20240903020007165.png)

### 显存占用情况

![image-20240903020151661](https://my-img-typora.oss-cn-chengdu.aliyuncs.com/img/image-20240903020151661.png)

### 训练过程

![image-20240903020031128](https://my-img-typora.oss-cn-chengdu.aliyuncs.com/img/image-20240903020031128.png)

![image-20240903020053988](https://my-img-typora.oss-cn-chengdu.aliyuncs.com/img/image-20240903020053988.png)

![image-20240903020605914](https://my-img-typora.oss-cn-chengdu.aliyuncs.com/img/image-20240903020605914.png)

### VALIDATE

![image-20240903020123464](https://my-img-typora.oss-cn-chengdu.aliyuncs.com/img/image-20240903020123464.png)

进行验证的原标签和预测对比

![image-20240903020403830](https://my-img-typora.oss-cn-chengdu.aliyuncs.com/img/image-20240903020403830.png)

![image-20240903020423372](https://my-img-typora.oss-cn-chengdu.aliyuncs.com/img/image-20240903020423372.png)

![image-20240903020439723](https://my-img-typora.oss-cn-chengdu.aliyuncs.com/img/image-20240903020439723.png)

## 4.训练结果

![results](https://my-img-typora.oss-cn-chengdu.aliyuncs.com/img/results.png)

## 5. 预测结果

### 图片

<center class="half">
    <img src="test/images/origin/test1.jpg" width="350"/>
    <img src="test/images/pred/test1.jpg" width="350"/>
</center>

<center class="half">
    <img src="test/images/origin/test2.png" width="350"/>
    <img src="test/images/pred/test2.png" width="350"/>
</center>

<center class="half">
    <img src="test/images/origin/test3.png" width="350"/>
    <img src="test/images/pred/test3.png" width="350"/>
</center>

<center class="half">
    <img src="test/images/origin/test4.png" width="350"/>
    <img src="test/images/pred/test4.png" width="350"/>
</center>

### 视频

原视频：`test/videos/origin/1.mp4`

训练之后的视频：`test/videos/pred/1_full.mp4`， `test/videos/pred/1_only_helmet.mp4`