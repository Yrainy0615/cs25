# -*- coding: utf-8 -*-

'''
牛の検出及びトラッキング用の画像の前処理をまとめたもの
フォルダcalibration, sampling_image.py, split_image.py
を同階層に置いてください
'''
import os
import datetime
import shutil
import cv2
import numpy as np
from glob import glob

import sampling_image as samp_img
from calibration import calibration as calib
import split_image as split_img


#動画からのサンプリング
def sampling_video():
    for videoname in glob("A:/datas_tmp/video/2018-10-12/12/*.avi"): #ここの指定によって対象範囲が変わる
        #動画のファイル名取得
        videonames = videoname.rsplit("\\",1)
        print videoname
        #動画の開始時刻を取得
        ##動画のファイル名から必要な部分を取得
        start_time_string = videonames[1][:-13]
        end_time_string = videonames[1][:11] + videonames[1][-12:-4]
        ##文字列の時刻をdatetime型に変換
        start_time = datetime.datetime.strptime(start_time_string, "%Y-%m-%d %H-%M-%S")
        end_time = datetime.datetime.strptime(end_time_string, "%Y-%m-%d %H-%M-%S")
        print start_time
            
        #動画をサンプリング
        savefolder = "A:/datas_tmp/sampling/"
        samp_img.save_frame_range_sec(videoname, start_time, end_time, 1, savefolder)

#動画の歪み補正(mejiro(旧Axis-silo1)のカラー画像にしか使えません)
def correct_distortion():
    #カメラの内部パラメータを求める
    calib.L_calibration()
    #サンプリング画像がある場所を指定
    foldername = "A:/datas_tmp/sampling/181012_12*/*.jpg*"
    for img_name in glob(foldername):
        undis_img = calib.undistort_img(img_name)

#画像を300*300に分割
def split_image():
    #歪み補正後の画像が保存されている場所を指定
    imagefolder = "A:/datas_tmp/sampling/"
    #保存したい場所を指定
    savefolder =  "A:/datas_tmp/sampling/"

    #分割する画像の範囲を時刻で指定
    startDate = datetime.datetime(2018,10,12,hour=12,minute=00,second=00)
    endDate = datetime.datetime(2018,10,12,hour=13,minute=00,second=00)

    #画像分割
    split_img.split_image(imagefolder, savefolder, startDate, endDate)



if __name__ == '__main__':
    ####　main 画像の前処理　####
    #1. 動画からのサンプリング
    sampling_video()

    '''
    1.5 1のサンプリングがばぐった場合, 何かしらのソフトでサンプリングしてから, 
    file_rename_time.pyでリネームしてください
    '''

    #2. 動画の歪み補正(mejiro(旧Axis-silo1)のカラー画像にしか使えません)
    correct_distortion()

    #3. 画像を300*300に分割
    split_image()
