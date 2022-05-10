### Introduction

本系统主要功能是通过识别手势与系统进行交互，还有一些额外的功能如录像回放、日志打印等，目的是帮助用户回溯历史操作。

手势识别通过卷积神经网络实现，这里使用了ResNet50的结构，为了适应项目进行了些微修改。用到了自己构建的数据集，0-9十个类别，共5000张左右650×650的图像。

### Installation

```bash
git clone https://gitee.com/balaa/hgrs.git
cd HGRS
pip install -r requirements.txt
# 下载weightfile文件，放置在resources/checkpoints下
```

### Pre-trained

请下载[weightfile](https://drive.google.com/drive/folders/1hxzhYrLdi3kir7EUl7uBpMaTfOKcI9RT?usp=sharing)，并best-10.pt文件放置在“resources/checkpoints/”目录下。

### Train

请下载数据[data](https://drive.google.com/drive/folders/1bwPzxeHKcwcehEmTaXwqDyRfiZ417pvr?usp=sharing)用于训练。训练脚本在packages/model目录下。

### Startup

```bash
bash AppSystem.sh
```


