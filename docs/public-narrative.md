# Protokol untuk Jejak Keputusan AI

**Status:** Draf — mencari validasi, bukan mengklaim sebagai standar
**Terakhir diperbarui:** 2026-07-22

> Dokumen ini menyatakan sebuah hipotesis. Kami sedang menguji apakah representasi bersama untuk pengambilan keputusan AI diperlukan, apakah objek yang kami usulkan adalah yang tepat, dan apakah masalahnya cukup mahal untuk mendorong adopsi. Kami berharap sebagian dari ini salah.

---

## 1. Lapisan yang Hilang

Ekosistem AI memiliki standar untuk banyak hal:

| Lapisan | Standar |
|---------|---------|
| Arsitektur model | ONNX, Safetensors |
| Antarmuka API | Format OpenAI API, Anthropic Messages API |
| Pemanggilan perkakas | Skema tool use, MCP (Model Context Protocol) |
| Observabilitas | OpenTelemetry traces, LangSmith, Arize |
| Format output | JSON mode, Structured Outputs |

Tetapi **tidak ada representasi bersama untuk proses pengambilan keputusan itu sendiri** — untuk apa yang dipertimbangkan AI, bukti apa yang digunakannya, bagaimana ia menyelesaikan konflik, dan bagaimana ia mencapai kesimpulan.

Ini berarti setiap tim yang membangun sistem keputusan AI menemukan kembali hal yang sama: format ad-hoc untuk mencatat apa yang terjadi di dalam pipa mereka. Format ini tidak kompatibel antar tim, framework, dan model. Tidak ada ekosistem perkakas yang bisa muncul di atas N format yang tidak kompatibel.

Kami mengajukan hipotesis bahwa **representasi semantik bersama** untuk jejak keputusan — apa itu klaim, apa itu bukti, apa arti hasil verifikasi — akan membuka interoperabilitas, auditabilitas, dan perkakas independen yang tidak dapat diberikan oleh framework atau vendor mana pun sendirian.

## 2. Mengapa Format yang Ada Tidak Cukup

Setiap pendekatan yang ada memecahkan satu masalah tetapi meninggalkan celah inti tidak tersentuh.

| Pendekatan | Yang dipecahkan | Yang tidak dipecahkan |
|------------|----------------|----------------------|
| **JSON Schema** | Mendefinisikan struktur data yang valid | Tidak mendefinisikan apa arti data tersebut. Dua sistem dapat menghasilkan JSON identik dengan semantik yang tidak kompatibel. |
| **Structured Outputs / JSON mode** | Menjamin LLM merespons dalam format tertentu | Hanya menjamin format — bukan bahwa respons berisi proses keputusan yang dapat dilacak. Menjawab "apa" tetapi bukan "mengapa". |
| **State internal framework agen** (LangGraph, CrewAI, AutoGen) | Menyimpan state eksekusi dalam satu framework | State bersifat spesifik framework. Keputusan yang dimulai di LangGraph, melewati layanan khusus, dan berakhir di laporan tidak dapat dilacak ujung ke ujung. |
| **Perkakas observabilitas LLM** (LangSmith, Arize, Braintrust) | Melacak latensi, token, dan panggilan LLM | Melacak *kinerja*, bukan *struktur penalaran*. Mereka menjawab "seberapa cepat" dan "berapa banyak token", bukan "bukti apa yang digunakan". |
| **MCP (Model Context Protocol)** | Membakukan cara perkakas diekspos ke model | Mendefinisikan antarmuka perkakas, bukan apa yang diputuskan model atau mengapa. |

Pola yang sama: setiap perkakas memecahkan satu bagian dari teka-teki infrastruktur, tetapi **tidak ada yang mendefinisikan representasi untuk keputusan itu sendiri**.

## 3. Apa yang Harus Distandarisasi

Kami mengusulkan bahwa standar jejak keputusan minimal membutuhkan objek-objek ini:

| Objek | Tujuan | Analogi |
|-------|--------|---------|
| **Klaim** | Pernyataan atom yang dibuat AI selama deliberasi | Pernyataan saksi |
| **Bukti** | Informasi pendukung untuk sebuah klaim | Referensi dokumen atau titik data |
| **HasilVerifikasi** | Apakah klaim didukung, tidak didukung, atau kontradiktif | Vonis pemeriksaan fakta |
| **CatatanProvenans** | Tautan antara klaim dan bukti tertentu | Kutipan |
| **StatusVerifikasi** | Status verifikasi (terverifikasi / tidak didukung / kontradiktif / tidak pasti) | Lampu lalu lintas untuk klaim |

Kelima objek ini cukup untuk merepresentasikan inti dari setiap proses keputusan AI: apa yang diklaim, apa yang mendukungnya, dan apakah dukungan itu valid.

**Kandidat masa depan** (belum dispesifikasikan):
- **JejakDeliberasi** — catatan langkah-demi-langkah bagaimana keputusan berkembang *(nama sementara — istilah pasti akan ditentukan dari percakapan dengan praktisi)*
- **Keyakinan** — skor keyakinan yang terkalibrasi di tingkat klaim dan keputusan
- **Kontradiksi** — konflik berpasangan antar klaim

Kami sengaja menunda ini agar v0.1 tetap cukup kecil untuk divalidasi.

## 4. Apa yang TIDAK Boleh Distandarisasi

Sebuah spesifikasi didefinisikan sama banyak oleh apa yang tidak dicakupnya seperti oleh apa yang dicakupnya.

| TIDAK distandarisasi | Alasan |
|---------------------|--------|
| **Format prompt** | Prompt bersifat spesifik implementasi. Proses keputusan yang sama dapat diprompt dengan banyak cara. |
| **Pilihan model** | Spesifikasi agnostik model. Klaim/Bukti/Verifikasi harus berfungsi baik modelnya GPT-4o, Claude, Llama, atau sistem berbasis aturan. |
| **Arsitektur agen** | Apakah sistem menggunakan satu panggilan LLM atau graf 20 node tidak relevan terhadap representasi output. |
| **Implementasi memori** | Bagaimana sistem menyimpan keputusan masa lalu (vektor DB, SQL, file) adalah detail implementasi. |
| **Orkestrasi** | Pemanggilan perkakas, perencanaan, eksekusi — ini urusan framework agen, bukan spesifikasi jejak keputusan. |

Kami berhipotesis bahwa pembatasan lingkup yang sempit — hanya jejak keputusan — memaksimalkan kemungkinan adopsi. Sistem yang sudah menggunakan LangGraph untuk orkestrasi harus dapat mengeluarkan jejak berformat Sabdo tanpa mengubah logika orkestrasinya. Sistem yang tidak menggunakan framework sama sekali harus sama mampu.

## 5. Mengapa Spesifikasi Terbuka

| Alasan | Penjelasan |
|--------|------------|
| **Interoperabilitas** | Perkakas dari ekosistem berbeda dapat memahami jejak keputusan satu sama lain |
| **Auditabilitas** | Regulator dan tim kepatuhan dapat memeriksa keputusan tanpa terikat pada vendor tertentu |
| **Netralitas vendor** | Tidak ada perusahaan tunggal yang mengontrol format; berganti penyedia AI tidak berarti membangun ulang traceability |
| **Perkakas independen** | Alat visualisasi, verifikasi, dan audit dapat dibangun oleh siapa pun yang mengimplementasikan spesifikasi |
| **Masa depan** | Standar memisahkan representasi keputusan dari arsitektur model — LLM hari ini, apa pun yang datang berikutnya |

## 6. Status Saat Ini

Ini adalah **spesifikasi draf** — kami sedang menguji apakah masalahnya nyata dan apakah pendekatan ini adalah yang tepat.

| Status | Arti |
|--------|------|
| **Kami memiliki** | Pernyataan masalah, model objek yang diusulkan, implementasi referensi, dan rangkaian uji kepatuhan yang agnostik bahasa |
| **Kami mencari** | 8 percakapan dengan praktisi untuk memvalidasi atau menginvalidasi hipotesis kami |
| **Kami belum tahu** | Apakah "jejak keputusan" adalah istilah yang tepat, apakah model objek sudah lengkap, apakah masalahnya cukup mahal untuk mendorong adopsi |
| **Kami butuh** | Implementasi independen dalam bahasa lain (Go, Rust, TypeScript) untuk memastikan spesifikasi dapat diimplementasikan dari spesifikasi saja |

Jika Anda membangun perkakas untuk keputusan AI, evaluasi LLM, atau tata kelola AI — kami ingin mendengar dari Anda. Bukan tentang Sabdo, tetapi tentang pengalaman Anda dengan masalah ini.

**Kontak:** Buka issue atau mulai diskusi di repositori.
