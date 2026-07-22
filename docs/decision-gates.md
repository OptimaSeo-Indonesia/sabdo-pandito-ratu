# Gerbang Keputusan

**Status:** Draf — menggantikan peta jalan produk yang tetap dengan gerbang berbasis bukti
**Terakhir diperbarui:** 2026-07-22

---

Alih-alih peta jalan berbasis waktu, kemajuan Sabdo diatur oleh **gerbang keputusan**. Setiap gerbang mendefinisikan bukti yang diperlukan untuk melanjutkan. Tidak ada gerbang yang dilewati berdasarkan jadwal — hanya berdasarkan bukti.

```
    P3.5A (selesai)
         │
         ▼
     ┌──── GATE 1 ────┐
     │ Validasi       │
     │ Masalah        │
     └────────────────┘
         │ lulus / gagal → revisi / pivot
         ▼
     ┌──── GATE 2 ────┐
     │ Validasi       │
     │ Spesifikasi    │
     └────────────────┘
         │ lulus / gagal → revisi / pivot
         ▼
     ┌──── GATE 3 ────┐
     │ Validasi       │
     │ Ekosistem      │
     └────────────────┘
         │ lulus
         ▼
       v0.1
```

---

## Gate 1: Validasi Masalah

**Tujuan:** Memastikan bahwa masalah yang dijelaskan dalam Pernyataan Masalah adalah nyata, dikenali, dan cukup mahal.

**Metode:** 8 percakapan terstruktur dengan segmen target.

### Kriteria kelulusan

| # | Kriteria | Bukti |
|---|----------|-------|
| 1 | ≥5 dari 8 percakapan mengonfirmasi masalah ada di konteks mereka | Catatan percakapan dengan kutipan langsung |
| 2 | ≥2 percakapan menunjukkan solusi internal (format internal, tracing khusus, dll.) | Deskripsi pekerjaan internal yang ada |
| 3 | Tidak ada percakapan yang menginvalidasi hipotesis inti (mis., "kami tidak punya masalah ini") | Jika ≥2 mengatakan bukan masalah, gagal |

### Jika lulus

Lanjut ke Gate 2. Masukkan umpan balik kosakata dan pembingkaian ke dalam Pernyataan Masalah v0.2.

### Jika gagal (≥2 invalidasi)

Revisi Pernyataan Masalah. Mungkin masalah salah diidentifikasi, pembingkaian salah, atau segmen target tidak tepat. Lakukan percakapan tambahan dengan segmen berbeda.

### Tangkapan kosakata

Untuk setiap percakapan, catat:
- Istilah apa yang digunakan praktisi? ("jejak keputusan", "jejak audit", "provenans penalaran", "provenans keputusan", dll.)
- Apakah istilah bervariasi berdasarkan segmen atau peran?
- Perbarui bahasa Pernyataan Masalah dan Narasi Publik sesuai temuan.

---

## Gate 2: Validasi Spesifikasi

**Tujuan:** Memastikan bahwa model objek yang diusulkan (Klaim, Bukti, HasilVerifikasi) dapat dipahami, cukup lengkap, dan dapat diimplementasikan dari spesifikasi saja.

**Metode:** Sajikan spesifikasi (tanpa implementasi referensi) kepada subset peserta Gate 1 + audiens teknis baru.

### Kriteria kelulusan

| # | Kriteria | Bukti |
|---|----------|-------|
| 1 | ≥1 pihak mengatakan spesifikasi cukup jelas untuk dicoba implementasi | Pernyataan tertulis atau terekam |
| 2 | Tidak ada kontradiksi besar yang diidentifikasi dalam model Klaim/Bukti/HasilVerifikasi | Jika ≥2 peninjau independen menandai masalah yang sama, harus diselesaikan |
| 3 | Orang yang kompeten secara teknis dapat membaca spesifikasi dan menghasilkan output JSON yang benar untuk input tertentu | Uji kepatuhan lulus tanpa melihat implementasi referensi |

### Jika lulus

Lanjut ke Gate 3. Publikasikan v0.1-draft dengan spesifikasi yang direvisi.

### Jika gagal (kontradiksi model atau spesifikasi tidak dapat diimplementasikan)

Revisi spesifikasi. Tangani umpan balik spesifik. Uji ulang dengan peserta yang sama.

---

## Gate 3: Validasi Ekosistem

**Tujuan:** Memastikan bahwa spesifikasi dapat eksis secara independen dari implementasi referensi Python.

**Metode:** Cari satu implementasi independen dan/atau satu integrasi nyata.

### Kriteria kelulusan

| # | Kriteria | Bukti |
|---|----------|-------|
| 1 | Setidaknya satu implementasi independen ada (Go, Rust, TypeScript, atau bahasa apa pun selain Python). Tidak perlu siap produksi — purwarupa yang berfungsi dan lulus uji kepatuhan sudah cukup. | Repositori publik atau PR |
| 2 | ATAU: Setidaknya satu integrasi nyata — penggunaan format yang tidak sepele di proyek lain. | Integrasi yang terdokumentasi |
| 3 | Rangkaian uji kepatuhan lulus terhadap implementasi independen. | Output pengujian |

### Jika lulus

**v0.1 dideklarasikan.** Spesifikasi telah menunjukkan bahwa ia:
1. Dapat diimplementasikan dari spesifikasi saja
2. Cukup berharga sehingga orang lain bersedia berinvestasi

### Jika gagal (tidak ada implementasi independen atau integrasi setelah upaya yang wajar)

Publikasikan spesifikasi apa adanya. Terima bahwa spesifikasi mungkin lebih maju dari permintaan. Lanjutkan mencari dengan intensitas lebih rendah sambil mengerjakan fitur P3.5B yang meningkatkan utilitas spesifikasi.

---

## Apa yang Terjadi Setelah Gate 3

v0.1 bukanlah akhir. v0.1 adalah titik di mana spesifikasi cukup stabil untuk diandalkan orang lain.

Setelah v0.1:
- **P3.5B** dimulai (kalibrasi keyakinan, deteksi bias — ditunda dari P3.5A)
- Promosi spesifikasi dari Draf ke Eksperimental (membutuhkan implementasi eksternal)
- Pertumbuhan ekosistem: uji kepatuhan, perbaikan dokumentasi, contoh integrasi

Tetapi konten P3.5B dan seterusnya akan diinformasikan oleh apa yang diungkapkan percakapan Gate 1–3.

---

## Ringkasan

| Gerbang | Pertanyaan | Kriteria keluar |
|---------|------------|-----------------|
| 1 | Apakah masalahnya nyata? | 5/8 konfirmasi, 2 dengan solusi internal |
| 2 | Apakah spesifikasi dapat diimplementasikan? | 1 pihak mengatakan cukup jelas, tidak ada kontradiksi |
| 3 | Bisakah ia eksis secara independen? | 1 implementasi atau integrasi independen |

**Catatan:** Gerbang ini tidak memiliki tenggat waktu. Mereka memiliki persyaratan bukti. Proyek maju ketika bukti mencukupi, bukan ketika kalender mengatakan demikian.
