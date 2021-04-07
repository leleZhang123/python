#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import numpy as np
import cv2
import base64
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
from functools import partial
import RestfulAPI
from pprint import pprint
import multiprocessing as mp

#Yanshee摄像头设置
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32  # 或者为40
rawCapture = PiRGBArray(camera, size=(640, 480))

#色域范围
#设置红色的阈值
lower_red = np.array([160, 40, 40])
upper_red = np.array([179, 255, 255])
#设置绿色的阈值
lower_green = np.array([30, 100, 100])
upper_green = np.array([80, 255, 255])
#设置蓝色的阈值
lower_blue = np.array([100, 100, 100])
upper_blue = np.array([124, 255, 255])
#设置黄色的阈值
lower_yellow = np.array([20, 30, 30])
upper_yellow = np.array([70, 255, 255])
#设置紫色的阈值
lower_purple = np.array([125, 50, 50])
upper_purple = np.array([150, 255, 255])

# HSV颜色空间转换
def get_circles(img):
    x = 0
    y = 0
    z = 0
    # 图形基本转换
    blurred = cv2.GaussianBlur(img, (11, 11), 0)#高斯模糊
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)#转换 hsv
    mask = cv2.inRange(hsv, lower_blue, upper_blue)#生成掩膜

    # 形态学操作
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]   #检测颜色的轮廓
    # 侦测到目标颜色
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), z) = cv2.minEnclosingCircle(c)
    return int(x), int(y), int(z), img


# 读取图片
def getimage(imagename):
    with open(imagename, 'rb') as f:
        img_byte = base64.b64encode(f.read())
    img_str = img_byte.decode('ascii')
    return img_str


ip_addr = "127.0.0.1"  # 调用本地服务
RestfulAPI.RobotInit(ip_addr)

url = "https://lab.qingsteam.cn/practice-web/practice/api/characterTest?accessToken=lw164EZ8oD6KEx60QC7Y8Ch43X290pZt" #接口调用地址
modelId = "d60d54f2377b4122a55dd0be0e20c9f7" #模型id
headers = { "Content-Type": "Application/json"} #请求头


#定义数组
crop_x = [0] * 6
crop_y = [0] * 6
crop_w = [0] * 6
crop_h = [0] * 6
img_str = [0] * 6
# 1号截取区域
'''crop_x[0] = 90
crop_y[0] = 190
crop_w[0] = 185
crop_h[0] = 80
# 2号截取区域
crop_x[1] = 240
crop_y[1] = 195
crop_w[1] = 165
crop_h[1] = 80
# 3号截取区域
crop_x[2] = 335
crop_y[2] = 205
crop_w[2] = 190
crop_h[2] = 80
# 临时停机点截取区域
crop_x[3] = 240
crop_y[3] = 285
crop_w[3] = 165
crop_h[3] = 135
# A号截取区域
crop_x[4] = 10
crop_y[4] = 320
crop_w[4] = 300
crop_h[4] = 175
# B号截取区域
crop_x[5] = 280
crop_y[5] = 310
crop_w[5] = 305
crop_h[5] = 166'''

# 1号截取区域
crop_x[0] = 140
crop_y[0] = 70
crop_w[0] = 120
crop_h[0] = 60
# 2号截取区域
crop_x[1] = 290
crop_y[1] = 50
crop_w[1] = 130
crop_h[1] = 80
# 3号截取区域
crop_x[2] = 420
crop_y[2] =80
crop_w[2] = 120
crop_h[2] = 70
# 临时停机点截取区域
crop_x[3] = 270
crop_y[3] = 140
crop_w[3] = 120
crop_h[3] = 135
# A号截取区域
crop_x[4] = 85
crop_y[4] = 200
crop_w[4] = 170
crop_h[4] = 150
# B号截取区域
crop_x[5] = 370
crop_y[5] = 200
crop_w[5] = 250
crop_h[5] = 160
# 1号区域头部舵机80
# 2号区域头部舵机90
# 3号区域头部舵机104
# 临时停机区域头部舵机90
# A区域头部舵机80
# B区域头部舵机104
angle1 = 80
angle2 = 90
angle3 = 104
angle_ls = 90
angleA = 80
angleB = 104
list_angle = [angle1, angle2, angle3, angle_ls, angleA, angleB]

if __name__ == '__main__':
    RestfulAPI.put_devices_volume(100)#音量调节
    while True:
        time.sleep(1)
        res = RestfulAPI.do_voice_iat_once()#语音识别，iat模式（听写操作）
        words = res["data"]["text"]['ws']#获取识别结果
        result = ""
        for word in words:
            result += word['cw'][0]['w'].encode('utf-8')#对获取结果进行编码串联
        print(result)
        #"开始工作" in result:
        if result == "开始":
            RestfulAPI.put_voice_tts("收到指令！", interrupt=False)
            RestfulAPI.put_motions(name="824")
            time.sleep(3)
            # 侦测1、3号区域时身体姿态
            # 让摄像头进行热身
            #time.sleep(1)
            loopcap = 0
            num = 1
            for capture in camera.capture_continuous(rawCapture,
                                                     format="bgr",
                                                     use_video_port=True):
                # 头部旋转角度
                now_angle = list_angle[num - 1]
                print(now_angle)
                RestfulAPI.put_servos_angles({"NeckLR": now_angle},200)#设置头部旋转角度
                time.sleep(1)
                frame = capture.array#获取图像
                cv2.imshow('1', frame)#显示frame图像
                # 在准备下一帧时清除流
                rawCapture.truncate(0)
                if cv2.waitKey(1) & 0xFF == ord('q'):  # 每帧数据延时 1ms，延时不能为 0，否则读取的结果会是静态帧
                    break
                # 确定裁剪区域
                x = crop_x[num - 1]
                y = crop_y[num - 1]
                w = crop_w[num - 1]
                h = crop_h[num - 1]
                img_crop = frame[(y ):(y + h ), (x ):(x + w ), ]  # 裁剪坐标为[y0:y1, x0:x1]
                if num==1:
                    cv2.imwrite("./mk1.jpg", img_crop)
                    img_str = getimage("./mk1.jpg")
                elif num==3:
                    cv2.imwrite("./mk3.jpg", img_crop)	
                    img_str = getimage("./mk3.jpg")
                        # 存储裁剪完成的图片
                else:
                	cv2.imwrite("./mk.jpg", img_crop)
                	img_str = getimage("./mk.jpg")
                # 打包发送
                img_data = img_data = {"modelId": modelId,"image": "data:image/jpeg;base64,"+img_str}  # 拼接JSON字符串
                json_mod = json.dumps(img_data)
                res = requests.post(url, json_mod, headers=headers, verify=False).text
                json_plain = json.loads(res)
                #print(json_plain)
                time.sleep(0.1)
                # 确认裁剪区域有无目标
                #加入识别可信度score判断,score值越大，可信度越高
                if(json_plain['msg']== u'\u6d4b\u8bd5\u5b8c\u6210\uff0c\u672a\u627e\u5230\u76ee\u6807'):
                    print("NONE")
                    if num == 1:
                        loopcap += 1
                        if loopcap >= 3:
                            num = 3
                            loopcap = 0

                    elif num == 3:
                        loopcap += 1
                        if loopcap >= 3:
                            num = 1
                            loopcap = 0
                #如果有目标1
                elif(json_plain['value'] != None and len(json_plain['value']['rects'])>0  and json_plain['value']['rects'][0]['score'] > 1.2):
                    img_str = json_plain['value']['img']
                    img_decode_ = img_str.encode('ascii')
                    img_decode = base64.b64decode(img_decode_)
                    img_np = np.frombuffer(img_decode, np.uint8)
                    img = cv2.imdecode(img_np, cv2.COLOR_RGB2BGR)
                    cv2.imshow('img1', img)
                    cv2.waitKey(1)
                    if num == 1:
                        # 语音播报
                        RestfulAPI.put_voice_tts("飞机在1号降落位置！", interrupt=False)
                        time.sleep(3)
                        # 调用动作库，指挥飞机转移
                        RestfulAPI.put_motions(name="turn_right_motion", repeat=3)
                        time.sleep(2)
                    elif num == 3:
                        # 语音播报
                        RestfulAPI.put_voice_tts("飞机在3号降落位置！", interrupt=False)
                        time.sleep(3)
                        # 调用动作库，指挥飞机转移
                        RestfulAPI.put_motions(name="turn_left_motion", repeat=3)
                        time.sleep(2)
                    break
                # 1、3号位置轮流侦测设置
                else:
                    print("NONE")
                    if num == 1:
                        loopcap += 1
                        if loopcap >= 3:
                            num = 3
                            loopcap = 0

                    elif num == 3:
                        loopcap += 1
                        if loopcap >= 3:
                            num = 1
                            loopcap = 0
            # 结束tts语音合成
            RestfulAPI.delete_voice_tts()
            # 侦测2号区域时身体姿态
            RestfulAPI.put_motions(name="824")
            time.sleep(2)
            # 2号区域确认
            num = 2
            for capture in camera.capture_continuous(rawCapture,
                                                     format="bgr",
                                                     use_video_port=True):
                now_angle = list_angle[num - 1]
                RestfulAPI.put_servos_angles({"NeckLR": now_angle})
                time.sleep(1)
                frame = capture.array
                cv2.imshow('1', frame)
                # 在准备下一帧时清除流
                rawCapture.truncate(0)
                if cv2.waitKey(1) & 0xFF == ord('q'):  # 每帧数据延时 1ms，延时不能为 0，否则读取的结果会是静态帧
                    break
                x = crop_x[num - 1]
                y = crop_y[num - 1]
                w = crop_w[num - 1]
                h = crop_h[num - 1]
                img_crop = frame[(y + 5):(y + h + 5), (x + 5):(x + w + 5), ]  # 裁剪坐标为[y0:y1, x0:x1]
                if num==2:
                    cv2.imwrite("./mk2.jpg", img_crop)
                    img_str = getimage("./mk2.jpg")
                else:
                	cv2.imwrite("./mk.jpg", img_crop)
                	img_str = getimage("./mk.jpg")
                img_data = {"modelId": modelId,"image": "data:image/jpeg;base64,"+img_str}  # 拼接JSON字符串
                json_mod = json.dumps(img_data)
                res = requests.post(url, json_mod, headers=headers, verify=False).text
                json_plain = json.loads(res)
                time.sleep(0.1)
                # 确认裁剪区域有无目标
                # 加入识别可信度score判断,score值越大，可信度越高
                #print(json_plain['value'])
                if(json_plain['msg']== u'\u6d4b\u8bd5\u5b8c\u6210\uff0c\u672a\u627e\u5230\u76ee\u6807'):
                    print("NONE")
                #如果有目标2
                elif(json_plain['value'] != None and len(json_plain['value']['rects'])>0  and json_plain['value']['rects'][0]['score'] > 1):
                    img_str = json_plain['value']['img']
                    img_decode_ = img_str.encode('ascii')
                    img_decode = base64.b64decode(img_decode_)
                    img_np = np.frombuffer(img_decode, np.uint8)
                    img = cv2.imdecode(img_np, cv2.COLOR_RGB2BGR)
                    cv2.imshow('img1', img)
                    cv2.waitKey(1)
                    RestfulAPI.put_voice_tts("飞机在2号降落位置！", interrupt=False)
                    time.sleep(2)
                    break
            RestfulAPI.delete_voice_tts()
            RestfulAPI.put_voice_tts("正常停止！", interrupt=False)
            RestfulAPI.put_motions(name="stop_motion")
            time.sleep(4)
            RestfulAPI.put_voice_tts("走向廊桥！", interrupt=False)
            time.sleep(2)
            RestfulAPI.put_motions(name="forward_motion", repeat=3)
            time.sleep(2)
            RestfulAPI.put_motions(name="824")
            time.sleep(2)
            # 临时停机位确认
            num = 4
            for capture in camera.capture_continuous(rawCapture,
                                                     format="bgr",
                                                     use_video_port=True):
                now_angle = list_angle[num - 1]
                RestfulAPI.put_servos_angles({"NeckLR": now_angle})
                time.sleep(1)
                frame = capture.array
                cv2.imshow('1', frame)
                # 在准备下一帧时清除流
                rawCapture.truncate(0)
                if cv2.waitKey(1) & 0xFF == ord('q'):  # 每帧数据延时 1ms，延时不能为 0，否则读取的结果会是静态帧
                    break
                x = crop_x[num - 1]
                y = crop_y[num - 1]
                w = crop_w[num - 1]
                h = crop_h[num - 1]
                img_crop = frame[(y + 5):(y + h + 5), (x + 5):(x + w + 5), ]  # 裁剪坐标为[y0:y1, x0:x1]
                if num==4:
                    cv2.imwrite("./mk4.jpg", img_crop)
                    img_str = getimage("./mk4.jpg")
                else:
                	cv2.imwrite("./mk.jpg", img_crop)
                	img_str = getimage("./mk.jpg")
                img_data = {"modelId": modelId,"image": "data:image/jpeg;base64,"+img_str}  # 拼接JSON字符串
                json_mod = json.dumps(img_data)
                res = requests.post(url, json_mod, headers=headers, verify=False).text
                json_plain = json.loads(res)
                time.sleep(1)
                # 确认裁剪区域有无目标
                # 加入识别可信度score判断,score值越大，可信度越高
                if(json_plain['msg']== u'\u6d4b\u8bd5\u5b8c\u6210\uff0c\u672a\u627e\u5230\u76ee\u6807'):
                    print("NONE")
                #如果有目标3
                elif(json_plain['value'] != None and len(json_plain['value']['rects'])>0  and json_plain['value']['rects'][0]['score'] > 1):
                    img_str = json_plain['value']['img']
                    img_decode_ = img_str.encode('ascii')
                    img_decode = base64.b64decode(img_decode_)
                    img_np = np.frombuffer(img_decode, np.uint8)
                    img = cv2.imdecode(img_np, cv2.COLOR_RGB2BGR)
                    cv2.imshow('img1', img)
                    cv2.waitKey(1)
                    RestfulAPI.put_voice_tts("飞机在临时停机位！", interrupt=False)
                    time.sleep(2)
                    break
            RestfulAPI.delete_voice_tts()
            RestfulAPI.put_voice_tts("紧急情况处理，出现火情！", interrupt=False)
            time.sleep(1)
            RestfulAPI.put_motions(name="fire_motion", repeat=2)
            RestfulAPI.put_media_music(
                operation="start", name="fire.mp3")
            time.sleep(3)
            time.sleep(1)
            RestfulAPI.put_voice_tts("开始停机入位！", interrupt=False)
            time.sleep(1)

            # camera.close()
            RestfulAPI.put_motions(name="824")
            time.sleep(1)
            num = 5
            loopcap = 0
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                now_angle = list_angle[num - 1]
                RestfulAPI.put_servos_angles({"NeckLR": now_angle})
                time.sleep(1)
                image = frame.array
                x, y, z, kl = get_circles(image)
                center_x = x
                center_y = y
                radius = z
                rawCapture.truncate(0)
                if (z > 15):
                    cv2.circle(kl, (x, y), z, (0, 255, 0), 5)
                cv2.imshow('Color_tracking', kl)
                print("x="+str(x)+",y="+str(y))

                if ((x > crop_x[num - 1]) and x < (crop_x[num - 1] + crop_w[num - 1])):
                    if num == 5:
                        RestfulAPI.put_voice_tts("B号停机位可用", interrupt=False)
                        num = 6
                        time.sleep(3)
                        RestfulAPI.put_motions(name="turn_left_motion", repeat=3)
                        time.sleep(2)

                    elif num == 6:
                        RestfulAPI.put_voice_tts("A号停机位可用", interrupt=False)
                        num = 5
                        time.sleep(3)
                        RestfulAPI.put_motions(name="turn_right_motion", repeat=3)
                        time.sleep(2)
                    break
                else:
                    if num == 5:
                        loopcap += 1
                        if loopcap >= 3:
                            num = 6
                            loopcap = 0

                    elif num == 6:
                        loopcap += 1
                        if loopcap >= 3:
                            num = 5
                            loopcap = 0
                # 停机区域确认
            RestfulAPI.delete_voice_tts()
            time.sleep(1)
            RestfulAPI.put_motions(name="824")
            time.sleep(1)
            # num = ?
            for capture in camera.capture_continuous(rawCapture,
                                                     format="bgr",
                                                     use_video_port=True):
                now_angle = list_angle[num - 1]
                RestfulAPI.put_servos_angles({"NeckLR": now_angle})
                time.sleep(1)
                frame = capture.array
                cv2.imshow('1', frame)
                # 在准备下一帧时清除流
                rawCapture.truncate(0)
                if cv2.waitKey(1) & 0xFF == ord('q'):  # 每帧数据延时 1ms，延时不能为 0，否则读取的结果会是静态帧
                    break
                x = crop_x[num - 1]
                y = crop_y[num-1]
                w = crop_w[num - 1]
                h = crop_h[num - 1]
                img_crop = frame[(y ):(y + h ), (x):(x + w), ]  # 裁剪坐标为[y0:y1, x0:x1]
                if num == 5:
                	cv2.imwrite("./mk5.jpg", img_crop)
                	img_str = getimage("./mk5.jpg")
                if num == 6:
                	cv2.imwrite("./mk6.jpg", img_crop)
                	img_str = getimage("./mk6.jpg")
                img_data = {"modelId": modelId,"image": "data:image/jpeg;base64,"+img_str}  # 拼接JSON字符串
                json_mod = json.dumps(img_data)
                res = requests.post(url, json_mod, headers=headers, verify=False).text
                json_plain = json.loads(res)
                time.sleep(1)
                # 确认裁剪区域有无目标
                # 加入识别可信度score判断,score值越大，可信度越高
                if(json_plain['msg']== u'\u6d4b\u8bd5\u5b8c\u6210\uff0c\u672a\u627e\u5230\u76ee\u6807'):
                    print("NONE")
                #如果有目标4
                elif(json_plain['value'] != None and len(json_plain['value']['rects'])>0  and json_plain['value']['rects'][0]['score'] > 0.8):
                    img_str = json_plain['value']['img']
                    img_decode_ = img_str.encode('ascii')
                    img_decode = base64.b64decode(img_decode_)
                    img_np = np.frombuffer(img_decode, np.uint8)
                    img = cv2.imdecode(img_np, cv2.COLOR_RGB2BGR)
                    cv2.imshow('img1', img)
                    cv2.waitKey(1)
                    if num == 5:
                        RestfulAPI.put_voice_tts("飞机已在A停机位停好！", interrupt=False)
                        time.sleep(3)
                    elif num == 6:
                        RestfulAPI.put_voice_tts("飞机已在B停机位停好！", interrupt=False)
                        time.sleep(3)
                    break
            RestfulAPI.delete_voice_tts()
            time.sleep(2)
            RestfulAPI.put_voice_tts("飞机停机成功！", interrupt=False)
            time.sleep(2)
            RestfulAPI.put_voice_tts("我的工作已完成！", interrupt=False)
            # camera.close()
            time.sleep(2)

            RestfulAPI.delete_voice_tts()
            RestfulAPI.put_motions(name="stand_up_motion")
            time.sleep(1)
            #######向休息区移动######
            RestfulAPI.put_motions(name="reset")
            time.sleep(3)
            #右转
            RestfulAPI.put_motions(name="turnright", repeat=3)
            time.sleep(0.5)
            time.sleep(3)
            RestfulAPI.put_motions(name="reset")
            time.sleep(0.5)
            RestfulAPI.put_motions(name="turnright", repeat=3)
            time.sleep(3)
            RestfulAPI.put_motions(name="003",repeat=1)
            time.sleep(2)
            RestfulAPI.put_motions(name="reset")
            time.sleep(1)
            while True:
                res = RestfulAPI.get_motions()
                if res["data"]["status"] == "idle" :
                    break
            time.sleep(0.5)
            #直走                 
            RestfulAPI.put_motions(name="Forward")
            time.sleep(35)
            #RestfulAPI.put_motions(name="003",repeat=1)
            time.sleep(2)
            RestfulAPI.put_motions(name="reset")
            time.sleep(1)
            # a = 70
            # res = RestfulAPI.put_servos_angles(
            #     {"RightAnkleFB": 90 + a, "LeftAnkleFB": 90 - a, "RightKneeFlex": 90 - a, "LeftKneeFlex": 90 + a}, 1000)
            RestfulAPI.put_motions(name="squat_down_motion")
            time.sleep(3)
            break

camera.close()
cv2.destroyAllWindows()
