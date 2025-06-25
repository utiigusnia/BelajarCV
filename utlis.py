import cv2
import numpy as np

def getContours(img, minArea=1000, filter=0, cThr=[100, 100], draw=True):
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1]) # Canny Edge Detection
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=3)
    imgThresh = cv2.erode(imgDial, kernel, iterations=2)

    contours, hierarchy = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    finalContours = []
    imgContourDraw = img.copy() # Salinan untuk menggambar kontur (jika draw=True)

    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx) # Dapatkan bounding box untuk setiap kontur

            if filter > 0: # Jika filter sudut ditentukan
                if len(approx) == filter:
                    finalContours.append([area, peri, approx, (x, y, w, h)])
                    if draw:
                        cv2.drawContours(imgContourDraw, [approx], -1, (0, 0, 255), 3) # Merah untuk kontur filtered
            else: # Jika tidak ada filter sudut (filter = 0)
                finalContours.append([area, peri, approx, (x, y, w, h)])
                if draw:
                    cv2.drawContours(imgContourDraw, [approx], -1, (255, 0, 0), 2) # Biru untuk kontur umum

    finalContours = sorted(finalContours, key=lambda x: x[0], reverse=True) # Urutkan berdasarkan area
    return imgContourDraw, finalContours

def reorder(myPoints):
    """
    Mengurutkan 4 titik sudut dari kontur agar selalu dalam urutan tertentu
    (top-left, top-right, bottom-left, bottom-right). Penting untuk warpImg.
    """
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)] # [0,0] Top Left
    myPointsNew[3] = myPoints[np.argmax(add)] # [width,height] Bottom Right
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)] # [width,0] Top Right
    myPointsNew[2] = myPoints[np.argmax(diff)] # [0,height] Bottom Left
    return myPointsNew

def warpImg(img, biggest, w, h):
    """
    Melakukan transformasi perspektif untuk meluruskan gambar berdasarkan 4 titik kontur.
    Digunakan untuk meluruskan objek referensi (misalnya A4).
    (Fungsi ini tetap ada di utlis.py, meskipun tidak dipanggil di ObjectMeasurement.py baru)
    """
    biggest = reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (w, h))
    # Opsional: crop sedikit untuk menghilangkan noise tepi setelah warping
    imgCropped = imgOutput[20:imgOutput.shape[0]-20, 20:imgOutput.shape[1]-20]
    imgCropped = cv2.resize(imgCropped, (w, h))
    return imgCropped

# findDis tidak digunakan
# def findDis(pts1, pts2):
#     return ((pts2[0] - pts1[0]) ** 2 + (pts2[1] - pts1[1]) ** 2) ** 0.5

"""
    Mendeteksi kontur dalam gambar.

    Args:
        img: Gambar input (BGR).
        minArea: Luas minimum kontur yang akan dipertimbangkan.
        filter: Jumlah sudut yang diharapkan untuk memfilter kontur (misal: 4 untuk persegi/persegi panjang).
                Jika 0, semua kontur di atas minArea akan dipertimbangkan.
        cThr: Batas threshold untuk Canny Edge Detector [threshold1, threshold2].
        draw: Apakah akan menggambar kontur pada salinan gambar untuk debugging.

    Returns:
        Tuple: (Gambar dengan kontur digambar, Daftar kontur yang ditemukan)
        Setiap kontur dalam daftar adalah tuple: (area, perimeter, kontur_array, bounding_box)
    """