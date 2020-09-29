# -*- coding: utf-8 -*-

'''
俯瞰動画のサンプリング用プログラム

修士論文後に突貫で書いたのでバグ残ってるかも
使えなかったら画像サンプリングソフトウェア(私はFree Video to JPG Converterを使用)を使ってサンプリングした後、
リネーム(file_rename_time.py)してください.

memo
#めっちゃ赤文字でエラーっぽいの出るから怖いんやけど動いてるみたい
#うまく動かなかったら opencvx.x.x/build/bin のパスを通してください
#(opencv_ffmpegxxx.dllがあるところです)
'''
import os
import datetime
import cv2
import numpy as np
from glob import glob

#step_secごとにstarttimeからendtimeまで動画をサンプリング
def save_frame_range_sec(video_path, start_time, end_time, step_sec, savefolder):
    #動画読み込み
    cap = cv2.VideoCapture(video_path)

    #動画が無い
    if not cap.isOpened():
        print "Can not read video file."
        return

    #savefolderがなかったら作る
    if not os.path.exists(savefolder):
        os.mkdir(savefolder)


    #savefolderの下に開始時刻フォルダを作成
    datestring = start_time.strftime("%y%m%d_%H%M%S")
    savetime_folder = savefolder + "/" + datestring + "/"

    #savetime_folderがなかったら作る
    if not os.path.exists(savetime_folder):
        os.mkdir(savetime_folder)

    #動画のfpsを求める
    fps = cap.get(cv2.CAP_PROP_FPS)

    time = start_time
    while(1):
        #endtimeになったら終了
        if time == end_time:
            break
        #特定の時刻のフレームを求める
        sec = (time - start_time).seconds
        #時間が戻っている動画を発見したためそれを弾く用
        if int(sec) < 0 :
            break 
        n = round(fps * sec)
        cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        ret, frame = cap.read()
        #求めたフレームを保存
        if ret:
            datestring = time.strftime("%y%m%d_%H%M%S")
            savename = savetime_folder + datestring + ".jpg"
            cv2.imwrite(savename, frame)
        #時刻をstep_sec秒増加
        time = time + datetime.timedelta(seconds = int(step_sec))

    return


#テスト用
if __name__ == '__main__':
    for videoname in glob("A:/datas_tmp/video/2018-10-12/*/*.avi"):
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
        save_frame_range_sec(videoname, start_time, end_time, 1, savefolder)
