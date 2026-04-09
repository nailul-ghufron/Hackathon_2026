# **MATA RAKYAT** **Machine Assisted Transaction Auditor untuk Realtime Analisis Keuangan** **yang Akuntabel & Transparan**

**A.​ Latar Belakang & Problem Statement**

Pemerintah Indonesia membelanjakan ratusan triliun rupiah per tahun, namun celah
korupsi pengadaan barang dan jasa terus dimanfaatkan melalui berbagai modus seperti
mark-up harga, pemecahan proyek (split transaction), dan persekongkolan vendor (vendor
collusion). Dengan volume melebihi 4 juta paket pengadaan yang diproses setiap
tahunnya di seluruh Indonesia, mustahil bagi auditor manusia untuk memeriksa transaksi
tersebut secara menyeluruh. Terbukti, kerugian negara akibat korupsi mencapai Rp28,4
triliun pada tahun 2023, dan 78,8% kasus korupsi yang ditangani KPK melibatkan sektor
pengadaan. Di sisi lain, BPK menemukan 9.116 permasalahan senilai Rp18,76 triliun
hanya dalam satu semester, padahal kapasitas audit manual BPKP hanya mampu
mencakup sekitar 3,2% transaksi per tahun.


Saat ini, Indonesia sedang dalam momentum keterbukaan data pemerintah. Jika
infrastruktur data yang sudah ada iniii tidak segera dimanfaatkan dengan membangun
sistem _intelligence layer_ untuk deteksi otomatis, anggaran layanan dasar akan terus bocor.
Ketiadaan sistem iniii merugikan masyarakat umum serta pelaku UMKM jujur yang kalah
tender karena bersaing dengan vendor berkoneksi. Lebih jauh lagi, tanpa penyelesaian
masalah iniii, potensi besar _open data_ pemerintah menjadi sia-sia dan kita gagal
mewujudkan kedaulatan digital dalam tata kelola keuangan yang akuntabel.


**B.​** **SOLUSI YANG DIUSULKAN DAN MODEL AI**
1)​ Deskripsi Solusi:

MATA RAKYAT adalah sistem kecerdasan buatan berbasis _Explainable Anomaly_
_Detection_ yang secara otomatis memindai, menganalisis, dan menandai transaksi
anggaran publik yang mencurigakan secara _real-time_ . Berbeda dengan sistem pasif
_existing_ yang hanya menampilkan visualisasi statistik, MATA RAKYAT tidak hanya
mendeteksi anomali, tetapi juga mampu menjelaskan mengapa transaksi tersebut anomali
dalam bahasa yang dipahami masyarakat awam, bukan hanya kalangan teknis. Sistem iniii
beroperasi secara mandiri ( _self-hosted_ ) untuk menjaga kedaulatan dan keamanan data.
2)​ Output Sistem:

Luaran yang dihasilkan meliputi: (1) _Anomaly Risk Score_ (0-100) untuk setiap transaksi
pengadaan; (2) Penjelasan Bahasa Alami (misalnya: "Harga satuan 3,2x di atas median
pasar, vendor baru terdaftar 3 hari sebelum tender"); (3) _Pattern Alert Dashboard_ untuk
visualisasi kejanggalan; (4) _Vendor Network Graph_ untuk memetakan jaringan relasi antar
vendor mencurigakan ; dan (5) Laporan PDF otomatis berisi ringkasan temuan untuk
didistribusikan ke aparat pengawas.
3)​ Pendekatan Teknologi:

Sistem iniii masuk dalam Kategori _Data Prediction_ dengan _task Anomaly Detection_
(kombinasi _Unsupervised_ dan _Semi-supervised_ ). Arsitektur pemodelan dibangun secara
berlapis:


●​ **Layer 1 - Statistical Baseline:** Menggunakan algoritma _Isolation Forest_ dan _Local_
_Outlier Factor_ untuk mendeteksi anomali berbasis distribusi data historis.
●​ **Layer 2 - Deep Anomaly Detection:** Mengimplementasikan _Autoencoder Neural_
_Network_ untuk menangkap pola anomali non-linear kompleks yang luput dari
pendekatan statistik.
●​ **Layer 3 - Explainability Engine:** Menggunakan _library_ SHAP ( _SHapley Additive_
_exPlanations_ ) dan LIME untuk menghitung kontribusi setiap fitur terhadap skor
anomali, sehingga memenuhi kriteria _White-box AI_ .
●​ **Layer 4 - Natural Language Generator:** Menggunakan _Template-based_ NLG dan
_Rule Engine_ untuk mengubah _output_ matematis menjadi penjelasan teks Bahasa
Indonesia.

**C.​ DATA**
1)​ Sumber Data:

Data dihimpun melalui web scraping dan API resmi publik. Sumber dataset mencakup:
Data pengadaan nasional dari LKPP/SPSE (~4 juta paket/tahun); APBD daerah dari DJPK
Kemenkeu; Harga referensi dari e-katalog LKPP (~2 juta item); Data perusahaan aktif dari
AHU Kemenkumham (~4 juta entitas) ; serta putusan korupsi inkrah dari Direktori
Mahkamah Agung (~8.000 kasus) sebagai ground truth. Untuk tahap prototype, data
difokuskan pada 3 provinsi pilot (DKI Jakarta, Jawa Timur, Sulawesi Selatan) dengan
estimasi 500.000 transaksi.


2)​ Persiapan & Pembagian Data:

●​ **Handling Missing Values & Outliers:** Nilai harga satuan yang kosong diimputasi
menggunakan nilai median kategori serupa dari e-katalog. Data profil vendor yang
tidak lengkap dikonversi menjadi fitur penanda spesifik (incomplete_vendor_profile =
1) karena hal tersebut merupakan sinyal kuat anomali. Tanggal yang tidak valid
di- _drop_ .
●​ **Handling Imbalance:** Mengingat distribusi positif (kasus korupsi) diperkirakan hanya
~1-3%, sistem menggunakan teknik SMOTE pada lapisan validasi. _Threshold tuning_
dioptimalkan untuk mengejar _recall_ tinggi (meminimalkan _False Negative_ ).
●​ **Pembagian Data:** Dataset dibagi secara sekuensial temporal menjadi 70% _Training_
_Data_ (transaksi 2019-2022), 15% _Validation Data_ (transaksi 2023), dan 15% _Testing_
_Data_ (transaksi 2024 _unseen_ ).


