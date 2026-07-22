# Pre-mortem: Mengapa Sabdo Gagal Mendapatkan Adopter

Bayangkan 6 minggu dari sekarang. 8 percakapan selesai. Tidak ada satu pun design partner yang berkomitmen.

**Mengapa?**

---

## 10 Alasan Paling Mungkin

| # | Alasan | Cara menguji (percakapan mana) |
|---|--------|----------------------------------|
| 1 | **Masalah tidak cukup menyakitkan.** Tim AI punya solusi sementara yang "cukup baik" — penjelasan teks bebas, scraping log — dan tidak merasa perlu standar. Biaya solusi saat ini < biaya adopsi. | Tier 2: tanya "Apa bagian paling menyakitkan dari proses pengambilan keputusan kalau harus diaudit?" Kalau jawabannya "tidak terlalu", ini penyebabnya. |
| 2 | **Istilah tidak nyambung.** "Deliberasi", "Klaim", "Provenans" adalah jargon internal. Pengguna mencari "jejak audit", "log keputusan", "jejak penalaran" — bukan deliberasi. | Semua tier: catat kata persis yang mereka pakai. Kalau 5/8 tidak pernah menyebut deliberasi, ini masalah. |
| 3 | **Lingkup terlalu besar.** Spesifikasi mencakup terlalu banyak objek. Orang ingin satu format JSON kecil untuk logging, bukan seluruh kerangka deliberasi. | Tier 1 (framework): tanya "Kalau hanya Klaim + Bukti + HasilVerifikasi, cukup?" Kalau mereka bilang "< 5 objek baru menarik", lingkup perlu dikecilkan. |
| 4 | **Orang ingin SDK, bukan protokol.** Pengembang ingin `pip install` dan langsung jalan. Protokol tanpa implementasi bahasa mereka = beban. | Tier 1: tanya "Apa yang lebih membantu — spesifikasi atau pustaka di bahasa Anda?" Kalau semua pilih pustaka, value prop protokol belum jelas. |
| 5 | **Setuju masalahnya ada, tapi tidak mau standar baru.** "Kami sudah punya format internal. Kenapa migrasi?" Biaya perpindahan > manfaat interoperabilitas yang belum terbukti. | Semua tier: tanya "Apa yang bisa membuat format internal Anda layak diganti?" Kalau jawabannya "tidak ada", ini masalah. |
| 6 | **Solusi internal sudah cukup matang.** Tim sudah investasi 6+ bulan di format tracing sendiri. Migrasi ke Sabdo berarti tulis ulang. | Tier 2: tanya "Ceritakan format yang kalian bangun. Apa yang kalian suka dan tidak suka?" Kalau mostly suka, adopsi berat. |
| 7 | **Nilai interoperabilitas tidak terasa.** "Kami cuma pakai satu framework + satu penyedia LLM. Interoperabilitas buat apa?" Chicken-and-egg: interoperabilitas berharga kalau ada ekosistem, ekosistem butuh adopter. | Tier 1: tanya "Apakah kalian pernah perlu melacak keputusan yang melintasi beberapa framework?" Kalau tidak pernah, ini masalah. |
| 8 | **Biaya adopsi > manfaat.** Memahami spesifikasi, implementasi, pengujian — butuh waktu. Tim sibuk tidak punya bandwidth untuk eksperimen. | Semua tier: tanya "Berapa jam kira-kira yang diperlukan untuk mencoba format ini?" Kalau > 8 jam, terlalu mahal. |
| 9 | **Klaim/Bukti terlalu abstrak.** Sulit dipetakan ke implementasi nyata. "Klaim di sistem saya apa? Satu panggilan LLM? Satu respons? Satu langkah penalaran?" | Tier 1 + 2: minta mereka petakan satu keputusan dari sistem mereka ke Klaim/Bukti. Kalau bingung, model terlalu abstrak. |
| 10 | **Waktu pasar belum tepat.** Pasar AI keputusan masih terlalu awal. Tim fokus pada "bikin jalan" bukan "bikin bisa diaudit." Permintaan auditability belum cukup kuat. | Tier 2: tanya "Apakah ada tekanan dari regulator/manajemen untuk explainability?" Kalau tidak ada, waktu belum tepat. |

---

## Pemetaan Percakapan → Alasan

Setiap percakapan harus menguji beberapa alasan sekaligus:

| Tipe percakapan | Alasan utama untuk diuji | Alasan sekunder |
|-----------------|--------------------------|-----------------|
| Tier 1: Pemelihara framework | 3 (lingkup), 4 (SDK vs protokol), 7 (nilai interoperabilitas) | 2 (terminologi), 9 (abstraksi) |
| Tier 2: Tim AI yang diatur | 1 (tingkat sakit), 6 (solusi existing), 10 (waktu pasar) | 5 (standar baru), 8 (biaya adopsi) |
| Tier 3: Peneliti/praktisi | 2 (terminologi), 9 (abstraksi), 5 (standar baru) | 7 (interoperabilitas), 10 (waktu) |

---

## Apa Arti "Kegagalan"

| Hasil | Interpretasi |
|-------|--------------|
| **Alasan 1+4+7 terkonfirmasi** | Pembingkaian masalah salah. Pivot ke masalah berbeda atau format berbeda (SDK-first). |
| **Alasan 2+3 terkonfirmasi** | Masalah bahasa/lingkup spesifikasi. Perbaiki terminologi dan/atau persempit lingkup. |
| **Alasan 5+6 terkonfirmasi** | Masalah waktu pasar produk. Lanjutkan membangun tetapi terima horizon lebih panjang. |
| **Alasan 8+9+10 terkonfirmasi** | Masalah desain spesifikasi. Perbaiki implementabilitas dan tingkat abstraksi. |

---

## Pertanyaan Pemicu untuk Setiap Alasan dalam Percakapan

| # | Jika Anda ingin menguji ini, tanyakan... |
|---|------------------------------------------|
| 1 | "Ceritakan kapan terakhir kali Anda harus menjelaskan keputusan AI ke pihak luar." |
| 2 | "Apa istilah yang kalian pakai untuk hasil proses pengambilan keputusan?" |
| 3 | "Kalau format ini cuma mencakup klaim, bukti, dan verifikasi — cukup untuk apa yang kalian butuhkan?" |
| 4 | "Apa yang lebih berguna untuk tim Anda — spesifikasi atau pustaka siap pakai?" |
| 5 | "Apa yang harus dimiliki format baru agar kalian bersedia migrasi?" |
| 6 | "Ceritakan solusi yang sudah kalian bangun. Apa yang membuat kalian puas?" |
| 7 | "Apakah kalian pernah perlu melacak keputusan yang melibatkan lebih dari satu framework?" |
| 8 | "Berapa jam estimasi untuk integrasi awal?" |
| 9 | "Coba petakan satu keputusan dari sistem Anda ke format ini." |
| 10 | "Seberapa besar tekanan dari regulator atau manajemen untuk explainability?" |
