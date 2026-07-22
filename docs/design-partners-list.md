# Daftar Design Partner

**Tujuan:** Identifikasi siapa yang paling mampu menyangkal hipotesis kami — bukan siapa yang paling terkenal.
**Metode:** 3 gelombang kontak, bukan 8 kontak simultan.
**Aturan:** Setiap percakapan harus dapat mengubah keputusan nyata.

---

## Kerangka Prioritas

| Prioritas | Profil | Mengapa kritis |
|-----------|--------|----------------|
| **P1** | Pemelihara: framework agen / orkestrasi | Dapat menyangkal H3 (protokol > SDK) dan H4 (nilai lintas framework) |
| **P1** | Pemelihara: evaluasi / observabilitas AI | Dapat menyangkal H1 (masalah ada) dan H2 (model objek tepat) |
| **P1** | Tim AI di domain yang diatur | Dapat menyangkal H1 (masalah ada) dan H6 (komitmen design partner) |
| **P2** | Peneliti: tata kelola / provenance AI | Dapat menyangkal H5 (kesenjangan terminologi) dan H2 (kewajaran konseptual) |
| **P2** | Vendor platform AI | Dapat menyangkal H4 (nilai lintas framework) atau mengungkap hambatan bisnis |

---

## Kartu Design Partner

### P1.1 — Pemelihara LangChain / LangGraph

| Field | Isi |
|-------|------|
| **Mengapa dipilih** | LangGraph adalah framework orkestrasi paling relevan untuk pipa deliberasi. Jika mereka mengatakan "model state internal kami sudah cukup", H4 (nilai lintas framework) melemah. Jika mereka mengatakan "format pertukaran standar akan bermanfaat bagi pengguna kami", H3 dan H4 menguat. |
| **Hipotesis yang diuji** | H3 (protokol > SDK), H4 (nilai lintas framework), H6 (komitmen design partner) |
| **Pendekatan** | Buka GitHub Discussion di repo langgraph: "Apakah format jejak keputusan standar akan bermanfaat bagi pengguna LangGraph?" — uji minat sebelum kontak langsung |
| **Pertanyaan pra-percakapan** | "Jika mereka mengatakan 'kami sudah punya tracing via LangSmith', apakah itu menyangkal H3?" → Ya, itu menunjukkan nilai ada di platform, bukan protokol. |
| **Gelombang** | 1 |
| **Status** | Belum dikontak |

---

### P1.2 — Arize AI (observabilitas LLM)

| Field | Isi |
|-------|------|
| **Mengapa dipilih** | Arize sudah melacak panggilan LLM. Jika mereka mengatakan "format trace kami sudah mencakup provenance keputusan", H1 (masalah ada) melemah — masalah mungkin sudah terpecahkan. Jika mereka mengatakan "kami menangkap kinerja, bukan struktur penalaran", H1 menguat. |
| **Hipotesis yang diuji** | H1 (masalah ada), H2 (model objek tepat), H5 (terminologi) |
| **Pendekatan** | Teliti format tracing OpenInference mereka terlebih dahulu. Kemudian hubungi: "Kami sedang menjajaki apakah informasi jejak keputusan membutuhkan representasi standar. Tim Anda memiliki pengalaman mendalam di bidang ini — bersediakah Anda berbagi pelajaran?" |
| **Pertanyaan pra-percakapan** | "Jika mereka mengatakan 'kami sudah punya ini di OpenInference', apakah kita pivot ke integrasi atau menerima bahwa kita terlambat?" |
| **Gelombang** | 1 |
| **Status** | Belum dikontak |

---

### P1.3 — Braintrust (evaluasi LLM)

| Field | Isi |
|-------|------|
| **Mengapa dipilih** | Braintrust fokus pada pengembangan berbasis evaluasi. Jika mereka mengatakan "framework eval yang ada memungkinkan Anda membandingkan output dengan baik", nilai jejak keputusan standar untuk evaluasi melemah. Jika mereka mengatakan "mengevaluasi penalaran membutuhkan data terstruktur yang tidak kami miliki", H1 menguat. |
| **Hipotesis yang diuji** | H1 (masalah ada), H2 (model objek), H6 (komitmen design partner) |
| **Pendekatan** | "Kami sedang menjajaki apakah jejak keputusan terstruktur dapat meningkatkan evaluasi LLM. Bersediakah Anda untuk percakapan singkat tentang apa yang menjadi perjuangan tim evaluasi?" |
| **Pertanyaan pra-percakapan** | "Jika mereka mengatakan 'kami tidak butuh lebih banyak struktur; perbandingan output sudah cukup', apakah ini menyangkal nilai spesifikasi untuk kasus penggunaan evaluasi?" |
| **Gelombang** | 1 |
| **Status** | Belum dikontak |

---

### P2.1 — Tim AI Fintech (keputusan kredit)

| Field | Isi |
|-------|------|
| **Mengapa dipilih** | Keputusan kredit adalah aplikasi AI berisiko tinggi dengan pengawasan regulasi (ECOA, FCRA di AS). Jika mereka mengatakan "regulator menerima dokumentasi kami saat ini", H1 (masalah ada) mungkin berlebihan. Jika mereka mendeskripsikan proses internal yang menyakitkan untuk kepatuhan audit, H1 terkonfirmasi kuat. |
| **Hipotesis yang diuji** | H1 (masalah ada), H2 (model objek), H5 (terminologi) |
| **Pendekatan** | Identifikasi via LinkedIn atau blog post: insinyur yang menulis tentang "explainability AI di fintech" atau "kepatuhan machine learning." Hubungi: "Kami mempelajari bagaimana tim fintech menangani auditabilitas keputusan AI. Boleh kami belajar dari pengalaman Anda?" |
| **Pertanyaan pra-percakapan** | "Jika mereka mengatakan 'tim ML kami menangani audit dengan alat yang ada, tidak masalah', apakah kita menjatuhkan tesis pasar yang diatur?" |
| **Gelombang** | 2 |
| **Status** | Belum diidentifikasi |

---

### P2.2 — Tim AI Healthtech (dukungan keputusan klinis)

| Field | Isi |
|-------|------|
| **Mengapa dipilih** | AI klinis memiliki risiko tertinggi untuk explainability (hasil pasien, regulasi, tanggung jawab). Jika mereka mengatakan "klinisi hanya ingin prediksi, bukan jejak", hipotesis inti ditantang. Jika mereka mendeskripsikan persyaratan untuk provenance keputusan, itu validasi kuat. |
| **Hipotesis yang diuji** | H1 (masalah ada), H2 (model objek), H5 (terminologi) |
| **Pendekatan** | Sama seperti fintech: cari praktisi yang menulis tentang "explainability AI klinis" atau "pengajuan FDA untuk perangkat berbasis ML." |
| **Pertanyaan pra-percakapan** | "Jika mereka mengatakan 'regulator hanya peduli pada metrik validasi, bukan jejak keputusan', apakah waktu (H8) menjadi kendala pengikat?" |
| **Gelombang** | 2 |
| **Status** | Belum diidentifikasi |

---

### P2.3 — Peneliti tata kelola / keamanan AI

| Field | Isi |
|-------|------|
| **Mengapa dipilih** | Peneliti yang memikirkan transparansi AI dapat memvalidasi apakah pembingkaian masalah masuk akal secara konseptal, bahkan jika mereka tidak membangun sistem produksi. Mereka juga dapat memperkenalkan terminologi yang tepat (H5). |
| **Hipotesis yang diuji** | H5 (terminologi), H2 (kewajaran konseptual) |
| **Pendekatan** | Cari penulis makalah tentang "auditabilitas AI" atau "provenans keputusan." Hubungi: "Kami menyusun spesifikasi untuk jejak keputusan AI. Pekerjaan Anda tentang [judul makalah] tampaknya relevan — bersediakah Anda untuk review singkat?" |
| **Pertanyaan pra-percakapan** | "Jika mereka mengatakan 'ini sudah ada di [bidang]', apakah kita perlu melihat di luar AI untuk prior art?" |
| **Gelombang** | 3 |
| **Status** | Belum diidentifikasi |

---

### P2.4 — Pemelihara Guardrails AI / NVIDIA NeMo Guardrails

| Field | Isi |
|-------|------|
| **Mengapa dipilih** | Toolkit guardrails berdekatan dengan deliberasi — mereka mendefinisikan kebijakan dan batasan untuk output AI. Jika mereka mengatakan "kami sudah punya format untuk ini di definisi kebijakan kami", ruang mungkin sudah ditempati. Jika mereka mengatakan "guardrails output dan jejak keputusan menangani kebutuhan yang berbeda", ruang spesifikasi lebih jelas. |
| **Hipotesis yang diuji** | H4 (nilai lintas framework), H6 (komitmen design partner) |
| **Pendekatan** | Pemelihara open source — hubungi langsung via GitHub atau saluran komunitas. |
| **Pertanyaan pra-percakapan** | "Jika mereka mengatakan 'ini tumpang tindih dengan pekerjaan kami, mari berkolaborasi', apakah H6 (design partner) terpicu lebih awal dari yang diharapkan?" |
| **Gelombang** | 3 |
| **Status** | Belum dikontak |

---

## Rencana Gelombang

| Gelombang | Siapa | Tujuan | Garis Waktu |
|-----------|-------|--------|-------------|
| **1** (3 kontak) | LangChain, Arize, Braintrust | Cari kritik paling tajam. Uji hipotesis inti (H1-H4) terhadap orang yang sangat memahami ruang ini. | Minggu 1 |
| **2** (3 kontak) | Fintech AI, Healthtech AI, (ketiga TBD dari pembelajaran gelombang 1) | Uji hipotesis yang direvisi terhadap praktisi nyata. Validasi tingkat rasa sakit dan terminologi. | Minggu 2-3 |
| **3** (2-4 kontak) | Peneliti, Guardrails, plus prospek baru dari gelombang 1-2 | Cari komitmen design partner. Uji H6 dan jelajahi potensi implementasi. | Minggu 3-4 |

---

## Log Keputusan Per-Percakapan

Untuk setiap design partner, jawab SEBELUM percakapan:

| Partner | Jika mereka mengatakan... | Maka kami... |
|---------|--------------------------|--------------|
| LangChain | "Kami tidak butuh jejak lintas framework" | Hapus H4 dari value prop inti; reposisi sebagai peningkatan single-framework |
| Arize | "Format trace kami sudah mencakup ini" | Pivot dari "format baru" ke "lapisan penyelarasan/pemetaan antar format yang ada" |
| Braintrust | "Perbandingan output sudah cukup untuk eval" | Hapus kasus penggunaan evaluasi dari value prop spesifikasi |
| Fintech AI | "Regulator menerima proses kami saat ini" | Terima bahwa tesis pasar yang diatur lemah; jelajahi kasus penggunaan yang tidak diatur |
| Healthtech AI | "Klinisi menginginkan prediksi, bukan jejak" | Pertimbangkan kembali apakah jejak keputusan adalah produk yang bisa dijual atau lapisan dasar yang diperlukan |
| Peneliti | "Terminologi ini tidak konsisten dengan X" | Revisi narasi publik dan bahasa spesifikasi sesuai |
| Guardrails | "Ini tumpang tindih dengan definisi guardrail kami" | Jelajahi lapisan integrasi atau kolaborasi daripada bersaing |

---

## Dasbor Status

| # | Partner | Prioritas | Gelombang | Hipotesis | Status | Tindakan selanjutnya |
|---|---------|-----------|-----------|-----------|--------|----------------------|
| 1 | LangChain/LangGraph | P1 | 1 | H3, H4, H6 | Belum dikontak | Buka GitHub Discussion |
| 2 | Arize AI | P1 | 1 | H1, H2, H5 | Belum dikontak | Teliti OpenInference, lalu hubungi |
| 3 | Braintrust | P1 | 1 | H1, H2, H6 | Belum dikontak | Siapkan pesan penjangkauan |
| 4 | Tim AI Fintech | P2 | 2 | H1, H2, H5 | Belum diidentifikasi | Cari praktisi via LinkedIn |
| 5 | Tim AI Healthtech | P2 | 2 | H1, H2, H5 | Belum diidentifikasi | Cari praktisi via blog/makalah |
| 6 | Peneliti tata kelola AI | P2 | 3 | H5, H2 | Belum diidentifikasi | Cari penulis makalah relevan |
| 7 | Pemelihara Guardrails | P2 | 3 | H4, H6 | Belum dikontak | Teliti format saat ini |
