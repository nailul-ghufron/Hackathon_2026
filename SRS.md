# Software Requirements Specification (SRS)
# MATA RAKYAT — Machine Assisted Transaction Auditor untuk Realtime Analisis Keuangan yang Akuntabel & Transparan

**Tim:** Qwerty
**Hackathon:** Hackathon 2026 — Track Data Prediction (Anomaly Detection)
**Versi SRS:** 1.0
**Referensi PRD:** PRD v1.0 (2026-04-09)
**Tanggal:** 2026-04-09
**Status:** Draft

---

## Daftar Isi

1. [Pendahuluan](#1-pendahuluan)
2. [Deskripsi Umum Sistem](#2-deskripsi-umum-sistem)
3. [Pemangku Kepentingan & Pengguna](#3-pemangku-kepentingan--pengguna)
4. [Arsitektur Komponen Sistem](#4-arsitektur-komponen-sistem)
5. [Spesifikasi Use Case](#5-spesifikasi-use-case)
6. [Spesifikasi Fungsional Detail](#6-spesifikasi-fungsional-detail)
7. [Spesifikasi Data & Skema](#7-spesifikasi-data--skema)
8. [Pipeline Pemrosesan Data (Data Flow)](#8-pipeline-pemrosesan-data-data-flow)
9. [Spesifikasi Model AI](#9-spesifikasi-model-ai)
10. [Spesifikasi Antarmuka Sistem](#10-spesifikasi-antarmuka-sistem)
11. [Spesifikasi Non-Fungsional Teknis](#11-spesifikasi-non-fungsional-teknis)
12. [Spesifikasi Pengujian](#12-spesifikasi-pengujian)
13. [Struktur Direktori & Artefak](#13-struktur-direktori--artefak)
14. [Dependensi & Lingkungan](#14-dependensi--lingkungan)
15. [Batasan Teknis & Asumsi](#15-batasan-teknis--asumsi)
16. [Matriks Keterlacakan Persyaratan](#16-matriks-keterlacakan-persyaratan)

---

## 1. Pendahuluan

### 1.1 Tujuan Dokumen

Dokumen ini merupakan **Software Requirements Specification (SRS)** untuk sistem MATA RAKYAT. SRS ini mendefinisikan secara teknis dan detail seluruh persyaratan perangkat lunak, antarmuka sistem, perilaku komponen, skema data, serta kontrak antar modul yang harus dipenuhi dalam implementasi. Dokumen ini berfungsi sebagai acuan teknis utama bagi tim pengembang dan validator.

### 1.2 Ruang Lingkup

SRS ini mencakup seluruh komponen perangkat lunak sistem MATA RAKYAT yang akan dibangun untuk Hackathon 2026, yaitu:

- Pipeline preprocessing dan feature engineering data pengadaan publik
- Modul Anomaly Detection berlapis (Layer 1 & Layer 2)
- Modul Explainability Engine (Layer 3)
- Modul Natural Language Generator / NLG (Layer 4)
- Antarmuka Dashboard (Pattern Alert & Vendor Network Graph)
- Modul Laporan PDF Otomatis
- Pipeline inferensi terpadu (`inference.py`)

### 1.3 Definisi, Akronim & Singkatan

| Singkatan | Kepanjangan |
|---|---|
| SRS | Software Requirements Specification |
| PRD | Product Requirements Document |
| FR | Functional Requirement |
| NFR | Non-Functional Requirement |
| UC | Use Case |
| ARS | Anomaly Risk Score |
| NLG | Natural Language Generator |
| SHAP | SHapley Additive exPlanations |
| LIME | Local Interpretable Model-agnostic Explanations |
| LOF | Local Outlier Factor |
| IF | Isolation Forest |
| AE | Autoencoder |
| SMOTE | Synthetic Minority Over-sampling Technique |
| CPU | Central Processing Unit |
| GPU | Graphics Processing Unit |
| JSON | JavaScript Object Notation |
| PDF | Portable Document Format |
| API | Application Programming Interface |
| LKPP | Lembaga Kebijakan Pengadaan Barang/Jasa Pemerintah |
| SPSE | Sistem Pengadaan Secara Elektronik |
| KPK | Komisi Pemberantasan Korupsi |
| BPK | Badan Pemeriksa Keuangan |
| BPKP | Badan Pengawasan Keuangan dan Pembangunan |

### 1.4 Referensi Dokumen

| Dokumen | Versi | Keterangan |
|---|---|---|
| PRD MATA RAKYAT | 1.0 | Dokumen persyaratan produk (induk) |
| Hackathon2026_Qwerty_MATA RAKYAT_Proposal.docx | Final | Proposal tim |
| Constraints Hackathon 2026.md | - | Sealed Constraints track Data Prediction |

---

## 2. Deskripsi Umum Sistem

### 2.1 Perspektif Sistem

MATA RAKYAT adalah sistem *standalone* yang beroperasi sepenuhnya secara **offline (localhost)**. Sistem tidak memiliki ketergantungan pada layanan cloud eksternal untuk fungsi inferensi inti. Sistem menerima input berupa data transaksi pengadaan publik (dalam format CSV/JSON atau dari database lokal) dan menghasilkan output berupa skor anomali, penjelasan berbahasa Indonesia, visualisasi, dan laporan PDF.

```
[Sumber Data Publik]         [Sistem MATA RAKYAT — Localhost]        [Output]
  LKPP/SPSE CSV    ------>  +----------------------------------+  -->  Risk Score JSON
  e-katalog CSV    ------>  |  Preprocessing  ->  AI Pipeline  |  -->  NL Explanation
  AHU CSV          ------>  |  Layer 1 + 2 + 3 + 4             |  -->  Dashboard HTML
  Putusan MA CSV   ------>  +----------------------------------+  -->  PDF Report
```

### 2.2 Fungsi Utama Sistem

1. **Ingest & Preprocess:** Membaca, membersihkan, dan mentransformasi data pengadaan mentah.
2. **Feature Engineering:** Menghasilkan fitur statistik, temporal, dan relasional untuk model.
3. **Anomaly Detection:** Menghitung skor anomali berlapis menggunakan IF+LOF+Autoencoder.
4. **Explainability:** Menghasilkan penjelasan berbasis SHAP/LIME untuk setiap prediksi.
5. **NLG:** Mengkonversi penjelasan matematis menjadi teks Bahasa Indonesia.
6. **Visualisasi:** Menampilkan dashboard interaktif dan vendor network graph.
7. **PDF Report:** Menghasilkan laporan PDF ringkasan temuan.

### 2.3 Batasan Sistem

- **Tidak ada koneksi cloud:** Semua proses berjalan di localhost.
- **Bahasa Python:** Pipeline AI wajib Python; komponen UI boleh HTML/JS.
- **Ukuran model <= 50 MB:** Bobot model terkompresi.
- **Inferensi <= 3 detik/sampel:** Pada kondisi CPU-only.
- **Prototipe:** Cakupan 3 provinsi, 500.000 transaksi pilot.

---

## 3. Pemangku Kepentingan & Pengguna

### 3.1 Pemangku Kepentingan

| Peran | Deskripsi | Kepentingan |
|---|---|---|
| Tim Pengembang (Qwerty) | Membangun dan memelihara sistem | Implementasi semua FR & NFR |
| Juri Hackathon | Mengevaluasi sistem | Validasi constraint & akurasi model |
| Auditor / BPK / BPKP | Pengguna target utama | Temuan anomali yang dapat ditindaklanjuti |
| KPK / Aparat Hukum | Pengguna sekunder | Laporan PDF untuk investigasi |
| Masyarakat / Jurnalis | Pengguna tersier | Akses penjelasan yang mudah dipahami |

### 3.2 Profil Pengguna

#### UP-01: Auditor Pemerintah
- **Keahlian teknis:** Menengah — familiar dengan sistem pengadaan, tidak expert AI
- **Kebutuhan utama:** Daftar transaksi berisiko tinggi + penjelasan yang dapat dipertanggungjawabkan
- **Interaksi:** Dashboard + PDF Report

#### UP-02: Analis Data / Investigator
- **Keahlian teknis:** Tinggi — memahami statistik dan data
- **Kebutuhan utama:** Vendor Network Graph, raw score, fitur-fitur penyumbang anomali
- **Interaksi:** Dashboard + output JSON

#### UP-03: Juri Hackathon
- **Keahlian teknis:** Sangat tinggi — AI/ML expert
- **Kebutuhan utama:** Validasi constraint, reproducibility, kecepatan inferensi, explainability
- **Interaksi:** `inference.py` CLI + model files + notebook demo

---

## 4. Arsitektur Komponen Sistem

### 4.1 Diagram Komponen

```
+==============================================================+
|                  SISTEM MATA RAKYAT (Localhost)              |
+==============================================================+
|                                                              |
|  +------------------+     +----------------------------+     |
|  | DATA INGESTION   |     | FEATURE ENGINEERING        |     |
|  | - CSV Reader     | --> | - Price ratio calc         |     |
|  | - JSON Parser    |     | - Temporal features        |     |
|  | - Data Validator |     | - Vendor profile features  |     |
|  +------------------+     | - Graph features           |     |
|                           +------------+---------------+     |
|                                        |                     |
|                           +------------v---------------+     |
|                           |  LAYER 1: Statistical      |     |
|                           |  Baseline                  |     |
|                           |  - Isolation Forest        |     |
|                           |  - Local Outlier Factor    |     |
|                           +------------+---------------+     |
|                                        |                     |
|                           +------------v---------------+     |
|                           |  LAYER 2: Deep Detection   |     |
|                           |  - Autoencoder NN          |     |
|                           |  - Reconstruction Error    |     |
|                           +------------+---------------+     |
|                                        |                     |
|                           +------------v---------------+     |
|                           |  LAYER 3: Explainability   |     |
|                           |  - SHAP Engine             |     |
|                           |  - LIME Engine             |     |
|                           |  - Feature Contribution    |     |
|                           +------------+---------------+     |
|                                        |                     |
|                           +------------v---------------+     |
|                           |  LAYER 4: NLG              |     |
|                           |  - Template Engine         |     |
|                           |  - Rule Engine             |     |
|                           |  - Bahasa Indonesia Text   |     |
|                           +-----+----------+-----------+     |
|                                 |          |                 |
|                    +------------v-+  +-----v------------+    |
|                    |  DASHBOARD   |  |  PDF GENERATOR   |    |
|                    |  - Alert UI  |  |  - ReportLab     |    |
|                    |  - Net Graph |  |  - Summary Table |    |
|                    +--------------+  +------------------+    |
|                                                              |
+==============================================================+
```

### 4.2 Daftar Modul & File

| Modul | File Utama | Tanggung Jawab |
|---|---|---|
| Data Ingestion | `src/ingestion/reader.py` | Baca CSV/JSON dari sumber data |
| Data Validator | `src/ingestion/validator.py` | Validasi skema dan tipe data |
| Preprocessor | `src/preprocessing/cleaner.py` | Imputasi, drop, encoding |
| Feature Engineering | `src/features/engineer.py` | Kalkulasi fitur derivatif |
| Layer 1 — IF | `src/models/isolation_forest.py` | Training & inferensi Isolation Forest |
| Layer 1 — LOF | `src/models/lof.py` | Training & inferensi LOF |
| Layer 2 — AE | `src/models/autoencoder.py` | Definisi, training & inferensi Autoencoder |
| Score Aggregator | `src/models/score_aggregator.py` | Gabungkan skor Layer 1+2 menjadi ARS |
| SHAP Engine | `src/explainability/shap_engine.py` | Komputasi SHAP values |
| LIME Engine | `src/explainability/lime_engine.py` | Komputasi LIME explanations |
| NLG | `src/nlg/generator.py` | Template-based text generation |
| NLG Templates | `src/nlg/templates/` | File template Jinja2 |
| Dashboard | `dashboard/app.py` | Antarmuka Streamlit/Dash |
| Network Graph | `dashboard/network.py` | Vendor graph visualization |
| PDF Generator | `src/report/pdf_generator.py` | Generate laporan PDF |
| Pipeline Inferensi | `inference.py` | Entry point utama (wajib) |
| Pipeline Training | `train.py` | Entry point training model |
| Config | `config/config.yaml` | Konfigurasi global sistem |

---

## 5. Spesifikasi Use Case

### 5.1 Diagram Use Case

```
        +-----------------------------------------------------+
        |                   SISTEM MATA RAKYAT                |
        |                                                      |
        |   +--[UC-01: Jalankan Inferensi Batch]              |
        |   |                                                  |
        |   +--[UC-02: Lihat Dashboard Anomali]               |
        |   |                                                  |
        |   +--[UC-03: Eksplorasi Vendor Network Graph]        |
        |   |                                                  |
        |   +--[UC-04: Generate Laporan PDF]                  |
        |   |                                                  |
        |   +--[UC-05: Latih Ulang Model]                     |
        |   |                                                  |
        |   +--[UC-06: Lihat Detail Transaksi & Penjelasan]   |
        |                                                      |
        +-----------------------------------------------------+
             ^            ^              ^
             |            |              |
        [Auditor]   [Investigator]  [Juri/Developer]
```

### 5.2 UC-01: Jalankan Inferensi Batch

| Atribut | Detail |
|---|---|
| **ID** | UC-01 |
| **Nama** | Jalankan Inferensi Batch |
| **Aktor Utama** | Developer / Juri / Auditor |
| **Prasyarat** | File model sudah tersimpan di `models/`; data input tersedia di format CSV/JSON |
| **Alur Utama** | 1. Pengguna menjalankan `python inference.py --input data/test.csv` |
| | 2. Sistem membaca dan memvalidasi file input |
| | 3. Sistem menjalankan preprocessing & feature engineering |
| | 4. Sistem menghitung ARS via Layer 1 + Layer 2 |
| | 5. Sistem menghitung SHAP values via Layer 3 |
| | 6. Sistem menghasilkan teks penjelasan via Layer 4 (NLG) |
| | 7. Sistem menyimpan output ke `output/results_[timestamp].json` |
| | 8. Sistem menampilkan ringkasan di terminal |
| **Alur Alternatif** | Jika file input tidak valid: sistem menampilkan pesan error dan berhenti |
| **Pasca-kondisi** | File JSON berisi ARS + penjelasan untuk setiap transaksi tersimpan di `output/` |
| **Referensi FR** | FR-01, FR-02, FR-03, FR-07 |

### 5.3 UC-02: Lihat Dashboard Anomali

| Atribut | Detail |
|---|---|
| **ID** | UC-02 |
| **Nama** | Lihat Dashboard Anomali |
| **Aktor Utama** | Auditor / Investigator |
| **Prasyarat** | File output hasil inferensi tersedia di `output/` |
| **Alur Utama** | 1. Pengguna menjalankan `python dashboard/app.py` |
| | 2. Dashboard terbuka di browser lokal (localhost:8501) |
| | 3. Pengguna memilih filter: provinsi, rentang tanggal, threshold skor |
| | 4. Dashboard menampilkan tabel transaksi berisiko tertinggi |
| | 5. Pengguna mengklik transaksi untuk melihat detail & penjelasan NLG |
| **Pasca-kondisi** | Pengguna dapat mengidentifikasi transaksi mencurigakan |
| **Referensi FR** | FR-04 |

### 5.4 UC-03: Eksplorasi Vendor Network Graph

| Atribut | Detail |
|---|---|
| **ID** | UC-03 |
| **Nama** | Eksplorasi Vendor Network Graph |
| **Aktor Utama** | Investigator |
| **Prasyarat** | Data vendor dan transaksi tersedia; graph sudah dibangun |
| **Alur Utama** | 1. Pengguna membuka tab "Vendor Network" di dashboard |
| | 2. Sistem menampilkan graf interaktif (node = vendor, edge = relasi) |
| | 3. Pengguna mengklik node vendor untuk melihat daftar transaksi |
| | 4. Sistem menyoroti kluster vendor mencurigakan |
| **Pasca-kondisi** | Pengguna dapat mengidentifikasi jaringan vendor yang berkolusi |
| **Referensi FR** | FR-05 |

### 5.5 UC-04: Generate Laporan PDF

| Atribut | Detail |
|---|---|
| **ID** | UC-04 |
| **Nama** | Generate Laporan PDF |
| **Aktor Utama** | Auditor |
| **Prasyarat** | File output hasil inferensi tersedia |
| **Alur Utama** | 1. Pengguna menjalankan `python src/report/pdf_generator.py --input output/results.json` |
| | 2. Sistem membaca file hasil inferensi |
| | 3. Sistem memfilter transaksi dengan ARS >= threshold (default: 70) |
| | 4. Sistem menghasilkan PDF berisi executive summary + tabel temuan + penjelasan |
| | 5. PDF disimpan di `output/report_[timestamp].pdf` |
| **Pasca-kondisi** | File PDF siap distribusi ke aparat pengawas |
| **Referensi FR** | FR-06 |

### 5.6 UC-05: Latih Ulang Model

| Atribut | Detail |
|---|---|
| **ID** | UC-05 |
| **Nama** | Latih Ulang Model |
| **Aktor Utama** | Developer |
| **Prasyarat** | Data training tersedia di `train_data/`; konfigurasi di `config/config.yaml` |
| **Alur Utama** | 1. Developer menjalankan `python train.py --config config/config.yaml` |
| | 2. Sistem membaca data training dan melakukan preprocessing |
| | 3. Sistem melatih IF, LOF, dan Autoencoder secara sequential |
| | 4. Sistem menyimpan bobot model ke `models/` |
| | 5. Sistem mengevaluasi performa pada validation set dan mencetak metrik |
| **Pasca-kondisi** | File model tersimpan di `models/`; log training tersimpan di `logs/` |
| **Referensi FR** | — |

---

## 6. Spesifikasi Fungsional Detail

### 6.1 SRS-FR-01: Modul Data Ingestion & Validation

**ID:** SRS-FR-01 | **Sumber:** PRD FR-01, FR-07

#### 6.1.1 Pembacaan Data

- Sistem HARUS mendukung format input: **CSV** dan **JSON**.
- Sistem HARUS membaca file dari path lokal; tidak boleh mengakses URL atau API eksternal.
- Sistem HARUS mendukung encoding UTF-8 untuk karakter Bahasa Indonesia.

#### 6.1.2 Validasi Skema

Sistem HARUS memvalidasi kehadiran kolom wajib berikut pada data input:

| Nama Kolom | Tipe Data | Keterangan |
|---|---|---|
| `id_paket` | string | Identifikasi unik paket pengadaan |
| `nama_paket` | string | Nama/deskripsi paket |
| `nilai_kontrak` | float | Nilai kontrak (IDR) |
| `harga_satuan` | float | Harga satuan item (IDR) |
| `jumlah_item` | integer | Jumlah item dalam paket |
| `nama_vendor` | string | Nama penyedia/vendor |
| `npwp_vendor` | string | NPWP vendor (identifier) |
| `tanggal_pengumuman` | date (YYYY-MM-DD) | Tanggal tender diumumkan |
| `tanggal_kontrak` | date (YYYY-MM-DD) | Tanggal penandatanganan kontrak |
| `jumlah_peserta` | integer | Jumlah peserta tender |
| `kode_provinsi` | string | Kode provinsi (2 digit) |
| `kategori_pengadaan` | string | Kategori barang/jasa |
| `metode_pengadaan` | string | Metode (tender/pengadaan langsung/dll) |

- Jika kolom wajib tidak ada: sistem HARUS menghentikan proses dan menampilkan pesan error yang spesifik.
- Jika tipe data tidak sesuai: sistem HARUS mencoba konversi; jika gagal, baris tersebut di-flag sebagai `invalid_row`.

### 6.2 SRS-FR-02: Modul Preprocessing & Feature Engineering

**ID:** SRS-FR-02 | **Sumber:** PRD Bab 6, FR-01

#### 6.2.1 Penanganan Missing Values

| Kolom | Strategi |
|---|---|
| `harga_satuan` | Imputasi dengan **median** `harga_satuan` dari kategori pengadaan yang sama |
| `jumlah_peserta` | Imputasi dengan nilai **1** (paling konservatif) |
| `npwp_vendor` | Set flag `incomplete_vendor_profile = 1` |
| `tanggal_*` | Baris di-drop jika tanggal tidak dapat di-parse |
| Kolom lainnya | Imputasi dengan **modus** untuk kategori; **median** untuk numerik |

#### 6.2.2 Fitur yang Dihasilkan (Feature Set)

Sistem HARUS menghasilkan minimal fitur-fitur berikut:

| Nama Fitur | Formula / Logika | Tipe |
|---|---|---|
| `price_ratio` | `harga_satuan / median_harga_kategori` | float |
| `log_nilai_kontrak` | `log(1 + nilai_kontrak)` | float |
| `days_reg_to_announce` | `tanggal_pengumuman - tanggal_registrasi_vendor` (hari) | integer |
| `is_single_bidder` | 1 jika `jumlah_peserta == 1`, else 0 | binary |
| `incomplete_vendor_profile` | 1 jika NPWP/alamat vendor kosong, else 0 | binary |
| `split_transaction_flag` | 1 jika vendor sama menang > N paket serupa dalam 30 hari | binary |
| `vendor_win_rate_30d` | Jumlah kemenangan vendor dalam 30 hari terakhir | integer |
| `nilai_kontrak_zscore` | Z-score `nilai_kontrak` dalam kategori | float |
| `month_of_year` | Bulan pengumuman (1-12) | integer |
| `quarter` | Kuartal pengumuman (1-4) | integer |
| `is_yearend` | 1 jika bulan 11 atau 12 | binary |
| `metode_encoded` | Label encoding metode pengadaan | integer |
| `kategori_encoded` | Label encoding kategori pengadaan | integer |
| `vendor_network_degree` | Jumlah vendor lain yang terhubung (berbagi direktur/alamat) | integer |

#### 6.2.3 Normalisasi

- Fitur numerik kontinu HARUS dinormalisasi menggunakan **RobustScaler** (tahan outlier).
- Scaler HARUS di-fit hanya pada `train_data` dan disimpan sebagai `models/scaler.joblib`.
- Scaler HARUS diterapkan (transform) pada `validation_data` dan `test_data` tanpa re-fitting.

### 6.3 SRS-FR-03: Layer 1 — Statistical Baseline

**ID:** SRS-FR-03 | **Sumber:** PRD Bab 5, FR-01

#### 6.3.1 Isolation Forest

- **Library:** `sklearn.ensemble.IsolationForest`
- **Hyperparameter wajib:**
  - `n_estimators`: 100 (default; dapat di-tune)
  - `contamination`: 0.05 (estimasi awal proporsi anomali)
  - `random_state`: 42 (wajib untuk reproducibility)
  - `max_samples`: 'auto'
- **Output:** Skor anomali raw (`decision_function`) dalam rentang [-1, 1]; semakin negatif = semakin anomali.
- **Normalisasi output:** Konversi ke rentang [0, 100] menggunakan: `score_if = (1 - decision_function) / 2 * 100`

#### 6.3.2 Local Outlier Factor

- **Library:** `sklearn.neighbors.LocalOutlierFactor`
- **Mode inferensi:** Gunakan `novelty=True` agar LOF dapat digunakan untuk prediksi data baru.
- **Hyperparameter wajib:**
  - `n_neighbors`: 20
  - `contamination`: 0.05
  - `novelty`: True
  - `metric`: 'euclidean'
- **Output:** Normalized outlier score dalam rentang [0, 100].

#### 6.3.3 Agregasi Skor Layer 1

```
score_layer1 = 0.6 * score_IF + 0.4 * score_LOF
```

### 6.4 SRS-FR-04: Layer 2 — Deep Anomaly Detection (Autoencoder)

**ID:** SRS-FR-04 | **Sumber:** PRD Bab 5, FR-01

#### 6.4.1 Arsitektur Autoencoder

```
Input Layer:  [N_features]
    |
Encoder:
    Dense(64, activation='relu')
    Dense(32, activation='relu')
    Dense(16, activation='relu')  <-- Bottleneck
    |
Decoder:
    Dense(32, activation='relu')
    Dense(64, activation='relu')
    Dense(N_features, activation='linear')  <-- Output
    |
Output Layer: [N_features]  (rekonstruksi)
```

- **Loss function:** Mean Squared Error (MSE)
- **Optimizer:** Adam, learning_rate=0.001
- **Framework:** PyTorch **atau** TensorFlow/Keras (pilih salah satu; konsisten)
- **Epochs training:** Maksimum 50 dengan EarlyStopping (patience=5, monitor val_loss)

#### 6.4.2 Penghitungan Anomaly Score dari Autoencoder

- **Reconstruction Error:** `MSE(input, reconstructed_output)` per sampel
- **Normalisasi:** Percentile-based normalization terhadap distribution error pada training set:
  - `score_AE = min(reconstruction_error / percentile_95_train_error * 100, 100)`

#### 6.4.3 Agregasi Skor Layer 1 + Layer 2 (Final ARS)

```
ARS = round(0.4 * score_layer1 + 0.6 * score_AE)
```

*Bobot dapat di-tune; nilai di atas adalah default dan harus terdokumentasi di `config.yaml`.*

- `ARS` adalah bilangan bulat dalam rentang **[0, 100]**.
- **Klasifikasi risiko:**
  - ARS 0–39: Risiko Rendah
  - ARS 40–69: Risiko Sedang
  - ARS 70–84: Risiko Tinggi
  - ARS 85–100: Risiko Sangat Tinggi

### 6.5 SRS-FR-05: Layer 3 — Explainability Engine

**ID:** SRS-FR-05 | **Sumber:** PRD FR-02, C-1, C-2, C-3

#### 6.5.1 SHAP Engine

- **Library:** `shap` (versi >= 0.42)
- **Explainer untuk Layer 1 (Isolation Forest):**
  - Gunakan `shap.TreeExplainer(isolation_forest_model)`
  - Hitung SHAP values untuk setiap sampel uji
- **Explainer untuk Layer 2 (Autoencoder):**
  - Gunakan `shap.KernelExplainer` dengan background dataset = subsample 100-300 sampel training
  - Hitung SHAP values untuk reconstruction error
- **Output SHAP per sampel:**
  ```json
  {
    "shap_values": {
      "price_ratio": 0.42,
      "days_reg_to_announce": 0.28,
      "is_single_bidder": 0.17,
      "vendor_win_rate_30d": 0.08,
      ...
    },
    "base_value": 0.15
  }
  ```
- **Constraint:** Wajib menghasilkan top-3 fitur beserta arah pengaruh (positif/negatif).

#### 6.5.2 LIME Engine

- **Library:** `lime` (versi >= 0.2)
- **Fungsi:** Validasi silang hasil SHAP; digunakan untuk sampel dengan ARS >= 70.
- **Explainer:** `lime.tabular.LimeTabularExplainer`
- **Num_features output:** Minimal 3.
- **Output LIME per sampel:**
  ```json
  {
    "lime_explanation": [
      {"feature": "price_ratio > 1.5", "weight": 0.38, "direction": "positive"},
      {"feature": "days_reg_to_announce < 7", "weight": 0.25, "direction": "positive"},
      {"feature": "is_single_bidder = 1", "weight": 0.21, "direction": "positive"}
    ]
  }
  ```

#### 6.5.3 Kontrak Output Layer 3

Sistem HARUS menghasilkan objek JSON berikut untuk setiap transaksi yang dianalisis:

```json
{
  "id_paket": "string",
  "ars": 87,
  "risk_level": "Risiko Sangat Tinggi",
  "top_features": [
    {"rank": 1, "feature": "price_ratio", "shap_value": 0.42, "direction": "positif", "human_label": "Rasio harga satuan terhadap median pasar"},
    {"rank": 2, "feature": "days_reg_to_announce", "shap_value": 0.28, "direction": "positif", "human_label": "Jarak hari registrasi vendor ke pengumuman tender"},
    {"rank": 3, "feature": "is_single_bidder", "shap_value": 0.17, "direction": "positif", "human_label": "Tender hanya diikuti satu peserta"}
  ],
  "raw_feature_values": {
    "price_ratio": 3.2,
    "days_reg_to_announce": 3,
    "is_single_bidder": 1
  }
}
```

### 6.6 SRS-FR-06: Layer 4 — Natural Language Generator (NLG)

**ID:** SRS-FR-06 | **Sumber:** PRD FR-03, C-2, C-4

#### 6.6.1 Arsitektur NLG

- **Pendekatan:** Template-based NLG dengan Rule Engine berbasis Python murni.
- **Tidak diperbolehkan:** Penggunaan API LLM eksternal (OpenAI, Gemini, Claude, dll).
- **Library:** Jinja2 untuk rendering template; tidak ada dependency model bahasa besar.

#### 6.6.2 Template Penjelasan

Sistem menggunakan template bertingkat berdasarkan kombinasi fitur:

**Template Level 1 — Header:**
```
Transaksi #{{ id_paket }} memiliki Skor Risiko Anomali {{ ars }}/100 ({{ risk_level }}).
```

**Template Level 2 — Faktor Risiko (per fitur):**

| Kondisi Fitur | Template Teks |
|---|---|
| `price_ratio > 2.0` | "Harga satuan {{ harga_satuan_fmt }} tercatat {{ price_ratio }}x di atas median pasar untuk kategori {{ kategori }}" |
| `price_ratio > 1.5` | "Harga satuan berada {{ persen_di_atas }}% di atas median pasar kategori {{ kategori }}" |
| `days_reg_to_announce < 7` | "Vendor '{{ nama_vendor }}' baru terdaftar {{ days_reg_to_announce }} hari sebelum tender diumumkan" |
| `is_single_bidder == 1` | "Tender hanya diikuti oleh 1 peserta, mengindikasikan minimnya kompetisi" |
| `split_transaction_flag == 1` | "Terdeteksi pola pemecahan transaksi (split transaction): vendor yang sama memenangkan {{ n_paket }} paket serupa dalam {{ n_hari }} hari" |
| `vendor_network_degree > 3` | "Vendor terhubung dengan {{ degree }} vendor lain dalam jaringan yang sama" |
| `is_yearend == 1` | "Transaksi dilakukan pada akhir tahun anggaran (bulan {{ month }}), periode berisiko tinggi" |

**Template Level 3 — Rekomendasi:**
```
Rekomendasi: Transaksi ini memerlukan pemeriksaan lebih lanjut oleh auditor terkait {{ rekomendasi_topik }}.
```

#### 6.6.3 Kontrak Output Layer 4

```json
{
  "id_paket": "string",
  "nlg_explanation": {
    "header": "Transaksi #PKD-DKI-2024-00812 memiliki Skor Risiko Anomali 87/100 (Risiko Sangat Tinggi).",
    "factors": [
      "Harga satuan Rp 45.000.000 tercatat 3,2x di atas median pasar untuk kategori Pengadaan Laptop.",
      "Vendor 'PT Maju Jaya Sentosa' baru terdaftar 3 hari sebelum tender diumumkan.",
      "Tender hanya diikuti oleh 1 peserta, mengindikasikan minimnya kompetisi."
    ],
    "recommendation": "Rekomendasi: Transaksi ini memerlukan pemeriksaan lebih lanjut oleh auditor terkait kewajaran harga dan legitimasi vendor.",
    "full_text": "Transaksi #PKD-DKI-2024-00812 memiliki Skor Risiko Anomali 87/100 (Risiko Sangat Tinggi). Harga satuan Rp 45.000.000 tercatat 3,2x di atas median pasar untuk kategori Pengadaan Laptop. Vendor 'PT Maju Jaya Sentosa' baru terdaftar 3 hari sebelum tender diumumkan. Tender hanya diikuti oleh 1 peserta, mengindikasikan minimnya kompetisi. Rekomendasi: Transaksi ini memerlukan pemeriksaan lebih lanjut oleh auditor terkait kewajaran harga dan legitimasi vendor."
  }
}
```

### 6.7 SRS-FR-07: Modul Score Aggregator

**ID:** SRS-FR-07

- Menerima output dari Layer 1 (`score_layer1`) dan Layer 2 (`score_AE`).
- Menghitung `ARS` menggunakan formula yang terdefinisi di `config.yaml`.
- Mengklasifikasikan risiko berdasarkan threshold yang terdefinisi.
- Mengekspor hasil ke format JSON standar untuk konsumsi Layer 3 & 4.

### 6.8 SRS-FR-08: Modul Dashboard

**ID:** SRS-FR-08 | **Sumber:** PRD FR-04, FR-05

#### 6.8.1 Halaman Utama — Pattern Alert

- Menampilkan **KPI cards:** Total transaksi dianalisis, Jumlah anomali terdeteksi (ARS >= 70), Total nilai paket berisiko tinggi.
- Menampilkan **tabel interaktif** berisi transaksi dengan ARS tertinggi, kolom: `id_paket`, `nama_paket`, `nama_vendor`, `nilai_kontrak`, `ARS`, `risk_level`.
- Menyediakan filter: provinsi (`kode_provinsi`), rentang tanggal (`tanggal_kontrak`), threshold ARS minimum, kategori pengadaan.
- Menampilkan **grafik tren** jumlah anomali per bulan/kuartal.
- Saat baris diklik: menampilkan panel detail berisi penjelasan NLG lengkap + SHAP bar chart.

#### 6.8.2 Halaman Vendor Network Graph

- Memvisualisasikan graf vendor menggunakan library **pyvis** atau **networkx + matplotlib**.
- **Node:** Setiap vendor unik (ukuran node proporsional dengan total nilai kontrak).
- **Edge:** Relasi antar vendor (berbagi direktur, alamat, atau pola menang bergantian).
- **Warna node:**
  - Merah: Vendor dengan rata-rata ARS >= 70
  - Kuning: Vendor dengan rata-rata ARS 40-69
  - Hijau: Vendor dengan rata-rata ARS < 40
- Fitur interaktif: zoom, pan, klik node untuk detail.

### 6.9 SRS-FR-09: Modul Laporan PDF

**ID:** SRS-FR-09 | **Sumber:** PRD FR-06

- **Library:** `reportlab` atau `weasyprint`
- **Struktur PDF:**

| Bagian | Konten |
|---|---|
| Halaman Sampul | Judul, tanggal generate, wilayah analisis |
| Executive Summary | Statistik kunci (total transaksi, jumlah temuan, total nilai berisiko) |
| Tabel Temuan Utama | Top-20 transaksi ARS tertinggi |
| Detail Per Temuan | Untuk setiap transaksi ARS >= 70: penjelasan NLG lengkap + nilai fitur kunci |
| Lampiran | Metodologi singkat, definisi ARS |

- **Threshold default PDF:** ARS >= 70.
- **Format output:** `output/report_YYYYMMDD_HHMMSS.pdf`.

---

## 7. Spesifikasi Data & Skema

### 7.1 Skema Input Utama (Raw Transaction Data)

```json
{
  "id_paket": "PKD-DKI-2024-00812",
  "nama_paket": "Pengadaan Laptop Dinas Pendidikan DKI Jakarta",
  "nilai_kontrak": 450000000.0,
  "harga_satuan": 45000000.0,
  "jumlah_item": 10,
  "nama_vendor": "PT Maju Jaya Sentosa",
  "npwp_vendor": "01.234.567.8-901.000",
  "tanggal_pengumuman": "2024-11-01",
  "tanggal_kontrak": "2024-11-15",
  "jumlah_peserta": 1,
  "kode_provinsi": "31",
  "kategori_pengadaan": "Laptop",
  "metode_pengadaan": "Pengadaan Langsung"
}
```

### 7.2 Skema Output Inferensi (results JSON)

```json
{
  "metadata": {
    "generated_at": "2024-11-20T14:30:00",
    "total_records": 500000,
    "high_risk_count": 1247,
    "model_version": "1.0.0"
  },
  "results": [
    {
      "id_paket": "PKD-DKI-2024-00812",
      "ars": 87,
      "risk_level": "Risiko Sangat Tinggi",
      "score_layer1": 72.3,
      "score_ae": 96.1,
      "top_features": [...],
      "raw_feature_values": {...},
      "nlg_explanation": {...}
    }
  ]
}
```

### 7.3 Skema Konfigurasi (config.yaml)

```yaml
system:
  name: "MATA RAKYAT"
  version: "1.0.0"
  random_seed: 42

data:
  train_path: "train_data/"
  test_path: "test_data/"
  output_path: "output/"
  supported_provinces: ["31", "35", "73"]  # DKI Jakarta, Jawa Timur, Sulawesi Selatan

preprocessing:
  imputation_strategy:
    harga_satuan: "median_by_category"
    jumlah_peserta: 1
  drop_invalid_dates: true

models:
  path: "models/"
  isolation_forest:
    n_estimators: 100
    contamination: 0.05
    random_state: 42
  lof:
    n_neighbors: 20
    contamination: 0.05
    novelty: true
  autoencoder:
    hidden_dims: [64, 32, 16]
    epochs: 50
    batch_size: 256
    learning_rate: 0.001
    early_stopping_patience: 5

scoring:
  weights:
    layer1: 0.4
    layer2: 0.6
  layer1_weights:
    isolation_forest: 0.6
    lof: 0.4
  thresholds:
    low_risk: 40
    medium_risk: 70
    high_risk: 85

explainability:
  shap_background_samples: 200
  min_top_features: 3

nlg:
  template_dir: "src/nlg/templates/"

report:
  pdf_threshold_ars: 70
  max_detail_items: 20

inference:
  batch_size: 1000
  max_inference_time_seconds: 3.0
```

---

## 8. Pipeline Pemrosesan Data (Data Flow)

### 8.1 Pipeline Training

```
[train_data/]
     |
     v
[1. DataReader.read()]
     |-- Baca CSV/JSON dari train_data/
     |
     v
[2. DataValidator.validate()]
     |-- Validasi skema kolom wajib
     |-- Laporkan invalid rows
     |
     v
[3. Cleaner.clean()]
     |-- Handle missing values (imputasi/drop)
     |-- Drop baris tanggal invalid
     |
     v
[4. FeatureEngineer.transform()]
     |-- Hitung semua fitur derivatif
     |-- Label encoding
     |
     v
[5. RobustScaler.fit_transform()]
     |-- Fit scaler pada training data
     |-- Simpan scaler.joblib
     |
     v
[6. SMOTE.fit_resample()]   (hanya pada validation layer)
     |-- Oversample kelas positif
     |
     v
[7. IsolationForest.fit()]   -- Simpan models/isolation_forest.joblib
[7. LOF.fit()]               -- Simpan models/lof_model.joblib
[7. Autoencoder.train()]     -- Simpan models/autoencoder.pt
     |
     v
[8. Evaluasi pada validation set]
     |-- Recall, Precision, F1, AUC-ROC
     |-- Simpan ke logs/training_metrics.json
```

### 8.2 Pipeline Inferensi (`inference.py`)

```
[Input: data CSV/JSON]
     |
     v  t=0ms
[1. DataReader + DataValidator]
     |
     v  t~50ms
[2. Cleaner + FeatureEngineer]
     |-- RobustScaler.transform() (load dari models/scaler.joblib)
     |
     v  t~150ms
[3. Layer 1: IF.predict() + LOF.predict()]
     |-- score_layer1 = 0.6*score_IF + 0.4*score_LOF
     |
     v  t~400ms
[4. Layer 2: Autoencoder.forward()]
     |-- Hitung reconstruction error
     |-- score_AE = normalisasi percentile
     |
     v  t~600ms
[5. ScoreAggregator]
     |-- ARS = round(0.4*score_layer1 + 0.6*score_AE)
     |-- risk_level = klasifikasi
     |
     v  t~1200ms
[6. Layer 3: SHAP Engine]
     |-- TreeExplainer untuk IF
     |-- KernelExplainer untuk AE (jika ARS >= 40)
     |-- Ekstrak top_features
     |
     v  t~1700ms
[7. Layer 4: NLG Generator]
     |-- Template matching per fitur
     |-- Render teks Bahasa Indonesia
     |
     v  t~1800ms (target < 2000ms)
[8. Output Writer]
     |-- Simpan ke output/results_[timestamp].json
     |-- Print ringkasan ke terminal
```

**Catatan waktu:** Seluruh pipeline HARUS selesai dalam <= 3000ms per sampel pada CPU i5 Gen 8.

---

## 9. Spesifikasi Model AI

### 9.1 Spesifikasi Isolation Forest

| Parameter | Nilai | Keterangan |
|---|---|---|
| `n_estimators` | 100 | Jumlah pohon dalam ensemble |
| `contamination` | 0.05 | Proporsi outlier yang diharapkan |
| `max_samples` | 'auto' | Jumlah sampel per pohon |
| `random_state` | 42 | Seed untuk reproducibility |
| `n_jobs` | -1 | Gunakan semua core CPU |
| **File output** | `models/isolation_forest.joblib` | Tersimpan dengan kompresi level 3 |
| **Estimasi ukuran** | < 5 MB | — |

### 9.2 Spesifikasi Local Outlier Factor

| Parameter | Nilai | Keterangan |
|---|---|---|
| `n_neighbors` | 20 | Jumlah tetangga untuk density estimation |
| `contamination` | 0.05 | — |
| `novelty` | True | Wajib untuk inferensi data baru |
| `metric` | 'euclidean' | Metrik jarak |
| `n_jobs` | -1 | — |
| **File output** | `models/lof_model.joblib` | — |
| **Estimasi ukuran** | < 3 MB | — |

### 9.3 Spesifikasi Autoencoder Neural Network

| Parameter | Nilai | Keterangan |
|---|---|---|
| **Arsitektur** | Input→64→32→16→32→64→Output | Symmetric encoder-decoder |
| `activation` | ReLU (semua layer kecuali output) | — |
| `output_activation` | Linear | Untuk rekonstruksi nilai kontinu |
| `loss` | MSE | Mean Squared Error |
| `optimizer` | Adam | lr=0.001, beta1=0.9, beta2=0.999 |
| `max_epochs` | 50 | Dengan EarlyStopping |
| `early_stopping_patience` | 5 | Monitor: val_loss |
| `batch_size` | 256 | — |
| **File output** | `models/autoencoder.pt` (PyTorch) | — |
| **Estimasi ukuran** | < 15 MB | — |

### 9.4 Estimasi Total Ukuran Model

| File | Estimasi Ukuran |
|---|---|
| `isolation_forest.joblib` | < 5 MB |
| `lof_model.joblib` | < 3 MB |
| `autoencoder.pt` | < 15 MB |
| `scaler.joblib` | < 1 MB |
| `shap_background.npy` | < 2 MB |
| **TOTAL** | **< 26 MB** (batas: 50 MB) |

---

## 10. Spesifikasi Antarmuka Sistem

### 10.1 Antarmuka Command Line Interface (CLI)

#### 10.1.1 `inference.py`

```bash
python inference.py [OPTIONS]

Options:
  --input   PATH    Path ke file input CSV/JSON (wajib)
  --output  PATH    Path folder output (default: output/)
  --config  PATH    Path ke config.yaml (default: config/config.yaml)
  --batch-size INT  Jumlah baris per batch (default: 1000)
  --threshold INT   ARS minimum untuk highlight (default: 70)
  --help            Tampilkan bantuan

Contoh:
  python inference.py --input test_data/sample_500k.csv --output output/
```

**Exit codes:**
- `0`: Sukses
- `1`: File input tidak ditemukan
- `2`: Validasi skema gagal
- `3`: Model tidak ditemukan di `models/`

#### 10.1.2 `train.py`

```bash
python train.py [OPTIONS]

Options:
  --config  PATH    Path ke config.yaml (wajib)
  --data    PATH    Override path data training
  --help            Tampilkan bantuan

Contoh:
  python train.py --config config/config.yaml
```

### 10.2 Antarmuka File (I/O)

| Jenis | Format | Path | Keterangan |
|---|---|---|---|
| Input Data | CSV / JSON | Ditentukan via `--input` | Wajib mengikuti skema Bab 7.1 |
| Output Hasil | JSON | `output/results_[timestamp].json` | Skema Bab 7.2 |
| Output PDF | PDF | `output/report_[timestamp].pdf` | Dipanggil via pdf_generator.py |
| Model IF | joblib | `models/isolation_forest.joblib` | — |
| Model LOF | joblib | `models/lof_model.joblib` | — |
| Model AE | .pt / .h5 | `models/autoencoder.pt` | — |
| Scaler | joblib | `models/scaler.joblib` | — |
| Config | YAML | `config/config.yaml` | — |
| Log Training | JSON | `logs/training_metrics.json` | — |

### 10.3 Antarmuka Dashboard

- **Teknologi:** Streamlit (direkomendasikan) atau Dash
- **Port:** localhost:8501 (Streamlit default)
- **Input:** Membaca file JSON dari folder `output/`
- **Tidak memerlukan koneksi internet** untuk beroperasi

---

## 11. Spesifikasi Non-Fungsional Teknis

### 11.1 Kecepatan Inferensi (WAJIB — Constraint Hackathon)

| Kondisi | Target | Batas Maksimum |
|---|---|---|
| CPU Intel Core i5 Gen 8 (1 core) | < 2 detik/sampel | **3 detik/sampel** |
| CPU Intel Core i5 Gen 8 (multi-core) | < 1 detik/sampel | — |
| GPU localhost (opsional, saat demo) | < 0.5 detik/sampel | — |

**Pengukuran wajib:** Validasi kecepatan dilakukan pada kondisi CPU-only tanpa GPU.

**Strategi pemenuhan:**
1. Gunakan `shap.TreeExplainer` (hanya Layer 1) — jauh lebih cepat dari KernelExplainer.
2. LIME hanya dijalankan untuk ARS >= 70 (tidak untuk semua sampel).
3. Autoencoder: arsitektur compact, tidak lebih dari 3 hidden layer per sisi.
4. Batch processing dengan `numpy` vectorization, hindari Python loop.
5. Pre-load model ke memori saat startup, bukan saat setiap inferensi.

### 11.2 Ukuran Model (WAJIB — Constraint Hackathon)

- Total file bobot model (di folder `models/`) **<= 50 MB**.
- Divalidasi dengan: `du -sh models/` sebelum submission.

### 11.3 Reproducibility

- **Random seed:** `42` digunakan di semua komponen (sklearn, PyTorch/TF, numpy).
- **Versi library:** Semua versi library didokumentasikan di `requirements.txt`.
- **Deterministic behavior:** Aktifkan `torch.backends.cudnn.deterministic = True` (jika PyTorch dengan GPU).

### 11.4 Kompatibilitas Python & Library

| Komponen | Versi Minimum | Versi Direkomendasikan |
|---|---|---|
| Python | 3.9 | 3.11 |
| scikit-learn | 1.3.0 | 1.4.x |
| PyTorch | 2.0.0 | 2.2.x |
| shap | 0.42.0 | 0.45.x |
| lime | 0.2.0 | 0.2.x |
| pandas | 1.5.0 | 2.1.x |
| numpy | 1.24.0 | 1.26.x |
| streamlit | 1.28.0 | 1.32.x |
| reportlab | 3.6.0 | 4.1.x |
| jinja2 | 3.1.0 | 3.1.x |
| pyvis | 0.3.0 | 0.3.x |
| imbalanced-learn | 0.10.0 | 0.12.x |
| pyyaml | 6.0 | 6.0.x |
| joblib | 1.3.0 | 1.4.x |

### 11.5 Keamanan & Privasi

- **Tidak ada data yang verluar dari localhost** selama proses inferensi.
- File output (`results_*.json`, `report_*.pdf`) disimpan lokal; tidak di-upload ke layanan eksternal.
- Data NPWP dan nama vendor dalam output JSON dikontrol aksesnya — tidak dipublikasikan tanpa otorisasi.

---

## 12. Spesifikasi Pengujian

### 12.1 Unit Test

| Test Case | Modul | Kondisi | Expected |
|---|---|---|---|
| UT-01 | DataValidator | Input CSV dengan semua kolom wajib | Validasi PASS |
| UT-02 | DataValidator | Input CSV tanpa kolom `nilai_kontrak` | Raise ValueError |
| UT-03 | Cleaner | Baris dengan `harga_satuan` null | Diimputasi dengan median kategori |
| UT-04 | Cleaner | Baris dengan `tanggal_kontrak` invalid | Baris di-drop |
| UT-05 | FeatureEngineer | Harga 3x median | `price_ratio = 3.0` |
| UT-06 | FeatureEngineer | `jumlah_peserta = 1` | `is_single_bidder = 1` |
| UT-07 | IsolationForest | 1 sampel known anomali | `score_IF >= 70` |
| UT-08 | ScoreAggregator | `score_layer1=80, score_AE=90` | `ARS = 86` |
| UT-09 | SHAPEngine | Output SHAP untuk 1 sampel | Dict berisi >= 3 fitur |
| UT-10 | NLGGenerator | `price_ratio = 3.2, days_reg = 3` | Teks mengandung "3,2x" dan "3 hari" |
| UT-11 | PDFGenerator | Input JSON dengan 5 item ARS >= 70 | PDF dihasilkan, > 0 bytes |
| UT-12 | InferencePipeline | 1 sampel valid end-to-end | Selesai dalam <= 3 detik |

### 12.2 Integration Test

| Test Case | Deskripsi | Expected |
|---|---|---|
| IT-01 | Pipeline inferensi end-to-end dengan 100 sampel | Output JSON valid, semua ID paket terepresentasi |
| IT-02 | Pipeline inferensi dengan missing values | Tidak crash; baris valid tetap diproses |
| IT-03 | Dashboard load hasil JSON 500K transaksi | Dashboard responsif dalam < 5 detik load awal |
| IT-04 | PDF generate dari JSON 1000+ transaksi ARS >= 70 | PDF valid, dapat dibuka |

### 12.3 Performance Test

| Test Case | Kondisi | Metrik | Target |
|---|---|---|---|
| PT-01 | Inferensi 1 sampel, CPU i5 Gen 8, tanpa GPU | Waktu eksekusi | <= 3 detik |
| PT-02 | Inferensi batch 1000 sampel | Memory usage | <= 2 GB RAM |
| PT-03 | Total ukuran `models/` | `du -sh models/` | <= 50 MB |
| PT-04 | Inferensi 500.000 sampel batch | Total waktu | Terdokumentasi |

### 12.4 Model Validation Test

| Test Case | Dataset | Metrik | Target |
|---|---|---|---|
| MV-01 | Test Data 2024 (unseen) | Recall | >= 80% |
| MV-02 | Test Data 2024 | Precision | >= 50% |
| MV-03 | Test Data 2024 | F1-Score | >= 60% |
| MV-04 | Test Data 2024 | AUC-ROC | >= 0.85 |
| MV-05 | Test Data 2024 | Penjelasan dengan >= 3 fitur | 100% sampel ARS >= 40 |

---

## 13. Struktur Direktori & Artefak

```
mata_rakyat/
|
+-- config/
|   +-- config.yaml                    <- Konfigurasi global sistem
|
+-- models/                            <- FILE MODEL (submit terpisah dari data)
|   +-- isolation_forest.joblib        <- Layer 1: IF model
|   +-- lof_model.joblib               <- Layer 1: LOF model
|   +-- autoencoder.pt                 <- Layer 2: Autoencoder weights
|   +-- scaler.joblib                  <- RobustScaler fit dari training
|   +-- shap_background.npy            <- Background dataset untuk SHAP KernelExplainer
|
+-- train_data/                        <- TRAINING DATA (dipisah dari models/)
|   +-- transactions_2019_2022.csv     <- 70% split: 2019-2022
|   +-- labels_2019_2022.csv           <- Ground truth dari putusan MA + audit BPK
|   +-- ecatalog_prices.csv            <- Referensi harga e-katalog LKPP
|   +-- vendor_registry.csv            <- Data perusahaan dari AHU
|
+-- test_data/                         <- TEST DATA (UNSEEN — dipisah dari models/)
|   +-- transactions_2024.csv          <- 15% split: 2024 (unseen)
|   +-- labels_2024.csv                <- Ground truth 2024
|
+-- src/
|   +-- ingestion/
|   |   +-- __init__.py
|   |   +-- reader.py                  <- DataReader class
|   |   +-- validator.py               <- DataValidator class
|   |
|   +-- preprocessing/
|   |   +-- __init__.py
|   |   +-- cleaner.py                 <- Cleaner class (imputasi, drop)
|   |
|   +-- features/
|   |   +-- __init__.py
|   |   +-- engineer.py                <- FeatureEngineer class
|   |
|   +-- models/
|   |   +-- __init__.py
|   |   +-- isolation_forest.py        <- IFModel: train, predict, save, load
|   |   +-- lof.py                     <- LOFModel: train, predict, save, load
|   |   +-- autoencoder.py             <- AutoencoderModel: train, infer, save, load
|   |   +-- score_aggregator.py        <- ScoreAggregator: calculate ARS
|   |
|   +-- explainability/
|   |   +-- __init__.py
|   |   +-- shap_engine.py             <- SHAPEngine: compute, extract top_features
|   |   +-- lime_engine.py             <- LIMEEngine: compute explanations
|   |
|   +-- nlg/
|   |   +-- __init__.py
|   |   +-- generator.py               <- NLGGenerator: render template
|   |   +-- templates/
|   |       +-- header.j2              <- Template header penjelasan
|   |       +-- factors.j2             <- Template per faktor risiko
|   |       +-- recommendation.j2      <- Template rekomendasi
|   |
|   +-- report/
|       +-- __init__.py
|       +-- pdf_generator.py           <- PDFGenerator: generate laporan PDF
|
+-- dashboard/
|   +-- app.py                         <- Entry point dashboard (Streamlit/Dash)
|   +-- network.py                     <- Vendor Network Graph module
|   +-- components/
|       +-- kpi_cards.py               <- Komponen KPI card
|       +-- transaction_table.py       <- Komponen tabel interaktif
|       +-- trend_chart.py             <- Komponen grafik tren
|       +-- detail_panel.py            <- Komponen panel detail transaksi
|
+-- output/                            <- Output generated (gitignore recommended)
|   +-- results_[timestamp].json       <- Hasil inferensi
|   +-- report_[timestamp].pdf         <- Laporan PDF
|
+-- logs/
|   +-- training_metrics.json          <- Metrik evaluasi training
|   +-- inference_log_[timestamp].txt  <- Log inferensi
|
+-- tests/
|   +-- test_validator.py
|   +-- test_cleaner.py
|   +-- test_features.py
|   +-- test_models.py
|   +-- test_explainability.py
|   +-- test_nlg.py
|   +-- test_pipeline.py               <- Integration + performance test
|
+-- inference.py                       <- Entry point inferensi (WAJIB)
+-- train.py                           <- Entry point training
+-- requirements.txt                   <- Daftar dependency dengan versi
+-- README.md                          <- Dokumentasi penggunaan sistem
```

---

## 14. Dependensi & Lingkungan

### 14.1 `requirements.txt`

```
# Core Data Science
numpy>=1.24.0
pandas>=1.5.0
scikit-learn>=1.3.0
imbalanced-learn>=0.10.0
joblib>=1.3.0

# Deep Learning (pilih salah satu)
torch>=2.0.0          # PyTorch (direkomendasikan)
# tensorflow>=2.12.0  # Alternatif TensorFlow

# Explainability
shap>=0.42.0
lime>=0.2.0

# NLG Templating
Jinja2>=3.1.0

# Dashboard
streamlit>=1.28.0
pyvis>=0.3.0
plotly>=5.15.0

# PDF Generation
reportlab>=3.6.0

# Config
PyYAML>=6.0

# Utilities
scipy>=1.10.0
networkx>=3.0
```

### 14.2 Spesifikasi Lingkungan Minimum

| Komponen | Minimum | Direkomendasikan |
|---|---|---|
| CPU | Intel Core i5 Gen 8 | Intel Core i7 Gen 10+ |
| RAM | 8 GB | 16 GB |
| Disk | 5 GB free | 20 GB free |
| OS | Windows 10 / Ubuntu 20.04 / macOS 12 | — |
| Python | 3.9 | 3.11 |
| GPU | Tidak wajib | CUDA-compatible NVIDIA |

### 14.3 Setup & Instalasi

```bash
# 1. Clone / extract project
cd mata_rakyat/

# 2. Buat virtual environment
python -m venv venv
source venv/bin/activate          # Linux/macOS
venv\Scripts\activate             # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Training model (jika belum ada models/)
python train.py --config config/config.yaml

# 5. Jalankan inferensi
python inference.py --input test_data/transactions_2024.csv

# 6. Jalankan dashboard
streamlit run dashboard/app.py

# 7. Generate PDF
python src/report/pdf_generator.py --input output/results_latest.json
```

---

## 15. Batasan Teknis & Asumsi

### 15.1 Batasan Teknis

1. **Offline total:** Sistem dirancang untuk beroperasi tanpa koneksi internet. Pengumpulan data (scraping/API) dilakukan terpisah sebelum training dan bukan bagian dari pipeline inferensi.
2. **Skala prototipe:** Sistem ini adalah prototipe untuk 3 provinsi. Generalisasi ke 34 provinsi memerlukan retraining dan validasi tambahan.
3. **Label terbatas:** Ground truth hanya berasal dari kasus korupsi yang sudah inkrah di MA (~8.000 kasus). Sebagian besar data tidak berlabel, sehingga evaluasi supervised bergantung pada subset berlabel ini.
4. **Latensi SHAP KernelExplainer:** Jika digunakan untuk Autoencoder, KernelExplainer bisa lambat. Dibatasi dengan subsample background 100-300 sampel dan hanya untuk sampel ARS >= 40.
5. **Graph vendor:** Relasi antar vendor (berbagi direktur, alamat) bergantung pada ketersediaan dan kualitas data AHU. Jika data AHU tidak lengkap, fitur `vendor_network_degree` di-fallback ke 0.

### 15.2 Asumsi

1. Data dari LKPP/SPSE diasumsikan memiliki kolom `id_paket` yang unik per paket pengadaan.
2. Harga referensi e-katalog LKPP diasumsikan representatif untuk median pasar kategori yang sama.
3. Tanggal registrasi vendor dari AHU diasumsikan tersedia dan dapat dihubungkan ke `npwp_vendor`.
4. Validation set (2023) dan Testing set (2024) diasumsikan tidak bocor ke training set karena split dilakukan secara temporal.
5. Pengukuran kecepatan inferensi oleh juri dilakukan pada satu sampel tunggal, bukan batch.

---

## 16. Matriks Keterlacakan Persyaratan

| ID SRS | Nama Persyaratan | ID PRD | Constraint Hackathon | UC Terkait |
|---|---|---|---|---|
| SRS-FR-01 | Data Ingestion & Validation | FR-01, FR-07 | C-4 (no cloud) | UC-01, UC-05 |
| SRS-FR-02 | Preprocessing & Feature Engineering | FR-01 | — | UC-01, UC-05 |
| SRS-FR-03 | Layer 1 Statistical Baseline | FR-01 | C-5 (inferensi <=3s), C-6 (<=50MB) | UC-01 |
| SRS-FR-04 | Layer 2 Autoencoder | FR-01 | C-5, C-6 | UC-01 |
| SRS-FR-05 | Layer 3 Explainability Engine | FR-02 | C-1 (explainability), C-3 (anti-blackbox) | UC-01, UC-06 |
| SRS-FR-06 | Layer 4 NLG | FR-03 | C-2 (human-readable), C-4 (no cloud) | UC-01, UC-06 |
| SRS-FR-07 | Score Aggregator | FR-01 | C-5 | UC-01 |
| SRS-FR-08 | Dashboard | FR-04, FR-05 | — | UC-02, UC-03 |
| SRS-FR-09 | Laporan PDF | FR-06 | — | UC-04 |
| NFR-01 | Kecepatan Inferensi <= 3 detik | NFR-01 | C-5 (WAJIB) | UC-01 |
| NFR-02 | Ukuran Model <= 50 MB | NFR-02 | C-6 (WAJIB) | — |
| NFR-03 | Kompatibilitas CPU-only | NFR-03 | C-5 | UC-01 |
| NFR-04 | Bahasa Python | NFR-04 | C-8 | — |
| NFR-05 | Reproducibility | NFR-05 | C-7 | UC-05 |
| NFR-06 | Offline / No Cloud | NFR-06 | C-4 (WAJIB) | UC-01 ~ UC-06 |

---

*Dokumen SRS ini merupakan spesifikasi teknis turunan dari PRD MATA RAKYAT v1.0. Digunakan sebagai panduan implementasi oleh Tim Qwerty pada Hackathon 2026.*
