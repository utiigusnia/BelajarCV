Real-time Object Measurement with Camera Calibration

Introduction This project provides a real-time object measurement solution using cameras and traditional computer vision techniques (contour detection) enhanced with camera calibration. This calibration is important for correcting lens distortion, ensuring measurement accuracy across frames. Measurement results are displayed in meters (m).

The system works by detecting a reference object with known physical dimensions (e.g. an ID card or other rectangular object) in each frame. A pixels per millimeter ratio (pixels_per_mm) is then calculated from this reference object, and used to convert the pixel dimensions of other detected objects into real-world physical sizes.

Key Features of Camera Calibration: Uses the ChArUco pattern to obtain the camera's intrinsic parameters and distortion coefficients, which enables correction of lens distortion in the video frame. Real-time Measurement: Capable of detecting and measuring object dimensions directly from the camera feed. Dynamic Reference Object: Uses a reference object with known physical dimensions to dynamically determine the measurement scale (pixels to millimeters) in each frame. Output in Meters: Object width and height measurement results are displayed in meters. Pure OpenCV: OpenCV-based implementation with no additional deep learning model training required (such as YOLO).

Struktur Proyek
.
├── utlis.py       # Skrip untuk melakukan kalibrasi kamera

├── Objectmeasurement.py        # Skrip utama untuk pengukuran objek real-time

├── assets/                   # (Opsional) Folder untuk gambar contoh

│   └── charuco_board.png

└── README.md                 # Berkas ini

Persyaratan Sistem
- Python 3.x
- Kamera (webcam atau kamera eksternal)
- Objek referensi dengan dimensi fisik yang diketahui (misalnya kartu ID)
- Lingkungan pengembangan (direkomendasikan VS Code)

Instalasi
Kloning Repositori:

Buat Virtual Environment (Direkomendasikan):


python -m venv venv
# Di Windows:
.\venv\Scripts\activate
# Di macOS/Linux:
source venv/bin/activate
Instal Dependensi:
pip install opencv-python numpy
Penggunaan
Langkah 1: Kalibrasi Kamera
Sebelum melakukan pengukuran, Anda harus mengkalibrasi kamera Anda. Ini akan membuat file calibration_data.npz yang diperlukan oleh aplikasi pengukuran.

Langkah 2: Pengukuran Objek Real-time
Setelah kalibrasi berhasil, Anda dapat menjalankan aplikasi pengukuran.

Siapkan Objek Referensi:

Gunakan objek persegi panjang (misalnya kartu ID, kartu kredit, atau benda lain) yang dimensi lebar dan tingginya Anda ketahui secara akurat dalam milimeter.
Edit measurement_app.py: Ubah nilai REF_OBJ_WIDTH_MM dan REF_OBJ_HEIGHT_MM pada skrip agar sesuai dengan dimensi objek referensi Anda.
Contoh untuk kartu ID standar:
Python

REF_OBJ_WIDTH_MM = 85.60  # Lebar kartu ID standar (dalam mm)
REF_OBJ_HEIGHT_MM = 53.98 # Tinggi kartu ID standar (dalam mm)
Jalankan Skrip Pengukuran:

Jalankan skrip:
python measurement_app.py
Sebuah jendela kamera akan muncul. Pastikan objek referensi Anda terlihat jelas di kamera. Aplikasi akan mendeteksi objek referensi, menghitung rasio piksel per mm, dan kemudian mengukur objek lain yang terdeteksi.
Tekan 'q' untuk keluar dari aplikasi.

Cara Kerja Pengukuran
Undistorsi Gambar: Setiap frame dari kamera pertama-tama di-undistorsi menggunakan camera_matrix dan dist_coeffs yang diperoleh dari kalibrasi. Ini menghilangkan efek "melengkung" dari lensa.
Deteksi Kontur: Gambar yang sudah ter-undistorsi kemudian diproses (grayscale, blur, Canny edge detection) untuk menemukan kontur objek.
Identifikasi Objek Referensi: Skrip mencari kontur persegi panjang yang rasio aspek dan ukurannya paling mendekati objek referensi yang telah Anda tentukan dimensinya.
Penentuan Skala (Piksel ke Milimeter): Setelah objek referensi terdeteksi, rasio pixels_per_mm dihitung dengan membagi dimensi piksel objek referensi dengan dimensi fisik milimeternya. Rasio ini bersifat dinamis untuk setiap frame karena jarak objek ke kamera dapat bervariasi.
Pengukuran Objek Lain: Kontur persegi panjang lain yang terdeteksi (selain objek referensi) kemudian diukur. Dimensi pikselnya dibagi dengan pixels_per_mm untuk mendapatkan ukuran dalam milimeter.
Konversi ke Meter: Hasil dalam milimeter kemudian dibagi dengan 1000 untuk ditampilkan dalam meter.
Batasan dan Peningkatan Potensial
Asumsi Planar: Akurasi terbaik dicapai ketika objek referensi dan objek yang diukur berada pada bidang yang relatif datar dan sejajar dengan bidang gambar kamera. Objek yang jauh atau sangat miring akan memiliki akurasi yang menurun.
Deteksi Kontur Sederhana: Metode deteksi kontur sederhana mungkin kesulitan dalam lingkungan yang kompleks, dengan pencahayaan yang buruk, atau jika ada banyak objek serupa yang bisa membingungkan.
Robustness: Identifikasi objek referensi dan objek yang akan diukur saat ini bergantung pada rasio aspek dan area. Ini bisa ditingkatkan dengan menggunakan teknik segmentasi atau deteksi objek berbasis deep learning (seperti YOLO) setelah proses undistorsi.
Kalibrasi Offline: Kalibrasi kamera dilakukan secara offline. Untuk skenario di mana kamera bisa bergerak secara signifikan, sistem yang memantau pose kamera secara real-time (misalnya dengan pelacakan marker ArUco) dapat meningkatkan akurasi.
