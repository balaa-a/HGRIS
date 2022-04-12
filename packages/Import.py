import cv2
from loguru import logger
import sys
from numpy import ndarray
import numpy as np
import pyautogui
import queue

import torch,os
from torch.utils.data import Dataset
from torchvision.datasets import ImageFolder
from torchvision import transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from torch import nn
from sklearn.semi_supervised import LabelSpreading
import torchvision
from torch import device, rand
import string
import time,math
from PIL import Image,ImageGrab
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap
import threading