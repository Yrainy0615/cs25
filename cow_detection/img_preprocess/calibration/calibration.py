# -*- coding: utf-8 -*-

'''
カメラのキャリブレーション用コード
files = glob("C:/tmp/calibration/*.jpg*")
内の画像の補正を行う by山下

上を基にした画像の歪み補正用コード
by青谷

'''

import numpy
import cv2
import os.path
from glob import glob

#左のカメラのキャリブレーション
#俯瞰画像の歪み補正に流用
#カメラの内部パラメータを求める
def L_calibration():
	square_size = 2.4     # 正方形のサイズ
	pattern_size = (10, 7)  # 模様のサイズ
	pattern_points = numpy.zeros( (numpy.prod(pattern_size), 3), numpy.float32 ) #チェスボード（X,Y,Z）座標の指定 (Z=0)
	pattern_points[:,:2] = numpy.indices(pattern_size).T.reshape(-1, 2)
	pattern_points *= square_size
	obj_points = []
	global img_pointsL
	img_pointsL = []
	
	#for fn in glob("C:/tmp/calibration/camera1_new/*.jpg*"):
	for fn in glob("A:/datas/camera1_new/*.jpg*"): #キャリブレーション用の画像がある場所を指定
		# 画像の取得
		im = cv2.imread(fn, 0)
		#im = cv2.resize(im, (960,540))
		#print "loading..." + fn
		# チェスボードのコーナーを検出
		found, corner = cv2.findChessboardCorners(im, pattern_size)
		# コーナーがあれば
		if found:
			term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
			corners2 = cv2.cornerSubPix(im, corner, (5,5), (-1,-1), term)
		# コーナーがない場合のエラー処理
		if not found:
			print fn + ": chessboard not found"
			continue
		img_pointsL.append(corner.reshape(-1, 2))   #appendメソッド：リストの最後に因数のオブジェクトを追加
		obj_points.append(pattern_points)
		#corner.reshape(-1, 2) : 検出したコーナーの画像内座標値(x, y)
		
		#draw
		im = cv2.drawChessboardCorners(im, (10,7), corners2,found)
		#####cv2.imshow('img',im)
		#####k = cv2.waitKey(30)
		#if k == ord('s'):
			#cv2.imwrite('test_sample.jpg',im)
		#cv2.waitKey(500)
		
	cv2.destroyAllWindows()
	
	# 内部パラメータを計算
	global Kl, dl
	rmsl, Kl, dl, r, t = cv2.calibrateCamera(obj_points,img_pointsL,(im.shape[1],im.shape[0]),None, None)
	# 計算結果を表示
	print "RMS_L = ", rmsl
	print "K_L = \n", Kl
	print "d_L = ", dl.ravel()
	
	#画像の歪み補正
	#image_name:画像のファイル名
def undistort_img(image_name):
	img = cv2.imread(image_name)
	(head,tail) = os.path.split(image_name)
	head = head.rsplit("\\",1)
	#print head
	#画像の大きさを取得
	h, w = img.shape[:2]
	#内部パラメータを取得
	newcameramtx, roi=cv2.getOptimalNewCameraMatrix(Kl,dl,(w,h),1,(w,h))
	#画像の歪み補正
	dst = cv2.undistort(img,Kl,dl,None,newcameramtx)
	#cv2.imshow('calibimg',dst)
	#cv2.waitKey(0)
	#print newcameramtx
	#print "roi=",roi
	#歪み補正でできたいらない部分を切り取る
	x,y,w,h = roi
	dst = dst[y:y+h, x:x+w]
	#cv2.imshow('calibimg',dst)
	#cv2.waitKey(0)
	#保存先を指定
	savefolder = head[0] + "/ud_" + head[1]
	savename = savefolder + "/ud_"+tail
	##print savename
	#画像を保存
	if not os.path.exists(savefolder):
		os.mkdir(savefolder)
	cv2.imwrite(savename, dst)
	return dst


#点の歪み補正
#なんか上手くいかない
#point: [x,y]
def undistort_point(point):
	pointlist = []
	pointlist.append([1323,352])
	pointlist.append(point)
	#new_KL = numpy.array([])
	print pointlist
	new_pt = cv2.undistortPoints(numpy.array([pointlist]).astype('float32'), Kl, dl, P=Kl)[0]
	print new_pt
	#roi:x,y,w,h:31,103,1863,871
	new_pt_x = new_pt[1][0]
	new_pt_y = new_pt[1][1]
	new_pt_x = new_pt_x-31
	new_pt_y = new_pt_y-103
	return [new_pt_x, new_pt_y]

#右のカメラのキャリブレーション
def R_calibration():
	square_size = 2.4      # 正方形のサイズ
	pattern_size = (10, 7)  # 模様のサイズ
	pattern_points = numpy.zeros( (numpy.prod(pattern_size), 3), numpy.float32 ) #チェスボード（X,Y,Z）座標の指定 (Z=0)
	pattern_points[:,:2] = numpy.indices(pattern_size).T.reshape(-1, 2)
	pattern_points *= square_size
	global obj_points, img_pointsR
	obj_points = []
	img_pointsR = []
	
	for fn in glob("C:/tmp/calibration/R/*.jpg*"):
		# 画像の取得
		im = cv2.imread(fn, 0)
		im = cv2.resize(im, (960,540))
#		print "loading..." + fn
		# チェスボードのコーナーを検出
		found, corner = cv2.findChessboardCorners(im, pattern_size)
		# コーナーがあれば
		if found:
			term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
			cv2.cornerSubPix(im, corner, (5,5), (-1,-1), term)
		# コーナーがない場合のエラー処理
		if not found:
			print fn + ": chessboard not found"
			continue
		img_pointsR.append(corner.reshape(-1, 2))   #appendメソッド：リストの最後に因数のオブジェクトを追加
		obj_points.append(pattern_points)
		#corner.reshape(-1, 2) : 検出したコーナーの画像内座標値(x, y)
		
	# 内部パラメータを計算
	global Kr,dr
	rmsr, Kr, dr, r, t = cv2.calibrateCamera(obj_points,img_pointsR,(im.shape[1],im.shape[0]),None,None)
	# 計算結果を表示
	print "RMS_R = ", rmsr
	print "K_R = \n", Kr
	print "d_R = ", dr.ravel()
	
	

def example():
	imgU1 = numpy.zeros((960,540,3), numpy.uint8)
	
	files = glob("C:/tmp/calibration/*.jpg*")
	
	#sift_keypoints print
	for file in files:
		if 'L' in file:
			img1 = cv2.imread(file)
			img1 = cv2.resize(img1, (960,540))
			imgU1 = cv2.remap(img1, maplx, maply, cv2.INTER_LINEAR, imgU1, cv2.BORDER_CONSTANT, 0)
			filename = file.replace('.jpg', '_C.jpg')
			cv2.imwrite(filename, imgU1)
		
		if 'R' in file:
			img2 = cv2.imread(file)
			img2 = cv2.resize(img2, (960,540))
			imgU2 = cv2.remap(img2, maprx, mapry, cv2.INTER_LINEAR)
			filename = file.replace('.jpg', '_C.jpg')
			cv2.imwrite(filename, imgU2)

if __name__ == '__main__':
	L_calibration()
	foldername = "C:/tmp/calibration/distort/*/*.jpg*"
	for img_name in glob(foldername):
		undis_img = undistort_img(img_name)
	#R_calibration()
	
