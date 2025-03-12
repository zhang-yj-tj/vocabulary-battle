from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import win32gui
import pyautogui
from PIL import Image
import re
import time
from pywinauto.application import Application
import logging
from paddleocr import PaddleOCR, draw_ocr
import json
import requests
import re
from baicizhanciku.find import get_mean_cn, remove_duplicates
import mouse
from search import search

# 创建一个日志记录器
mylogger = logging.getLogger("my_logger")
mylogger.setLevel(logging.DEBUG)  # 设置全局日志级别为 DEBUG
# 创建文件处理器，将日志输出到文件
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)  # 文件处理器的日志级别为 DEBUG
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
# 将处理器添加到日志记录器
mylogger.addHandler(file_handler)
# 禁用日志记录器的传播
mylogger.propagate = False

# 针对 paddleocr 的日志记录器单独配置
paddle_logger = logging.getLogger('ppocr')
paddle_logger.setLevel(logging.ERROR)  # 忽略 INFO 和 WARNING 级别的日志
# 禁用失败安全机制
#pyautogui.FAILSAFE = False

remove_duplicates()
#预载模型需要较长时间
model = SentenceTransformer(r".\\distiluse-base-multilingual-cased-v2")
ocr = PaddleOCR(use_angle_cls=False, lang="ch",cls_model_dir="ocr//cls_model")
T = True
while T:
    try:
        window_title = "雷电模拟器"  # 替换为你的雷电模拟器窗口标题
        # 连接到雷电模拟器窗口
        app = Application(backend="uia").connect(title=window_title)
        window = app.window(title=window_title)

        # 获取窗口的屏幕位置和大小
        rect = window.rectangle()
        left, top, right, bottom = rect.left, rect.top, rect.right, rect.bottom
        T = False
    except:
        pass
title_bar_height = 500  # 标题栏高度
border_width = 100      # 边框宽度
under_width = 10      # 底框宽度
print("模型预载成功")#预载模型需要较长时间

def chinese_or_english(text):
    chinese_count = 0
    english_count = 0

    for char in text:
        if '\u4e00' <= char <= '\u9fff' or \
           '\u3400' <= char <= '\u4dbf' or \
           '\u20000' <= char <= '\u2a6df' or \
           '\u3000' <= char <= '\u303f':
            chinese_count += 1
        elif '\u0041' <= char <= '\u005a' or \
             '\u0061' <= char <= '\u007a':
            english_count += 1

    if chinese_count > english_count:
        return "中文"
    elif english_count > chinese_count:
        return "英文"
    else:
        return "混合或无法判断"
    
def myocr(image_path):
    # 识别图片中的文字
    points, words, stats = ocr(image_path, cls=True)
    #print('result:',points , words , stats)
    result = [{'word':words[0][0],'x':(points[0][0][0]+points[0][1][0]+points[0][2][0]+points[0][3][0])/4,'y':(points[0][0][1]+points[0][1][1]+points[0][2][1]+points[0][3][1])/4}]
    for i in range(1,len(points)):
        if words[i][0]=='返回':
            print('返回')
            myclick((points[i][0][0]+points[i][1][0]+points[i][2][0]+points[i][3][0])/4,(points[i][0][1]+points[i][1][1]+points[i][2][1]+points[i][3][1])/4)
            time.sleep(3)
        elif words[i][0]=='开始对战吧！':
            myclick((points[i][0][0]+points[i][1][0]+points[i][2][0]+points[i][3][0])/4,(points[i][0][1]+points[i][1][1]+points[i][2][1]+points[i][3][1])/4)
            print('开始对战吧！')
            time.sleep(0.5)
        elif '能量不足' in words[i][0]:
            myclick((points[0][0][0]+points[0][1][0]+points[0][2][0]+points[0][3][0])/4,(points[0][0][1]+points[0][1][1]+points[0][2][1]+points[0][3][1])/4)
            print('能量不足，等待1min！')
            time.sleep(60)
        elif (points[i-1][2][1]+points[i-1][3][1])/2 > (points[i][0][1]+points[i][1][1]+points[i][2][1]+points[i][3][1])/4 > (points[i-1][0][1]+points[i-1][1][1])/2:
            result[-1]['word']=result[-1]['word']+' '+words[i][0]
        else:
            result.append({'word':words[i][0],'x':(points[i][0][0]+points[i][1][0]+points[i][2][0]+points[i][3][0])/4,'y':(points[i][0][1]+points[i][1][1]+points[i][2][1]+points[i][3][1])/4})
        
    return {
        "problem":result[0],
        "A":result[1],
        "B":result[2],
        "C":result[3],
        "D":result[4]
        }

def choose(data):
    english_sentence = data["problem"]['word']
    options = [data["A"]['word'], data["B"]['word'], data["C"]['word'], data["D"]['word']]
    english_embedding = model.encode([english_sentence])
    option_embeddings = model.encode(options)
    # 使用 Faiss 构建索引
    index = faiss.IndexFlatL2(len(option_embeddings[0]))
    index.add(option_embeddings)
    # 搜索最相似的翻译选项
    D, I = index.search(english_embedding, k=1)
    best_match = options[I[0][0]]
    keys = [key for key in ["A", "B", "C", "D"] if data[key]['word'] == best_match]
    print(best_match)
    return keys[0] if keys else None

def capture_ld_player():
    # 截图
    cropped_image = pyautogui.screenshot(region=(left + border_width, top + title_bar_height , right - left - 2*border_width, bottom - top - title_bar_height - under_width))
    
    # 保存截图
    #filename = f"screenshot.png"
    #cropped_image.save(filename)

    #print(f"截图已保存为：{filename}")
    # 将 PIL.Image 转换为 numpy 数组
    image_array = np.array(cropped_image)
    return image_array  # 返回裁剪后的图像数组

def myclick(x,y):
    try:
        # 点击绝对坐标位置
        mouse.move(left + x + border_width, top + y + title_bar_height, duration=0)
        mouse.click(button='left')
        mouse.move(left, top, duration=0)
        #print("Clicked at (",x,y,") within the window.")
    except Exception as e:
        print(f"Error: {e}")

while 1:
    try:
        word = myocr(capture_ld_player())
        mylogger.info(f"OCR结果: {word}")
        if chinese_or_english(word["problem"]["word"])=='英文' and chinese_or_english(word["A"]["word"])!='英文' and chinese_or_english(word["B"]["word"])!='英文' and chinese_or_english(word["C"]["word"])!='英文' and chinese_or_english(word["D"]["word"])!='英文':
            word["problem"]["word"] = get_mean_cn(word["problem"]["word"])
            if chinese_or_english(word["problem"]["word"])=='英文':
                word["problem"]["word"] = search(word["problem"]["word"])
            if chinese_or_english(word["problem"]["word"])=='英文':
                word["problem"]["word"] = search(word["problem"]["word"])
            mylogger.info(f"转换结果: {word}")
            key = choose(word)
            mylogger.info(f"选择: {key}")
            myclick(word[key]['x'],word[key]['y'])
    except Exception as e:
        #print(e)
        pass
