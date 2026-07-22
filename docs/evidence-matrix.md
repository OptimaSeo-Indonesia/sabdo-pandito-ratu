# Matriks Bukti

**Tujuan:** Melacak apa yang dipelajari dari percakapan dengan design partner. Setiap percakapan harus mengubah tingkat keyakinan pada setidaknya satu hipotesis.

**Aturan:** Bukti adalah kutipan dan observasi, bukan interpretasi. Opini masuk di kolom keyakinan, bukan kolom bukti.

**Penyelesaian:** Fase ini selesai ketika setiap hipotesis memiliki bukti yang cukup untuk diterima, direvisi, atau ditolak — terlepas dari jumlah percakapan.

---

## Bobot Bukti

| Bobot | Jenis sumber |
|-------|--------------|
| **3** | Menjalankan sistem keputusan AI di produksi, atau pemelihara framework yang relevan |
| **2** | Insinyur yang pernah membangun sistem serupa |
| **1** | Tertarik tetapi belum pernah menghadapi masalah secara langsung |

Pernyataan berbobot-3 memiliki bobot lebih besar dari tiga pernyataan berbobot-1.

---

## Hipotesis

### H1 — Masalah itu ada

| Field | Isi |
|-------|------|
| **Hipotesis** | Tim AI membutuhkan representasi standar untuk jejak keputusan yang dapat diaudit |
| **Mengapa penting** | Jika salah, Sabdo tidak punya alasan untuk eksis |
| **Ambang keputusan** | ≥5 dari 8 design partner mengonfirmasi mereka memiliki solusi internal atau menyatakan kebutuhan yang sama |
| **Apa yang akan mengubah arah** | Jika 6/8 mengatakan penjelasan teks bebas sudah cukup untuk kebutuhan mereka → pivot ke masalah yang berbeda |
| **Status** | Tidak diketahui |

| P# | Bobot | Bukti mendukung | Bukti menolak | Δ Keyakinan |
|----|-------|-----------------|---------------|-------------|
| | | | | |

---

### H2 — Model objek sudah tepat

| Field | Isi |
|-------|------|
| **Hipotesis** | Klaim, Bukti, dan HasilVerifikasi berada pada tingkat abstraksi yang tepat |
| **Mengapa penting** | Menentukan apakah spesifikasi v0.1 dapat digunakan |
| **Ambang keputusan** | Design partner dapat memetakan konsep ini ke sistem mereka tanpa kebingungan |
| **Apa yang akan mengubah arah** | Jika banyak partner menemukan Klaim terlalu abstrak atau Bukti terlalu sempit → revisi model atau persempit lingkup |
| **Status** | Tidak diketahui |

| P# | Bobot | Bukti mendukung | Bukti menolak | Δ Keyakinan |
|----|-------|-----------------|---------------|-------------|
| | | | | |

---

### H3 — Protokol > SDK

| Field | Isi |
|-------|------|
| **Hipotesis** | Nilai utama ada pada spesifikasi, bukan pustaka atau SDK |
| **Mengapa penting** | Menentukan arah proyek jangka panjang (spesifikasi vs perkakas) |
| **Ambang keputusan** | Design partner menyatakan minat pada interoperabilitas atau penggunaan lintas platform |
| **Apa yang akan mengubah arah** | Jika semua orang meminta pustaka dan tidak ada yang peduli pada spesifikasi → pivot ke pendekatan SDK-first |
| **Status** | Tidak diketahui |

| P# | Bobot | Bukti mendukung | Bukti menolak | Δ Keyakinan |
|----|-------|-----------------|---------------|-------------|
| | | | | |

---

### H4 — Nilai lintas framework

| Field | Isi |
|-------|------|
| **Hipotesis** | Ada nilai nyata dalam format interoperabel lintas framework dan model |
| **Mengapa penting** | Menguji apakah interoperabilitas adalah fitur atau value prop inti |
| **Ambang keputusan** | Design partner menggunakan atau mengantisipasi penggunaan beberapa model/framework dan melihat nilai dalam format bersama |
| **Apa yang akan mengubah arah** | Jika semua partner menggunakan satu stack dan tidak berencana diversifikasi → reposisi spesifikasi sebagai peningkatan single-framework, bukan standar lintas platform |
| **Status** | Tidak diketahui |

| P# | Bobot | Bukti mendukung | Bukti menolak | Δ Keyakinan |
|----|-------|-----------------|---------------|-------------|
| | | | | |

---

### H5 — Kesenjangan terminologi

| Field | Isi |
|-------|------|
| **Hipotesis** | Istilah yang digunakan praktisi berbeda dari kosakata internal Sabdo |
| **Mengapa penting** | Menentukan bahasa narasi publik |
| **Ambang keputusan** | Pola yang jelas muncul — jika ≥5/8 menggunakan istilah yang berbeda dari "deliberasi" |
| **Apa yang akan mengubah arah** | Jika istilah alternatif yang konsisten muncul (mis., "provenans keputusan"), kami mengadopsinya di semua dokumen publik |
| **Status** | Tidak diketahui |

| P# | Bobot | Bukti mendukung | Bukti menolak | Δ Keyakinan |
|----|-------|-----------------|---------------|-------------|
| | | | | |

---

### H6 — Komitmen design partner

| Field | Isi |
|-------|------|
| **Hipotesis** | Setidaknya satu pihak bersedia menjadi design partner berkelanjutan (mencoba, memberi umpan balik, atau mengimplementasi) |
| **Mengapa penting** | Mengukur apakah kita dapat bertransisi dari validasi ke kreasi bersama |
| **Ambang keputusan** | ≥1 partner mengatakan "ya" ke langkah konkret berikutnya (mencoba spesifikasi, mengimplementasi subset, mengintegrasi) |
| **Apa yang akan mengubah arah** | Jika semua percakapan berakhir di diskusi tanpa tindak lanjut → terima horizon lebih panjang; lanjutkan membangun spesifikasi di publik tetapi kurangi investasi |
| **Status** | Tidak diketahui |

| P# | Bobot | Bukti mendukung | Bukti menolak | Δ Keyakinan |
|----|-------|-----------------|---------------|-------------|
| | | | | |

---

## Log Percakapan

### Percakapan #1

| Field | Isi |
|-------|------|
| **Tanggal** | |
| **Nama / Peran** | |
| **Segmen** | Tier 1 / Tier 2 / Tier 3 |
| **Bobot** | 1 / 2 / 3 |
| **Konteks** | |
| **Solusi saat ini** | |
| **Kosakata yang digunakan** | |
| **Kutipan kunci** | |
| **Kejutan** | |
| **Tindak lanjut** | |

---

## Kemajuan Gerbang

| Gerbang | Status | Ambang | Kemajuan |
|---------|--------|--------|----------|
| Gate 1: Validasi Masalah | ❓ | ≥5/8 konfirmasi masalah (H1) + ≥2 dengan solusi internal + 0 invalidasi | |
| Gate 2: Validasi Spesifikasi | ❓ | H2 terkonfirmasi (tanpa kontradiksi) | |
| Gate 3: Validasi Ekosistem | ❓ | 1 implementasi atau integrasi independen | |
