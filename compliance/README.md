# Rangkaian Uji Kepatuhan Sabdo

Direktori ini berisi Rangkaian Uji Kepatuhan Sabdo untuk Spesifikasi Klaim v0.1.

## Cara Kerja

Uji kepatuhan **agnostik bahasa**. Ia menggunakan JSON sebagai format pertukaran:

1. Setiap pengujian mendefinisikan input JSON (klaim + bukti) dan output JSON yang diharapkan (hasil verifikasi)
2. Implementasi Anda membaca input, menjalankan verifikasi, dan menghasilkan output
3. Pelari uji membandingkan output Anda dengan output yang diharapkan

## Menjalankan Uji Kepatuhan

### Untuk implementasi referensi Python:

```bash
python compliance/runner.py
```

### Untuk implementasi Anda sendiri (bahasa apa pun):

1. Tulis skrip yang membaca `compliance/tests/test_001_input.json`
2. Menghasilkan `compliance/tests/test_001_output.json`
3. Jalankan `python compliance/runner.py --implementation ./skrip-anda` (segera hadir)

## Format Pengujian

Setiap kasus uji memiliki:

- `input.json` — berisi `claims` (array objek Klaim) dan `evidence` (array objek Bukti)
- `expected.json` — berisi `results` (array objek HasilVerifikasi dengan status yang diharapkan)

## Apa yang Diuji

| Tes | Deskripsi |
|-----|-----------|
| test_001 | Verifikasi dasar — klaim cocok dengan bukti melalui overlap kata kunci |
| test_002 | Tanpa bukti — semua klaim harus TIDAK DIDUKUNG |
| test_003 | Overlap rendah — klaim harus TIDAK PASTI |
| test_004 | Hasil campuran — beberapa terverifikasi, beberapa tidak pasti |
| test_005 | Daftar klaim kosong — harus menghasilkan hasil kosong |
