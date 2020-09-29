# -*- coding: utf-8 -*-

'''
SSDに使用するために画像を300×300に分割するプログラム
カメラによって分割位置を変更
'''

import cv2
import numpy as np
import os
import datetime

#縦
split_height = 300
#横
split_width = 300
#カメラから遠いほう、重ね合わせる幅
overlap_pixel1 = 50
#カメラから近いほう、重ね合わせる幅
overlap_pixel2 = 80

#imagefile = "F:/usi/TimeData/170613/170613_140000/140001.jpg"
#imagefolder = "F:/annotation_files_silo2/"
#imagefolder = "F:/usi/TimeData/"
#savefolder = "Y:/PastureImages/split2/"
#savefolder2 = "X:/aotani/ssd_test_image/test_silo2/"
#Date = datetime.datetime(2018,10,12,hour=6,minute=00,second=00)

#mejiro(旧Axis-silo1)のカラー画像用設定
def init_silo1_rgb():
    distant_x = 30
    distant_y = 300
    near_x = 530
    near_y = 550
    split_range = 7
    split_end = 11
    return distant_x,distant_y,near_x,near_y,split_range,split_end

#roba(旧Axis-silo2)のカラー画像用設定
def init_silo2_rgb():
    distant_x = 300
    distant_y = 200
    near_x = 600
    near_y = 450
    split_range = 6
    split_end = 11
    return distant_x,distant_y,near_x,near_y,split_range,split_end

#画像を300*300に分割して保存
def split_image(imagefolder, savefolder, startDate, endDate):
    #初期化
    Date = startDate
    while(1):
        #カメラによって変更
        distant_x,distant_y,near_x,near_y,split_range,split_end = init_silo1_rgb()
        if Date == endDate:
            break
        datestring = Date.strftime("%y%m%d_%H%M%S")
        print datestring
        imagefile = imagefolder + "ud_" + datestring[:10] + "000/" + "ud_" + datestring + ".jpg"

        #画像読み込み
        image = cv2.imread(imagefile)
        if image is not None:
            im_cp = image.copy()

        #カメラから遠い部分切り出し
        for i in range(1, int(split_range)):
            if image is None:
                print "No image"
                break

            #画像を分割する
            dst = image[distant_y:distant_y+split_height, distant_x:distant_x+split_width]
            #分割位置を矩形で描画
            cv2.rectangle(im_cp, (distant_x, distant_y), (distant_x+split_height, distant_y+split_width), (0, 0, 255))

            #保存するフォルダを作成
            if not os.path.exists(savefolder + "ud_" + datestring[:10] + "000s/"):
                os.mkdir(savefolder + "ud_" + datestring[:10] + "000s/")
            savename = savefolder + "ud_" + datestring[:10] + "000s/" + "ud_" + datestring + "_0" + str(i) + ".jpg"

            #分割位置表示
            #cv2.imshow("all", im_cp)
            #cv2.waitKey(0)

            #分割画像保存
            cv2.imwrite(savename,dst)
            distant_x = distant_x + split_height - overlap_pixel1
            cv2.destroyAllWindows()

        #カメラから近い部分切り出し
        for i in range(int(split_range), int(split_end)):
            if image is None:
                print "No image"
                break

            #画像を分割する
            dst = image[near_y:near_y+split_height, near_x:near_x+split_width]
            #分割位置を矩形で描画
            cv2.rectangle(im_cp, (near_x, near_y), (near_x+split_height, near_y+split_width), (0, 0, 255))

            #保存するフォルダを作成
            if i < 10 :
                savename = savefolder + "ud_" + datestring[:10] + "000s/" + "ud_" + datestring + "_0" + str(i) + ".jpg"
            else :
                savename = savefolder + "ud_" + datestring[:10] + "000s/" + "ud_" + datestring + "_" + str(i) + ".jpg"

            #分割位置表示
            #cv2.imshow("all", im_cp)
            #cv2.waitKey(0)

            #分割画像保存
            cv2.imwrite(savename,dst)
            near_x = near_x + split_height - overlap_pixel2
            cv2.destroyAllWindows()

        #時間を1s進める
        Date = Date+datetime.timedelta(seconds = 1)

#テスト用
if __name__ == '__main__':
    while(1):
        Date = Date+datetime.timedelta(seconds = 1)
        datestring = Date.strftime("%y%m%d_%H%M%S")
        print datestring
        imagefile = imagefolder + datestring[:6] + "/" + datestring[:10] + "000/" +  datestring + ".jpg"

        #if Date.minutes == 30:
        #    break

        if Date.hour == 18:
            break

        image = cv2.imread(imagefile)
        if image is not None:
            im_cp = image.copy()

        #カメラから遠い部分切り出し
        #silo1
        x = 30
        y = 300
        #silo2
        x = 300
        y = 200
        #silo1:range 1-7
        #silo2:range 1-6
        for i in range(1,6):
            if image is None:
                print "No image"
                break

            dst = image[y:y+split_height, x:x+split_width]
            cv2.rectangle(im_cp, (x, y), (x+split_height, y+split_width), (0, 0, 255))
            #silo1
            '''
            if not os.path.exists(savefolder + "ud_" + datestring[:10] + "000s/"):
                os.mkdir(savefolder + "ud_" + datestring[:10] + "000s/")
            if not os.path.exists(savefolder2 + "ud_" + datestring[:10] + "000s/"):
                os.mkdir(savefolder2 + "ud_" + datestring[:10] + "000s/")
            '''
            savename = savefolder + "ud_" + datestring[:10] + "000s/" + "ud_" + datestring + "_0" + str(i) + ".jpg"
            savename2 = savefolder2 + "ud_" + datestring[:10] + "000s/" + "ud_" + datestring + "_0" + str(i) + ".jpg"   
            
            #silo2
            if not os.path.exists(savefolder2 + datestring[:10] + "000s/"):
                os.mkdir(savefolder2 + datestring[:10] + "000s/")
            savename2 = savefolder2 + datestring[:10] + "000s/" + datestring + "_0" + str(i) + ".jpg"   
            
            #共通
            #cv2.imshow("all", im_cp)
            #cv2.waitKey(0)
            cv2.imwrite(savename,dst)
            cv2.imwrite(savename2,dst)
            x = x + split_height - overlap_pixel1
            cv2.destroyAllWindows()

        #カメラから近い部分切り出し
        #silo1
        x = 530
        y = 550
        #silo2
        x = 600
        y = 450
        #silo1:range 7-11
        #silo2:range 6-11
        for i in range(6,11):
            if image is None:
                print "No image"
                break

            dst = image[y:y+split_height, x:x+split_width]
            cv2.rectangle(im_cp, (x, y), (x+split_height, y+split_width), (0, 0, 255))
            #silo1
            '''
            if i < 10 :
                savename = savefolder + "ud_" + datestring[:10] + "000s/" + "ud_" + datestring + "_0" + str(i) + ".jpg"
                savename2 = savefolder2 + "ud_" + datestring[:10] + "000s/" + "ud_" + datestring + "_0" + str(i) + ".jpg"
            else :
                savename = savefolder + "ud_" + datestring[:10] + "000s/" + "ud_" + datestring + "_" + str(i) + ".jpg"
                savename2 = savefolder2 + "ud_" + datestring[:10] + "000s/" + "ud_" + datestring + "_" + str(i) + ".jpg"
            '''
            #silo2
            if i < 10 :
                savename2 = savefolder2 + datestring[:10] + "000s/" + datestring + "_0" + str(i) + ".jpg"
            else :
                savename2 = savefolder2 + datestring[:10] + "000s/" + datestring + "_" + str(i) + ".jpg"

            #共通
            #cv2.imshow("all", im_cp)
            #cv2.waitKey(0)
            cv2.imwrite(savename,dst)
            cv2.imwrite(savename2,dst)
            x = x + split_height - overlap_pixel2
            cv2.destroyAllWindows()
