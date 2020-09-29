# -*- coding: utf-8 -*-

'''
フォルダ内のファイルを時刻にリネームするプログラム
datelistに指定した時刻のフォルダに対してリネームを行う
sampling_image.pyがうまく動かなかったら使ってください
(修士論文後に整理してないので読みにくいと思いますが)
'''

import os
import shutil
from glob import glob
import datetime

#フォルダ名(サンプリングした画像のある場所を指定)
#ここで指定した場所以下のフォーマットは ./yymmdd_HHMMSS/*.jpg　とし, 時刻どおりに並べておく
#folder = "F:/usi/TimeData/180304/180302_120000"
folder2 = "F:/usi/TimeData/181011/"
#セーブするフォルダ名
#savefolder = "F:/annotation_files/180302_120000"
savefolder2 = "F:/annotation_files/"
#ここにリネームしたい時刻を指定(フォルダごと)
datelist = ["181011_06","181011_07","181011_08","181011_09","181011_12","181011_13","181011_14","181011_15","181011_16","181011_17"]
#ここはそのままでok. datelistとminutelistを結合することでファイル探索
minutelist = ["0000","1000","2000","3000","4000","5000"]

def rename_time(Date, file):
    #時間だけ取り出し
    Time = Date.time()
    #文字列に変換
    timestring = Time.strftime("%H%M%S")
    #新しいファイル名つくる
    newname = folder+"/"+timestring+".jpg"
    print newname

    ##rename(copy)
    #shutil.copy(file, newname)
    ##rename(move)
    os.rename(file, newname)
    #return Date

def rename_datetime(Date, file):
    #文字列に変換
    datestring = Date.strftime("%y%m%d_%H%M%S")
    #新しいファイル名つくる
    newname = savefolder+"/"+datestring+".jpg"
    print newname
    ##rename(copy)
    shutil.copy(file, newname)
    ##rename(move)
    ##os.rename(file, newname)


if __name__ == '__main__':
    #ファイル探索
    for date1 in datelist:
        for minute1 in minutelist:
            folder = folder2 + date1 + minute1
            savefolder = savefolder2 + date1 + minute1
            aDate = datetime.datetime.strptime(date1 + minute1, "%y%m%d_%H%M%S")
            print folder,savefolder,aDate
            ####date_string = aDate.strftime("%y%m%d_%H%M%S")
            if os.path.exists(folder):
                if not os.path.exists(savefolder):
                    os.mkdir(savefolder)
            
                for file1 in glob(folder+"/*.jpg*"):
                    print file1
                    aDate = aDate+datetime.timedelta(seconds = 1)
                    rename_datetime(aDate, file1)
                    rename_time(aDate, file1)
        
       

    