import numpy as np
import win32gui
import pyautogui
from PIL import Image
import re
import time
from pywinauto.application import Application
import logging
import json
import requests
import re
import pydirectinput
import mouse
from paddleocr import PaddleOCR, draw_ocr
from baicizhanciku.find import appenddb

# 针对 paddleocr 的日志记录器单独配置
paddle_logger = logging.getLogger('ppocr')
paddle_logger.setLevel(logging.ERROR)  # 忽略 INFO 和 WARNING 级别的日志
#预载模型需要较长时间
ocr = PaddleOCR(use_angle_cls=False, lang="ch",cls_model_dir="ocr//cls_model")
print("模型预载成功")#预载模型需要较长时间
    
T = True
while T:
    try:
        window_title = "百词斩单词查询"  # 替换为你的雷电模拟器窗口标题
        # 连接到雷电模拟器窗口
        app = Application(backend="uia").connect(title=window_title)
        window = app.window(title=window_title)

        # 获取窗口的屏幕位置和大小
        rect = window.rectangle()
        left2, top2, right2, bottom2 = rect.left, rect.top, rect.right, rect.bottom
        T = False
    except:
        pass
title_bar_height2 = 70  # 标题栏高度
border_width2 = 30      # 边框宽度
under_width2 = 600      # 底框宽度
    
def myocr(image_path):
    # 识别图片中的文字
    points, words, stats = ocr(image_path, cls=True)
    #print('result:',points , words , stats)
    result = [{'word':words[0][0],'x':(points[0][0][0]+points[0][1][0]+points[0][2][0]+points[0][3][0])/4,'y':(points[0][0][1]+points[0][1][1]+points[0][2][1]+points[0][3][1])/4}]
    for i in range(1,len(points)):
        if (points[i-1][2][1]+points[i-1][3][1])/2 > (points[i][0][1]+points[i][1][1]+points[i][2][1]+points[i][3][1])/4 > (points[i-1][0][1]+points[i-1][1][1])/2:
            result[-1]['word']=result[-1]['word']+' '+words[i][0]
            result[-1]['x']=result[-1]['x']/2+(points[i][0][0]+points[i][1][0]+points[i][2][0]+points[i][3][0])/8
        else:
            result.append({'word':words[i][0],'x':(points[i][0][0]+points[i][1][0]+points[i][2][0]+points[i][3][0])/4,'y':(points[i][0][1]+points[i][1][1]+points[i][2][1]+points[i][3][1])/4})
    return result

def capture_ld_player():
    # 截图
    cropped_image = pyautogui.screenshot(region=(left2 + border_width2, top2 + title_bar_height2 , right2 - left2 - 2*border_width2, bottom2 - top2 - title_bar_height2 - under_width2))
    
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
        mouse.move(left2 + x + border_width2, top2 + y + title_bar_height2, duration=0)
        mouse.click(button='left')
        mouse.move(left2, top2, duration=0)
        #print("Clicked at (",x,y,") within the window.")
    except Exception as e:
        print(f"Error: {e}")


def search(word):
    try:
        raw = word
        myclick(380,50)
        pydirectinput.PAUSE = 0.01
        time.sleep(0.4)
        pydirectinput.keyDown('ctrl')
        pydirectinput.keyDown('a')
        pydirectinput.keyUp('ctrl')
        pydirectinput.keyUp('a')
        pydirectinput.press('delete')
        pydirectinput.write(word.lower())
        pydirectinput.press('enter')
        time.sleep(0.6)
        myclick(320,220)
        time.sleep(0.5)
        word = myocr(capture_ld_player())
        ch=''
        #print(word)
        for term in word[2:]:
            if '.' in term['word']:
                ch = ch+term['word']+'   '
            elif ch!='':
                break
        appenddb(word[1]["word"],ch)
        return ch
    
    except Exception as e:
        print(e)
        return raw

if __name__ == "__main__":
    print(search('help'))
    print(search('man'))
    print(search('can'))
