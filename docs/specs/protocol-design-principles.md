# Prinsip Desain Protokol Sabdo

**Status:** Stabil (prinsip panduan — tidak diharapkan sering berubah)
**Terakhir diperbarui:** 2026-07-22

---

## 1. Lingkup

Sabdo mendefinisikan spesifikasi untuk **deliberasi dan verifikasi** keputusan AI saja. Ia TIDAK mendefinisikan:

- Format prompt
- Sistem memori
- Pemanggilan perkakas (*tool calling*)
- Orkestrasi agen
- Perencanaan atau eksekusi
- Pelatihan atau penyesuaian model

**Alasan:** Sabdo berada di antara framework agen (yang menangani eksekusi) dan aplikasi (yang mengonsumsi keputusan). Dengan lingkup yang sempit, Sabdo menghindari persaingan dengan standar yang ada dan memaksimalkan interoperabilitas.

---

## 2. Model Stabilitas Objek

Setiap objek dalam spesifikasi Sabdo memiliki tingkat stabilitas:

| Tingkat | Arti | Kompatibilitas mundur |
|---------|------|-----------------------|
| **Draf** | Desain awal, aktif berubah | Tanpa jaminan |
| **Eksperimental** | Cukup stabil untuk prototipe, tetapi mungkin berubah | Perubahan besar dengan panduan migrasi |
| **Stabil** | Siap produksi | Kompatibel mundur dalam versi mayor yang sama |
| **Usang** | Digantikan oleh versi yang lebih baru | Dihapus di versi mayor berikutnya |

**Status saat ini semua objek:**

| Objek | Status | Sejak |
|-------|--------|-------|
| Klaim | Draf | v0.1 |
| Bukti | Draf | v0.1 |
| CatatanProvenans | Draf | v0.1 |
| HasilVerifikasi | Draf | v0.1 |
| StatusVerifikasi | Draf | v0.1 |
| Kontradiksi | Draf | v0.1 |

---

## 3. Apa yang Bisa Berubah dan Apa yang Harus Stabil

### Bisa berubah di Draf:
- Nama dan tipe field (dengan panduan migrasi jika dipromosikan ke Eksperimental)
- Nilai enum
- Detail algoritma dalam implementasi referensi

### Harus stabil setelah dipromosikan ke Eksperimental:
- Identitas objek (apa itu Klaim vs apa itu BUKAN Klaim)
- Field wajib vs opsional
- Format serialisasi JSON
- Ruang nilai enum (dapat menambahkan nilai baru, tidak pernah menghapus)

### Harus stabil setelah dipromosikan ke Stabil:
- Semua nama dan tipe field
- Semua field wajib
- Format serialisasi JSON
- Semua nilai enum yang ada

---

## 4. Versi

Spesifikasi Sabdo mengikuti **Semantic Versioning 2.0**:

- **Versi mayor** (mis., v1.0 → v2.0): Perubahan besar pada objek Stabil
- **Versi minor** (mis., v1.0 → v1.1): Objek baru atau field opsional ditambahkan
- **Versi patch** (mis., v1.0 → v1.1): Klarifikasi, koreksi, perubahan non-semantik

Pengidentifikasi pra-rilis: `v0.1-draf`, `v0.2-eksperimental`, `v1.0`

---

## 5. Menambahkan Field Baru

Field baru dapat ditambahkan ke objek mana pun di tingkat stabilitas mana pun, selama:

1. Field tersebut **opsional** (memiliki nilai default yang masuk akal atau null)
2. Field tersebut tidak mengubah arti field yang ada
3. Field tersebut memiliki spesifikasi yang jelas dan contoh serialisasi JSON

**Alasan:** Kompatibilitas maju — produsen yang lebih baru dapat menambahkan field tanpa merusak konsumen yang lebih lama yang mengabaikan field yang tidak dikenal.

---

## 6. Mengapa Objek Dipisahkan

| Pemisahan | Alasan |
|-----------|--------|
| **Klaim ≠ Bukti** | Klaim adalah pernyataan; Bukti adalah informasi pendukung. Mereka memiliki siklus hidup berbeda: klaim berasal dari penasihat, bukti berasal dari sumber data. |
| **Klaim ≠ Argumen** | Klaim adalah pernyataan atom tunggal. Argumen (spesifikasi masa depan) mengelompokkan banyak klaim dengan penalaran. Pemisahan memungkinkan klaim diverifikasi secara individual. |
| **HasilVerifikasi ≠ Klaim** | HasilVerifikasi adalah metadata tentang klaim, bukan klaim itu sendiri. Menjaga mereka tetap terpisah memungkinkan klaim ada tanpa verifikasi, dan sebaliknya. |
| **CatatanProvenans ≠ HasilVerifikasi** | Provenans adalah tautan antara klaim dan bukti pendukung. HasilVerifikasi berisi banyak catatan provenans ditambah metrik agregat. |

---

## 7. Aturan Serialisasi

1. Semua objek HARUS dapat diserialisasi ke JSON
2. Nama field HARUS dalam `snake_case`
3. Nilai enum HARUS berupa string
4. UUID HARUS diformat sebagai string (`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)
5. Datetime HARUS ISO 8601 UTC (`2026-07-22T10:30:00Z`)
6. Field yang tidak dikenal HARUS dipertahankan (konsumen tidak boleh menghapus field yang tidak dikenal saat baca-tulis)

---

## 8. Kepatuhan

Sebuah implementasi **patuh** terhadap versi spesifikasi jika:

1. Ia dapat memproduksi dan mengonsumsi semua objek yang didefinisikan dalam spesifikasi
2. Semua tipe dan batasan field dihormati
3. Serialisasi JSON cocok persis dengan spesifikasi
4. Ia lulus Rangkaian Uji Kepatuhan Sabdo untuk versi spesifikasi tersebut

Kepatuhan diuji melalui antarmuka **JSON-only** — rangkaian uji mengirim input JSON dan mengharapkan output JSON. Ini memastikan bahasa apa pun dapat diuji tanpa terikat pada runtime Python.

---

## 9. Ekstensibilitas

Implementasi BOLEH:
- Menambahkan field khusus implementasi (akan dipertahankan tetapi diabaikan oleh konsumen yang patuh)
- Menambahkan method pembantu yang bukan bagian dari spesifikasi
- Mengoptimalkan representasi internal selama serialisasi cocok dengan spesifikasi

Implementasi TIDAK BOLEH:
- Mengubah semantik field yang ditentukan
- Menghapus field wajib
- Mengubah format serialisasi JSON
- Menambahkan field wajib baru tanpa perubahan spesifikasi

---

## 10. Proses Evolusi

1. **Usulan** — Objek atau field baru diusulkan sebagai Draf
2. **Implementasi** — Runtime referensi mengimplementasikannya
3. **Pengujian** — Uji kepatuhan ditulis
4. **Review** — Setidaknya dua implementor independen mereview
5. **Promosi** — Draf → Eksperimental (setelah 1 implementasi eksternal)
6. **Stabilisasi** — Eksperimental → Stabil (setelah 3+ bulan penggunaan lapangan)

Proses ini memastikan tidak ada objek yang menjadi Stabil tanpa validasi dunia nyata.
