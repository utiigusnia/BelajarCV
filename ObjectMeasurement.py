import cv2
import numpy as np
import utlis

###################################
webcam = True

# --- KONFIGURASI KAMERA ---
camera_source = 0 # Sesuaikan ini (0, 1, atau URL IP Webcam/iVCam)
cap = cv2.VideoCapture(camera_source)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Coba 1920
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # Coba 1080
cap.set(cv2.CAP_PROP_BRIGHTNESS, 160)

# --- DIMENSI OBJEK REFERENSI YANG DIKETAHUI (dalam mm) ---
REF_OBJ_WIDTH_MM = 80  # Misalnya lebar kartu kredit
REF_OBJ_HEIGHT_MM = 50 # Misalnya tinggi kartu kredit
###################################

while True:
    if webcam:
        success, img = cap.read()
        if not success:
            print("Gagal membaca frame dari kamera. Pastikan kamera terhubung dan sumber kamera benar.")
            break

    imgDisplay = img.copy() # Gambar untuk tampilan akhir

    # --- Deteksi Objek Referensi di Live Feed ---
    # minArea: Sesuaikan berdasarkan ukuran objek referensi di frame Anda.
    # Jika Anda menggunakan 1920x1080, objek 10000 mungkin terlalu kecil, coba tingkatkan.
    imgContoursRef, contsRef = utlis.getContours(img, minArea=20000, filter=4, cThr=[50, 50], draw=True)

    pixelsPerMm_current = 0.0 # Reset PPM setiap frame

    if len(contsRef) != 0:
        ref_obj_contour = contsRef[0][2]
        x_ref, y_ref, w_ref_pix, h_ref_pix = contsRef[0][3]

        cv2.polylines(imgDisplay, [ref_obj_contour], True, (0, 255, 255), 5)

        if REF_OBJ_WIDTH_MM > 0:
            pixelsPerMm_current = w_ref_pix / REF_OBJ_WIDTH_MM
        else:
            print("Peringatan: REF_OBJ_WIDTH_MM adalah nol, tidak dapat melakukan kalibrasi PPM.")

        # --- Deteksi dan Ukur Objek Lain di Live Feed ---
        # minArea untuk objek yang diukur mungkin juga perlu disesuaikan dengan resolusi baru.
        imgContoursObjects, contsObjects = utlis.getContours(img, minArea=5000, filter=0, cThr=[50, 50], draw=False)

        if len(contsObjects) != 0 and pixelsPerMm_current > 0:
            for obj in contsObjects:
                # Logika untuk menghindari pengukuran objek referensi lagi
                # Ini bisa disempurnakan, tapi ini adalah pendekatan sederhana
                # Jika area objek yang dideteksi sangat dekat dengan area referensi, mungkin dilewati
                # Atau bandingkan bounding box secara langsung
                if not (x_ref == obj[3][0] and y_ref == obj[3][1] and \
                        w_ref_pix == obj[3][2] and h_ref_pix == obj[3][3]):

                    x_obj, y_obj, w_obj_pix, h_obj_pix = obj[3]

                    cv2.rectangle(imgDisplay, (x_obj, y_obj), (x_obj + w_obj_pix, y_obj + h_obj_pix), (0, 255, 0), 2)

                    width_mm = w_obj_pix / pixelsPerMm_current
                    height_mm = h_obj_pix / pixelsPerMm_current

                    width_cm = round(width_mm / 10, 1)
                    height_cm = round(height_mm / 10, 1)

                    cv2.putText(imgDisplay, f'W: {width_cm}cm', (x_obj, y_obj - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 0, 255), 2)
                    cv2.putText(imgDisplay, f'H: {height_cm}cm', (x_obj + w_obj_pix + 10, y_obj + h_obj_pix // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 0, 255), 2)
    else:
        cv2.putText(imgDisplay, "Letakkan Objek Referensi", (50, imgDisplay.shape[0] // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # --- MENAMPILKAN LAYAR KAMERA UTAMA LEBIH BESAR ---
    # Hilangkan cv2.resize atau gunakan skala yang lebih besar (misal 1.0 untuk ukuran asli)
    # imgDisplayResized = cv2.resize(imgDisplay, (0, 0), None, 0.5, 0.5) # Ini akan memperkecil jadi setengah
    cv2.imshow('Live Camera Feed with Measurements', imgDisplay) # Tampilkan imgDisplay secara langsung (ukuran aslinya)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()