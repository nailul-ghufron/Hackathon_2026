# Product Requirements Document (PRD)
# MATA RAKYAT — Machine Assisted Transaction Auditor untuk Realtime Analisis Keuangan yang Akuntabel & Transparan

**Tim:** Qwerty
**Hackathon:** Hackathon 2026 — Track Data Prediction (Anomaly Detection)
**Versi PRD:** 1.0
**Tanggal:** 2026-04-09
**Status:** Draft

---

## Daftar Isi

1. [Ringkasan Eksekutif](#1-ringkasan-eksekutif)
2. [Latar Belakang & Problem Statement](#2-latar-belakang--problem-statement)
3. [Tujuan & Sasaran Produk](#3-tujuan--sasaran-produk)
4. [Ruang Lingkup Produk](#4-ruang-lingkup-produk)
5. [Arsitektur Sistem & Model AI](#5-arsitektur-sistem--model-ai)
6. [Spesifikasi Data](#6-spesifikasi-data)
7. [Persyaratan Fungsional](#7-persyaratan-fungsional)
8. [Persyaratan Non-Fungsional](#8-persyaratan-non-fungsional)
9. [Kepatuhan Sealed Constraints Hackathon 2026](#9-kepatuhan-sealed-constraints-hackathon-2026)
10. [Metrik Keberhasilan](#10-metrik-keberhasilan)
11. [Risiko & Mitigasi](#11-risiko--mitigasi)
12. [Glosarium](#12-glosarium)

---

## 1. Ringkasan Eksekutif

**MATA RAKYAT** adalah sistem kecerdasan buatan berbasis *Explainable Anomaly Detection* yang dirancang untuk memindai, menganalisis, dan menandai transaksi anggaran publik yang mencurigakan secara *real-time*. Sistem ini menjawab kesenjangan kritis antara volume pengadaan publik (>4 juta paket/tahun) dan kapasitas audit manual yang hanya mampu menjangkau ~3,2% transaksi per tahun.

Keunggulan utama MATA RAKYAT terletak pada kemampuannya memberikan **penjelasan berbahasa Indonesia yang mudah dipahami** atas setiap temuan anomali — bukan sekadar angka probabilitas — sehingga dapat dimanfaatkan tidak hanya oleh auditor profesional tetapi juga oleh masyarakat umum dan jurnalis investigatif.

Sistem beroperasi secara **self-hosted (offline/localhost)**, menjamin kedaulatan dan keamanan data tanpa ketergantungan pada API cloud eksternal.

---

## 2. Latar Belakang & Problem Statement

### 2.1 Skala Masalah

| Indikator | Data |
|---|---|
| Volume paket pengadaan per tahun | >4 juta paket |
| Kerugian negara akibat korupsi (2023) | Rp 28,4 Triliun |
| Kasus korupsi KPK yang melibatkan pengadaan | 78,8% |
| Permasalahan yang ditemukan BPK (1 semester) | 9.116 kasus senilai Rp 18,76 Triliun |
| Cakupan audit manual BPKP per tahun | ~3,2% transaksi |

### 2.2 Modus Korupsi yang Umum Terjadi

- **Mark-up harga:** Harga pengadaan jauh melebihi harga pasar yang wajar.
- **Split transaction (pemecahan proyek):** Proyek besar dipecah menjadi paket-paket kecil untuk menghindari ambang batas review.
- **Vendor collusion (persekongkolan vendor):** Vendor-vendor yang saling terhubung bergiliran memenangkan tender.

### 2.3 Peluang yang Belum Dimanfaatkan

Indonesia sedang dalam momentum **keterbukaan data pemerintah** dengan berbagai sumber data publik yang telah tersedia (LKPP/SPSE, DJPK Kemenkeu, AHU Kemenkumham, e-katalog LKPP). Tanpa adanya *intelligence layer* yang mengolah data tersebut secara otomatis, potensi besar *open data* pemerintah menjadi sia-sia dan anggaran layanan dasar terus bocor.

### 2.4 Dampak pada Pemangku Kepentingan

- **Masyarakat umum:** Kehilangan akses layanan publik berkualitas akibat kebocoran anggaran.
- **UMKM jujur:** Kalah tender karena bersaing dengan vendor berkoneksi secara tidak adil.
- **Auditor & BPK/BPKP/KPK:** Kewalahan dengan volume pemeriksaan yang jauh melampaui kapasitas.

---

## 3. Tujuan & Sasaran Produk

### 3.1 Tujuan Utama

Membangun prototipe sistem AI yang mampu **mendeteksi anomali transaksi pengadaan publik secara otomatis** dengan tingkat akurasi tinggi sekaligus **menjelaskan temuan** dalam bahasa yang dapat dipahami oleh pemangku kepentingan non-teknis.

### 3.2 Sasaran Terukur (OKR)

| Objektif | Key Result |
|---|---|
| Deteksi anomali akurat | Recall >= 80% pada dataset uji (meminimalkan False Negative) |
| Kecepatan inferensi memadai | Waktu inferensi per transaksi <= 3 detik pada CPU standar (Intel Core i5 Gen 8 / setara) |
| Explainability efektif | Setiap prediksi menghasilkan penjelasan dengan >= 3 variabel teratas beserta arah pengaruhnya |
| Kemandirian sistem | 100% inferensi berjalan localhost, tidak ada data yang dikirim ke server eksternal |
| Ukuran model efisien | Total bobot model <= 50 MB (file .pt / .h5 / .onnx) |

---

## 4. Ruang Lingkup Produk

### 4.1 Dalam Ruang Lingkup (In Scope)

- **Anomaly Detection Engine:** Deteksi transaksi mencurigakan menggunakan pendekatan berlapis.
- **Explainability Module:** Penjelasan fitur dominan menggunakan SHAP dan/atau LIME.
- **Natural Language Generator (NLG):** Konversi output matematis menjadi teks Bahasa Indonesia yang mudah dipahami.
- **Pattern Alert Dashboard:** Visualisasi anomali dan tren mencurigakan.
- **Vendor Network Graph:** Pemetaan jaringan relasi antar vendor yang terindikasi berkolusi.
- **Laporan PDF Otomatis:** Ringkasan temuan untuk distribusi ke aparat pengawas.
- **Anomaly Risk Score:** Skor risiko 0-100 per transaksi pengadaan.
- **Cakupan Pilot:** 3 provinsi (DKI Jakarta, Jawa Timur, Sulawesi Selatan) dengan estimasi 500.000 transaksi untuk tahap prototipe.

### 4.2 Di Luar Ruang Lingkup (Out of Scope)

- Integrasi real-time langsung ke sistem SPSE/LKPP produksi (fase berikutnya).
- Tindak lanjut hukum atau pelaporan resmi ke aparat penegak hukum secara otomatis.
- Penggunaan API inferensi cloud (OpenAI, Google AI, AWS, Azure AI, Hugging Face Inference API, dll.).
- Sistem manajemen pengguna multi-tenant skala enterprise.

---

## 5. Arsitektur Sistem & Model AI

Sistem MATA RAKYAT menggunakan pendekatan **Data Prediction — Anomaly Detection** dengan kombinasi metode *Unsupervised* dan *Semi-supervised*. Arsitektur dibangun secara berlapis:

```
+-------------------------------------------------------------+
|               INPUT: Data Transaksi Pengadaan               |
+---------------------------+---------------------------------+
                            |
                            v
+-------------------------------------------------------------+
|  LAYER 1 -- Statistical Baseline                            |
|  * Isolation Forest                                         |
|  * Local Outlier Factor (LOF)                               |
|  Deteksi anomali berbasis distribusi data historis          |
+---------------------------+---------------------------------+
                            |
                            v
+-------------------------------------------------------------+
|  LAYER 2 -- Deep Anomaly Detection                          |
|  * Autoencoder Neural Network                               |
|  Menangkap pola anomali non-linear kompleks yang luput      |
|  dari pendekatan statistik konvensional                     |
+---------------------------+---------------------------------+
                            |
                            v
+-------------------------------------------------------------+
|  LAYER 3 -- Explainability Engine (White-box AI)            |
|  * SHAP (SHapley Additive exPlanations)                     |
|  * LIME                                                     |
|  Menghitung kontribusi setiap fitur terhadap skor anomali   |
|  -> Output: >= 3 variabel teratas + arah pengaruh (+/-)     |
+---------------------------+---------------------------------+
                            |
                            v
+-------------------------------------------------------------+
|  LAYER 4 -- Natural Language Generator                      |
|  * Template-based NLG                                       |
|  * Rule Engine                                              |
|  Mengkonversi output matematis ke penjelasan Bahasa         |
|  Indonesia yang mudah dipahami masyarakat awam              |
+---------------------------+---------------------------------+
                            |
                            v
+-------------------------------------------------------------+
|  OUTPUT                                                     |
|  * Anomaly Risk Score (0-100)                               |
|  * Penjelasan Bahasa Alami                                  |
|  * Pattern Alert Dashboard                                  |
|  * Vendor Network Graph                                     |
|  * Laporan PDF Otomatis                                     |
+-------------------------------------------------------------+
```

### 5.1 Detail Setiap Layer

#### Layer 1 — Statistical Baseline
- **Algoritma:** Isolation Forest, Local Outlier Factor (LOF)
- **Fungsi:** Mendeteksi anomali berbasis distribusi data historis
- **Keunggulan:** Ringan dan cepat, cocok sebagai filter awal

#### Layer 2 — Deep Anomaly Detection
- **Algoritma:** Autoencoder Neural Network
- **Fungsi:** Menangkap pola anomali non-linear kompleks
- **Keunggulan:** Mampu menemukan pola tersembunyi yang tidak terdeteksi Layer 1

#### Layer 3 — Explainability Engine
- **Library:** SHAP dan LIME
- **Fungsi:** Menghitung kontribusi fitur terhadap skor anomali
- **Output Wajib:** Minimal 3 variabel teratas beserta arah pengaruh (positif/negatif)
- **Compliance:** Memenuhi syarat *White-box AI* dan constraint explainability mandatory

#### Layer 4 — Natural Language Generator
- **Pendekatan:** Template-based NLG + Rule Engine (berjalan lokal, tanpa LLM eksternal)
- **Fungsi:** Mengubah output matematis menjadi teks Bahasa Indonesia
- **Contoh Output:** *"Harga satuan 3,2x di atas median pasar, vendor baru terdaftar 3 hari sebelum tender"*
- **Kepatuhan Constraint:** Tidak menggunakan Language Model >4B parameter; seluruh NLG berjalan localhost

---

## 6. Spesifikasi Data

### 6.1 Sumber Data

| Sumber | Keterangan | Estimasi Volume |
|---|---|---|
| LKPP/SPSE | Data pengadaan nasional | ~4 juta paket/tahun |
| DJPK Kemenkeu | APBD daerah | Seluruh provinsi |
| e-katalog LKPP | Harga referensi barang/jasa | ~2 juta item |
| AHU Kemenkumham | Data perusahaan aktif | ~4 juta entitas |
| Direktori Mahkamah Agung | Putusan korupsi inkrah (ground truth) | ~8.000 kasus |

**Metode pengumpulan:** Web scraping terstruktur dan konsumsi API resmi publik.

### 6.2 Scope Prototipe

- **Cakupan wilayah:** 3 provinsi pilot — DKI Jakarta, Jawa Timur, Sulawesi Selatan
- **Estimasi transaksi:** 500.000 transaksi untuk tahap prototipe

### 6.3 Pembagian Dataset (Temporal Split)

```
Dataset Temporal:
|
+-- 70% Training Data   ->  Transaksi 2019-2022
+-- 15% Validation Data ->  Transaksi 2023
+-- 15% Testing Data    ->  Transaksi 2024 (unseen)
```

### 6.4 Penanganan Kualitas Data

| Isu Data | Strategi Penanganan |
|---|---|
| Missing value harga satuan | Imputasi menggunakan nilai **median** kategori serupa dari e-katalog LKPP |
| Profil vendor tidak lengkap | Dikonversi menjadi fitur `incomplete_vendor_profile = 1` (sinyal anomali kuat) |
| Tanggal tidak valid | Baris terkait di-*drop* |
| Class imbalance (~1-3% positif) | Teknik **SMOTE** pada lapisan validasi + *threshold tuning* untuk mengejar *recall* tinggi |

---

## 7. Persyaratan Fungsional

### 7.1 FR-01: Anomaly Scoring

- **Deskripsi:** Sistem wajib menghasilkan *Anomaly Risk Score* bernilai integer 0-100 untuk setiap transaksi pengadaan yang dianalisis.
- **Kriteria Penerimaan:**
  - Skor 0 = tidak mencurigakan; skor 100 = sangat mencurigakan.
  - Skor dihasilkan dari pipeline berlapis (Layer 1 + Layer 2).
  - Setiap skor yang dihasilkan disertai penjelasan dari Layer 3 & 4.

### 7.2 FR-02: Explainability Output

- **Deskripsi:** Untuk setiap prediksi anomali, sistem wajib menghasilkan penjelasan yang menyebutkan minimal 3 variabel teratas yang memengaruhi hasil prediksi beserta arah pengaruhnya (positif/negatif).
- **Kriteria Penerimaan:**
  - Implementasi menggunakan SHAP dan/atau LIME.
  - Output dapat dibaca manusia (*human-readable explanation*).
  - Format output JSON terstruktur untuk integrasi ke dashboard.

### 7.3 FR-03: Natural Language Explanation

- **Deskripsi:** Sistem wajib mengkonversi output matematis Layer 3 menjadi teks penjelasan Bahasa Indonesia yang dapat dipahami oleh masyarakat awam.
- **Kriteria Penerimaan:**
  - Penjelasan dihasilkan oleh Template-based NLG + Rule Engine yang berjalan lokal.
  - Tidak ada ketergantungan pada API LLM eksternal.
  - Teks mencakup fakta konkret (misalnya perbandingan harga, profil vendor, kronologis tanggal terkait).

### 7.4 FR-04: Pattern Alert Dashboard

- **Deskripsi:** Sistem menyediakan antarmuka visualisasi untuk menampilkan pola anomali dan tren mencurigakan.
- **Kriteria Penerimaan:**
  - Menampilkan daftar transaksi dengan skor risiko tertinggi.
  - Filter berdasarkan provinsi, SKPD, rentang waktu, dan kategori pengadaan.
  - Grafik tren anomali per periode.

### 7.5 FR-05: Vendor Network Graph

- **Deskripsi:** Sistem memetakan jaringan relasi antar vendor yang terindikasi berkolusi.
- **Kriteria Penerimaan:**
  - Visualisasi graf dengan node = vendor, edge = indikasi relasi.
  - Identifikasi kluster vendor mencurigakan.
  - Dapat di-drill down untuk melihat daftar transaksi terkait setiap vendor.

### 7.6 FR-06: Laporan PDF Otomatis

- **Deskripsi:** Sistem menghasilkan laporan PDF berisi ringkasan temuan anomali secara otomatis.
- **Kriteria Penerimaan:**
  - PDF berisi: executive summary, daftar transaksi berisiko tinggi, penjelasan per temuan, dan rekomendasi tindak lanjut.
  - Laporan dapat di-*generate* secara on-demand maupun terjadwal.

### 7.7 FR-07: Offline Inference

- **Deskripsi:** Seluruh pipeline inferensi wajib berjalan secara lokal (localhost/offline).
- **Kriteria Penerimaan:**
  - Tidak ada request ke API cloud atau server eksternal selama proses inferensi.
  - Sistem tetap berfungsi penuh tanpa koneksi internet.

---

## 8. Persyaratan Non-Fungsional

### 8.1 NFR-01: Kecepatan Inferensi

- Waktu inferensi per satu sampel input (single inference) **TIDAK BOLEH melebihi 3 detik** pada mesin CPU standar minimum Intel Core i5 Generasi 8 atau setara.
- Pengukuran dilakukan pada kondisi CPU-only, tanpa akselerasi GPU.

### 8.2 NFR-02: Ukuran Model

- Total bobot model final (file `.pt` / `.h5` / `.onnx`) **TIDAK BOLEH melebihi 50 MB**.
- Folder `train_data` dan `test_data` disimpan secara terpisah dari file bobot model.

### 8.3 NFR-03: Kompatibilitas Platform

- Model wajib dapat berjalan di lingkungan **CPU-only**.
- Model boleh memanfaatkan GPU localhost saat demo, namun validasi constraint kecepatan dilakukan pada kondisi CPU.

### 8.4 NFR-04: Bahasa Pemrograman

- **Python** adalah bahasa utama yang digunakan untuk seluruh pipeline AI.
- Komponen lain (dashboard, laporan PDF) boleh menggunakan bahasa/framework berbeda dengan dokumentasi jelas.

### 8.5 NFR-05: Reproducibility

- Pipeline training dan inferensi wajib bersifat *reproducible* (fixed random seed, versi dependensi terdokumentasi).
- File model, `train_data`, dan `test_data` disimpan secara terpisah.

### 8.6 NFR-06: Privasi & Keamanan Data

- Tidak ada data yang dikirim ke server atau API eksternal dalam pipeline utama.
- Data sensitif yang muncul dalam proses analisis diperlakukan sesuai prinsip kerahasiaan.

### 8.7 NFR-07: Skalabilitas Prototipe

- Prototipe wajib mampu memproses batch 500.000 transaksi dalam waktu yang wajar untuk keperluan demonstrasi.

---

## 9. Kepatuhan Sealed Constraints Hackathon 2026

Bagian ini secara eksplisit mendokumentasikan bagaimana MATA RAKYAT memenuhi setiap poin *Sealed Constraint* yang berlaku untuk track **Data Prediction (Anomaly Detection / Explainable AI)**.

> **PENTING:** Seluruh constraint bersifat **mandatory (wajib)**, bukan opsional. Kegagalan memenuhi satu constraint saja berdampak fatal pada penilaian.

### C-1: Explainability Wajib ✅

| Constraint | Pemenuhan |
|---|---|
| Model WAJIB menyertakan mekanisme explainability | ✅ Layer 3 mengimplementasikan SHAP dan LIME sebagai inti Explainability Engine |
| Implementasi minimal: SHAP, LIME, feature importance plot, atau metode interpretabilitas ilmiah lain | ✅ SHAP (SHapley Additive exPlanations) + LIME diimplementasikan |

**Detail Implementasi:**
- SHAP digunakan untuk menghitung Shapley values — kontribusi marginal setiap fitur terhadap skor anomali.
- LIME digunakan sebagai validasi silang explainability pada sampel lokal.
- Kedua library ini berjalan sepenuhnya secara lokal tanpa dependensi cloud.

### C-2: Output Penjelasan Human-Readable ✅

| Constraint | Pemenuhan |
|---|---|
| Sistem wajib menghasilkan output penjelasan yang dapat dibaca manusia untuk setiap prediksi | ✅ Layer 4 (NLG) menghasilkan teks Bahasa Indonesia |
| Penjelasan minimal menyebutkan 3 variabel teratas beserta arah pengaruhnya (positif/negatif) | ✅ Output SHAP/LIME dikonversi ke format narasi dengan >= 3 variabel + arah pengaruh |

**Contoh Output Penjelasan:**
```
"Transaksi #TRX-2024-00812 memiliki skor risiko 87/100.
Faktor utama yang memicu anomali:
  (+) Harga satuan 3,2x di atas median pasar untuk kategori yang sama [+42 poin]
  (+) Vendor terdaftar hanya 3 hari sebelum tender dibuka [+28 poin]
  (+) Jumlah peserta tender hanya 1 (tender tidak kompetitif) [+17 poin]"
```

### C-3: Anti-Black Box ✅

| Constraint | Pemenuhan |
|---|---|
| Penggunaan model opaque (black box) tanpa lapisan explainability tidak memenuhi syarat | ✅ Seluruh model dilengkapi lapisan explainability (Layer 3) |

**Detail Implementasi:**
- **Layer 1 (Isolation Forest, LOF):** Secara inheren interpretable melalui SHAP TreeExplainer.
- **Layer 2 (Autoencoder):** Dilengkapi SHAP DeepExplainer / KernelExplainer untuk explainability.
- Tidak ada model yang digunakan dalam pipeline inferensi tanpa mekanisme penjelasan.

### C-4: Larangan Cloud Inference ✅

| Constraint | Pemenuhan |
|---|---|
| Dilarang menggunakan API inferensi cloud sebagai komponen inti model | ✅ Seluruh komponen berjalan localhost |

**Detail Implementasi:**
- Layer 1 & 2: scikit-learn + PyTorch/TensorFlow — berjalan lokal.
- Layer 3: SHAP + LIME — library Python lokal.
- Layer 4: Template-based NLG + Rule Engine — logika Python murni, tanpa API LLM eksternal.
- **Tidak ada dependency** pada OpenAI, Google AI, AWS, Azure AI, atau Hugging Face Inference API.

### C-5: Kecepatan Inferensi <= 3 Detik pada CPU ✅

| Constraint | Pemenuhan |
|---|---|
| Waktu inferensi per satu sampel TIDAK BOLEH melebihi 3 detik pada CPU standar | ✅ Dioptimasi melalui pemilihan model ringan + kuantisasi |

**Strategi Optimasi:**
- Layer 1 (Isolation Forest, LOF): inferensi sub-100ms.
- Layer 2 (Autoencoder): arsitektur compact (< 5 layer, bottleneck kecil) untuk inferensi cepat.
- Layer 3 (SHAP): menggunakan `shap.TreeExplainer` (fast) untuk Layer 1 dan sampling terbatas untuk Layer 2.
- Layer 4 (NLG): template lookup — O(1), tidak menambah latensi signifikan.
- **Target total pipeline:** < 2 detik pada CPU i5 Gen 8.

### C-6: Ukuran Model <= 50 MB ✅

| Constraint | Pemenuhan |
|---|---|
| Bobot model final TIDAK BOLEH melebihi 50 MB | ✅ Dikendalikan melalui arsitektur compact |

**Strategi Pengendalian Ukuran:**
- Isolation Forest: simpan model dengan `joblib` dengan kompresi = estimasi < 5 MB.
- Autoencoder: arsitektur minimal (encoder-decoder 3 layer), simpan dalam format `.h5` / `.pt` = estimasi < 15 MB.
- SHAP background dataset: subsample 100-500 data referensi = estimasi < 5 MB.
- **Total estimasi:** < 25 MB (jauh di bawah batas 50 MB).

### C-7: Reproducibility & Struktur Direktori ✅

| Constraint | Pemenuhan |
|---|---|
| File bobot model, folder train_data, dan folder test_data disimpan secara terpisah | ✅ Struktur direktori didesain sesuai ketentuan |

**Struktur Direktori:**
```
mata_rakyat/
+-- models/              <- File bobot (.pt/.h5/.onnx)
|   +-- isolation_forest.joblib
|   +-- lof_model.joblib
|   +-- autoencoder.pt
+-- train_data/          <- Dataset training (2019-2022)
+-- test_data/           <- Dataset testing (2024, unseen)
+-- inference.py         <- Pipeline inferensi utama
+-- explainability.py    <- Modul SHAP + LIME
+-- nlg.py               <- Natural Language Generator
+-- dashboard/           <- Komponen visualisasi
```

### C-8: Bahasa Kode Python ✅

| Constraint | Pemenuhan |
|---|---|
| Python adalah bahasa utama yang direkomendasikan | ✅ Seluruh pipeline AI dan model dibangun dengan Python |

**Stack Teknologi:**

| Komponen | Teknologi |
|---|---|
| Anomaly Detection (Layer 1) | Python — scikit-learn (Isolation Forest, LOF) |
| Anomaly Detection (Layer 2) | Python — PyTorch / TensorFlow (Autoencoder) |
| Explainability (Layer 3) | Python — SHAP, LIME |
| NLG (Layer 4) | Python — Template Engine (Jinja2 / custom) |
| Dashboard | Python — Streamlit / Dash, atau HTML+JS |
| Laporan PDF | Python — ReportLab / WeasyPrint |

---

## 10. Metrik Keberhasilan

### 10.1 Metrik Model AI

| Metrik | Target | Justifikasi |
|---|---|---|
| **Recall** | >= 80% | Prioritas utama: meminimalkan False Negative (kasus korupsi yang terlewat) |
| **Precision** | >= 50% | Menjaga jumlah False Alarm pada level yang dapat ditangani auditor |
| **F1-Score** | >= 60% | Keseimbangan Precision-Recall |
| **AUC-ROC** | >= 0.85 | Kemampuan diskriminasi model secara keseluruhan |
| **Waktu Inferensi (CPU)** | <= 3 detik/sampel | Sesuai constraint mandatory |
| **Ukuran Model** | <= 50 MB | Sesuai constraint mandatory |

### 10.2 Metrik Kualitas Explainability

| Metrik | Target |
|---|---|
| Setiap prediksi anomali disertai penjelasan | 100% |
| Penjelasan mencakup >= 3 variabel + arah pengaruh | 100% |
| Konsistensi penjelasan (SHAP vs manual review) | >= 90% |

### 10.3 Metrik Sistem

| Metrik | Target |
|---|---|
| Uptime sistem (saat demo) | 99%+ |
| Pipeline berjalan offline penuh | 100% |
| Reproducibility (hasil sama pada seed yang sama) | 100% |

---

## 11. Risiko & Mitigasi

| Risiko | Kemungkinan | Dampak | Mitigasi |
|---|---|---|---|
| Class imbalance ekstrem (~1-3% positif) | Tinggi | Tinggi | SMOTE + threshold tuning; optimasi recall |
| Data pengadaan mengandung banyak missing value | Tinggi | Sedang | Strategi imputasi dan feature flagging yang solid |
| Waktu inferensi melebihi 3 detik akibat SHAP | Sedang | Tinggi | Gunakan TreeExplainer (cepat) + batasi jumlah background samples |
| Ukuran model membengkak melebihi 50 MB | Rendah | Tinggi | Monitoring ukuran model sejak awal; kompresi joblib |
| Kualitas ground truth dari kasus inkrah terbatas | Sedang | Sedang | Augmentasi dengan hasil audit BPK sebagai label proxy |
| Overfitting pada data 3 provinsi pilot | Sedang | Sedang | Validasi silang temporal; regularisasi model |

---

## 12. Glosarium

| Istilah | Definisi |
|---|---|
| **Anomaly Detection** | Proses identifikasi pola atau data point yang menyimpang signifikan dari perilaku yang diharapkan |
| **Autoencoder** | Arsitektur neural network yang belajar merepresentasikan data dalam dimensi lebih rendah; rekonstruksi error tinggi = anomali |
| **SHAP** | SHapley Additive exPlanations — metode game theory untuk menghitung kontribusi setiap fitur terhadap prediksi model |
| **LIME** | Local Interpretable Model-agnostic Explanations — metode penjelasan lokal yang memperkirakan perilaku model di sekitar satu prediksi |
| **Isolation Forest** | Algoritma anomaly detection berbasis pohon keputusan; anomali lebih mudah "diisolasi" dengan split lebih sedikit |
| **LOF** | Local Outlier Factor — algoritma berbasis kepadatan yang mengidentifikasi titik data dengan kepadatan lokal jauh lebih rendah dari tetangganya |
| **SMOTE** | Synthetic Minority Over-sampling Technique — metode oversampling untuk menangani class imbalance |
| **Self-hosted** | Sistem yang dijalankan sepenuhnya di infrastruktur sendiri tanpa dependensi layanan cloud pihak ketiga |
| **NLG** | Natural Language Generation — proses menghasilkan teks bahasa alami dari data terstruktur |
| **White-box AI** | Model AI yang keputusannya dapat dijelaskan dan dipahami oleh manusia |
| **LKPP** | Lembaga Kebijakan Pengadaan Barang/Jasa Pemerintah |
| **SPSE** | Sistem Pengadaan Secara Elektronik |
| **DJPK** | Direktorat Jenderal Perimbangan Keuangan, Kemendikbud |
| **AHU** | Administrasi Hukum Umum, Kemenkumham |
| **BPK** | Badan Pemeriksa Keuangan |
| **BPKP** | Badan Pengawasan Keuangan dan Pembangunan |
| **KPK** | Komisi Pemberantasan Korupsi |

---

*PRD ini dibuat berdasarkan Proposal Tim Qwerty — MATA RAKYAT dan diselaraskan penuh dengan Sealed Constraints Hackathon 2026. Semua constraint bersifat mandatory dan telah diverifikasi pemenuhannya pada Bab 9 dokumen ini.*
