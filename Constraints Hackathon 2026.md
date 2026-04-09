**D** alam semangat tema "Adaptive Intelligence", setiap tim peserta
tidak hanya ditantang untuk membangun model AI yang akurat, tetapi
juga model yang mampu beradaptasi dengan spesifikasi teknis
lingkungan tertentu. Inilah inti dari Sealed Constraints, yaitu batasan
teknis rahasia yang baru diungkap saat Tahap 2 dimulai.


Kegagalan memenuhi seluruh constraint yang telah ditentukan akan
berdampak fatal pada penilaian. Constraint bersifat wajib
(mandatory), bukan opsional.


Setiap track memiliki constraint masing-masing yang mencerminkan
tantangan dunia nyata di domain tersebut. Baca dan pahami
constraint track Anda dengan seksama sebelum memulai
pengembangan model.


(.pt/.h5/dll), folder train_data, dan folder test_data secara
terpisah.
2. **Reproducibility:** Model boleh memanfaatkan GPU localhost

bawaan laptop peserta saat demo. Namun, model wajib tetap
dapat berjalan di lingkungan CPU-only dan memenuhi batas waktu
inferensi pada kondisi CPU (lihat C-A3). Juri memvalidasi
constraint kecepatan pada kondisi CPU, bukan GPU.
3. **Bahasa** **Kode:** Python adalah bahasa utama yang
direkomendasikan. Penggunaan bahasa lain untuk komponen
tertentu diperbolehkan dengan dokumentasi yang jelas.
4. **Larangan Cloud Inference:** Dilarang menggunakan API inferensi

cloud (OpenAI, Google AI, AWS, Azure AI, Hugging Face Inference
API, dll) sebagai komponen inti model. Pelanggaran ini
mengakibatkan diskualifikasi.
5. **Proposal Bab 3:** Setiap tim wajib mendedikasikan Bab 3 proposal

untuk menjelaskan secara rinci bagaimana model mereka
memenuhi setiap poin constraint track masing-masing. Bab ini
akan menjadi dasar penilaian kepatuhan constraint.


komputasi yang besar. Namun di dunia nyata, solusi AI sering harus
berjalan di perangkat dengan sumber daya sangat terbatas, seperti
drone, kamera edge, atau sensor IoT. Track ini menguji kemampuan
tim membangun model yang cerdas sekaligus ringan.



**Constraint:**



1. **Ukuran Model:** Bobot model final (file .pt / .h5 / .onnx) TIDAK

BOLEH melebihi 50 MB.
2. **Kompatibilitas Platform:** Model boleh memanfaatkan GPU

localhost bawaan laptop peserta saat demo. Namun, model wajib
tetap dapat berjalan di lingkungan CPU-only dan memenuhi batas
waktu inferensi pada kondisi CPU (lihat C-A3). Juri memvalidasi
constraint kecepatan pada kondisi CPU, bukan GPU.
3. **Kecepatan Inferensi:** Waktu inferensi per satu sampel input

(single inference) TIDAK BOLEH melebihi 3 detik pada mesin CPU
standar (minimum Intel Core i5 Gen 8 / setara). Pengukuran
dilakukan pada kondisi CPU tanpa akselerasi GPU.
4. **Framework:** Model wajib menggunakan salah satu framework



pipeline inferensi.


data yang diproses oleh sistem AI sering mengandung informasi
pribadi yang sangat sensitif. Model bahasa yang mengirimkan data ke
server eksternal, sekecil apapun, adalah risiko nyata. Track ini menguji
kemampuan tim membangun sistem NLP yang benar-benar berdaulat
dan sadar privasi.



**Constraint:**



1. **Ukuran Model:** Model bahasa (Language Model) yang digunakan

tidak boleh melebihi 4 Miliar parameter (≤ 4B params). Wajib
menggunakan Small Language Model (SLM) atau model yang telah
dioptimasi.
2. **Offline Total:** Seluruh inferensi wajib berjalan secara lokal

(localhost/offline). Dilarang mengirimkan data teks apapun ke
server atau API eksternal (termasuk OpenAI, Gemini, Claude API,
Hugging Face Inference API, dll) dalam pipeline utama.
3. **PII Filter Wajib:** Model wajib dilengkapi mekanisme deteksi dan

penyensoran Personally Identifiable Information (PII) secara
otomatis. Mekanisme ini wajib berjalan sebagai bagian dari
pipeline inferensi (inference.ipynb), bukan sebagai skrip terpisah
di luar pipeline.




keputusannya adalah model yang tidak bisa dipercaya, terutama
dalam pengambilan keputusan kritis seperti kredit, diagnosis, atau
kebijakan publik. Track ini menguji kemampuan tim membangun
sistem prediktif yang presisi sekaligus transparan dan dapat
dipertanggungjawabkan.



**Constraint:**



1. **Explainability Wajib:** Model WAJIB menyertakan mekanisme

explainability yang dapat menjelaskan faktor-faktor penting di
balik setiap prediksi. Implementasi minimal menggunakan salah
satu dari: SHAP, LIME, feature importance plot, atau metode
interpretabilitas lain yang dapat dipertanggungjawabkan secara
ilmiah.
2. **Output Penjelasan :** Sistem wajib menghasilkan output penjelasan

yang dapat dibaca manusia (human-readable explanation) untuk
setiap prediksi, bukan hanya angka probabilitas. Penjelasan
minimal menyebutkan 3 variabel teratas yang memengaruhi hasil
prediksi beserta arah pengaruhnya (positif/negatif).
3. **Anti-Black Box :** Penggunaan model yang sepenuhnya opaque

(black box) tanpa lapisan explainability apapun tidak memenuhi




