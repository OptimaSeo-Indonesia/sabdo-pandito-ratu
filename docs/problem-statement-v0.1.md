# Pernyataan Masalah v0.1

**Status:** Draf — akan divalidasi melalui percakapan dengan calon pengguna
**Terakhir diperbarui:** 2026-07-22

> **Pembaca yang dituju:** CTO, teknisi AI, dan pimpinan teknis yang membangun atau mengevaluasi sistem keputusan berbasis LLM.
>
> **Catatan tentang bahasa:** Dokumen ini menggunakan "jejak keputusan" (*decision trace*) sebagai istilah kerja. Melalui percakapan validasi, kami berharap mengetahui istilah yang sebenarnya dipakai oleh praktisi — apakah itu "jejak audit" (*audit trail*), "provenance keputusan" (*decision provenance*), "jejak penalaran" (*reasoning trace*), atau istilah lain. Istilah ini bersifat sementara.

---

## 1. Masalahnya

Setiap tim yang menerapkan sistem AI untuk keputusan dengan konsekuensi nyata pada akhirnya menghadapi tantangan yang sama:

- **"Mengapa AI merekomendasikan ini?"** — Jawabannya biasanya berupa paragraf teks, bukan rantai penalaran yang terstruktur dan dapat dilacak.
- **"Fakta apa yang digunakan?"** — Klaim dan bukti tercampur dalam respons teks bebas, sehingga tidak mungkin memisahkan pernyataan dari dukungannya.
- **"Bisakah kita memutar ulang dan memverifikasi keputusan ini?"** — Tidak ada format standar untuk mencatat apa yang dipertimbangkan AI, bukti apa yang mendukung setiap klaim, dan bagaimana konflik diselesaikan.
- **"Apakah ini bisa bertahan dalam audit?"** — Lingkungan yang diatur (kesehatan, keuangan, hukum) semakin menuntut explainability, tetapi tidak ada format yang interoperabel untuk menyediakannya.

Masalah ini menjadi semakin akut ketika sistem AI berpindah dari purwarupa ke produksi — terutama ketika keputusan perlu ditinjau, dijustifikasi, atau diaudit oleh pihak yang tidak membangun sistem tersebut.

## 2. Biaya Jika Tidak Diselesaikan

| Dimensi | Biaya |
|---------|-------|
| **Waktu engineering** | Setiap tim membangun format tracing ad-hoc mereka sendiri. Pekerjaan duplikatif di setiap organisasi yang menerapkan AI untuk keputusan. |
| **Biaya audit** | Tanpa format standar, audit membutuhkan review manual terhadap log teks bebas — mahal, lambat, dan rawan kesalahan. |
| **Vendor lock-in** | Fitur explainability terikat pada platform tertentu. Berganti penyedia AI berarti membangun ulang lapisan traceability. |
| **Evaluasi lintas model** | Membandingkan kualitas keputusan antar model atau framework berbeda membutuhkan normalisasi manual terhadap output yang tidak terstruktur. |
| **Skalabilitas tata kelola** | Proses tata kelola yang berjalan untuk 10 keputusan akan gagal pada 10.000 keputusan tanpa jejak yang terstandarisasi dan dapat dibaca mesin. |

## 3. Mengapa Pendekatan Saat Ini Tidak Memadai

| Pendekatan | Mengapa Tidak Cukup |
|------------|---------------------|
| **Penjelasan teks bebas** (`"Kami memilih X karena..."`) | Tidak dapat dibaca mesin; tidak bisa dibandingkan antar keputusan; tidak bisa diaudit secara terprogram |
| **Format JSON ad-hoc** (setiap tim membuat sendiri) | Setiap integrasi bersifat khusus; ekosistem perkakas tidak bisa muncul di atas N format yang tidak kompatibel; masing-masing memiliki semantik berbeda di balik field yang serupa |
| **Interpretabilitas khusus model** (attention maps, SHAP values, feature importance) | Terikat pada arsitektur tertentu; menangkap mekanisme model, bukan proses penalaran itu sendiri |
| **State internal framework agen** (LangGraph, CrewAI, AutoGen) | Setiap framework memiliki representasi sendiri; keputusan yang dimulai di LangGraph dan dievaluasi di layanan khusus tidak bisa dilacak ujung ke ujung karena tidak ada representasi bersama |
| **Mode output terstruktur LLM** (JSON mode, structured outputs) | Mendefinisikan *bentuk* output, bukan *proses deliberasi* yang menghasilkannya; mereka menjawab "apa" tetapi bukan "mengapa" |

Tidak satu pun dari ini menyelesaikan celah struktural inti: **tidak ada representasi bersama untuk apa yang dipertimbangkan sistem AI, bukti apa yang digunakannya, dan bagaimana ia mencapai kesimpulan** — representasi yang bekerja lintas bahasa, framework, dan model.

### Mengapa JSON Schema Tidak Cukup

JSON Schema mendefinisikan *struktur*: field apa yang ada, tipe-nya, batasannya. Itu perlu tetapi tidak cukup.

Sebuah spesifikasi mendefinisikan *semantik*: apa arti sebuah Klaim, bagaimana ia berbeda dari Bukti, apa yang diwakili oleh Hasil Verifikasi, jaminan apa yang diberikan oleh Catatan Provenans.

HTTP bukan sekadar format pesan — ia mendefinisikan method, status code, dan artinya. SQL bukan sekadar grammar — ia mendefinisikan relasi, transaksi, dan jaminan. Demikian pula, spesifikasi jejak keputusan harus mendefinisikan arti setiap objek, bukan hanya bentuknya.

Tanpa semantik bersama, dua sistem dapat menghasilkan JSON yang valid dengan struktur identik tetapi semantik yang tidak kompatibel.

## 4. Siapa yang Paling Merasakan Ini (Fokus Fase Validasi)

Untuk fase validasi awal, kami menargetkan **dua** segmen:

### Primer: Tim AI yang membangun sistem keputusan berisiko tinggi

Tim internal di perusahaan di mana keputusan AI memiliki konsekuensi nyata — perekrutan, kredit, underwriting asuransi, triase medis, kepatuhan. Mereka membutuhkan jejak audit bukan karena ingin membangun standar, tetapi karena fungsi legal/kepatuhan/risiko mereka menuntut explainability. Saat ini mereka membangun lapisan tracing khusus yang mahal untuk dirawat dan sulit diaudit.

### Sekunder: Pemelihara framework agen / orkestrasi

Tim yang membangun infrastruktur tempat aplikasi AI lain berjalan. Mereka mendengar dari pengguna: "Bagaimana cara melacak apa yang dilakukan agen saya?" dan "Bagaimana saya membuktikan keputusan ini masuk akal?" Format output standar akan memungkinkan mereka menawarkan traceability tanpa harus membangunnya sendiri.

Segmen lain (peneliti evaluasi LLM, pengadaan perusahaan, startup AI) ditunda sampai hipotesis utama tervalidasi.

## 5. Mengapa Protokol, Bukan Pustaka

| Pendekatan | Konsekuensi |
|------------|-------------|
| **Pustaka / SDK** | Hanya bekerja di satu bahasa; menciptakan ketergantungan; sulit bagi auditor independen untuk memverifikasi tanpa menggunakan pustaka yang sama |
| **Plugin framework** (plugin LangGraph, dll.) | Mengikat Anda pada framework tersebut; tidak menguntungkan pengguna framework lain |
| **Platform SaaS** | Memerlukan pengiriman data keputusan ke pihak ketiga; menciptakan vendor lock-in; mungkin melanggar kebijakan tata kelola data |
| **Protokol terbuka** (spesifikasi independen bahasa) | Siapa pun dapat mengimplementasikannya dalam bahasa apa pun; perkakas dapat dibangun secara independen; audit terlepas dari keputusan implementasi |

---

## Yang Sedang Kami Uji

Dokumen ini menyatakan sebuah hipotesis: bahwa ada masalah yang nyata dan mahal — sebuah celah antara bagaimana keputusan AI dibuat dan bagaimana keputusan itu dapat dilacak, diverifikasi, dan diaudit — dan bahwa representasi bersama (sebuah protokol, bukan produk) adalah tingkat solusi yang tepat.

Kami tidak menguji apakah orang menyukai Sabdo. Kami menguji apakah masalahnya nyata.

**Sinyal validasi kuat:** Seseorang berkata, "Kami sudah menyelesaikan ini sendiri" atau "Kami telah membangun format khusus untuk ini."

**Sinyal validasi lemah:** Seseorang berkata, "Menarik" — dan tidak ada yang berubah dalam cara mereka bekerja.

**Invalidasi:** Setelah 8 percakapan, tidak ada yang mengenali masalah tersebut sebagai sesuatu yang cukup mahal untuk diselesaikan.
