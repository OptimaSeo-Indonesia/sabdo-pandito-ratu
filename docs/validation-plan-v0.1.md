# Rencana Validasi & Target Design Partner v0.1

**Status:** Draf
**Terakhir diperbarui:** 2026-07-22
**Tujuan:** Mendefinisikan siapa yang akan diajak bicara, apa yang ingin dipelajari, dan keputusan apa yang harus diinformasikan oleh setiap percakapan.

---

## 1. Hipotesis yang Diuji

| Segmen | Hipotesis | Sinyal kuat | Sinyal lemah | Invalidasi |
|--------|-----------|-------------|--------------|------------|
| **Tim AI di domain yang diatur** (fintech, healthtech, legaltech, AI enterprise internal) | Mereka membutuhkan representasi keputusan yang dapat diaudit, dan solusi saat ini bersifat ad-hoc dan mahal | Mereka menunjukkan format internal atau mendeskripsikan sistem tracing buatan sendiri | "Menarik" tetapi tidak ada tindakan konkret atau pekerjaan yang ada | "Kami tidak punya masalah ini" atau "Output LLM sudah cukup untuk kepatuhan" |
| **Pemelihara framework / orkestrasi** (LangGraph, CrewAI, AutoGen, dll.) | Mereka melihat nilai dari format pertukaran yang netral untuk jejak keputusan; pengguna mereka meminta traceability | "Ekspor/impor format standar akan berguna bagi pengguna kami" atau "Kami pernah mempertimbangkan membangun sesuatu seperti ini" | "Mungkin akan kami pakai suatu hari nanti" | "State internal kami sudah cukup; pengguna tidak butuh portabilitas" |
| **Peneliti evaluasi AI** (eval LLM, safety, alignment) | Mereka membutuhkan struktur yang konsisten untuk membandingkan penalaran lintas model dan konfigurasi | Mereka mengusulkan metrik atau kasus penggunaan yang selaras dengan data jejak deliberasi | Minat umum tanpa kasus penggunaan spesifik | "Benchmark yang ada sudah cukup" |
| **Praktisi tata kelola / jaminan** (kepatuhan, audit, risiko) | Mereka membutuhkan provenance dan jejak audit yang independen dari penyedia AI | Mereka mengoreksi atau memperkaya model kami — mis., "Anda kehilangan field X yang dibutuhkan regulator kami" | Pengakuan bahwa provenance itu penting | "Kami percaya pada pelaporan vendor yang ada" |

## 2. Komposisi Target (8 Percakapan)

| Tier | Deskripsi | Jumlah | Contoh |
|------|-----------|--------|--------|
| **Tier 1** | Pembangun perkakas — pemelihara framework, penulis alat evaluasi, penulis alat tata kelola | 3 | LangGraph maintainer, Arize AI / Braintrust, Guardrails AI |
| **Tier 2** | Pengguna nyata — tim yang membangun sistem keputusan AI berisiko tinggi | 3 | Fintech (keputusan kredit), healthtech (dukungan klinis), AI enterprise internal |
| **Tier 3** | Influencer teknis — peneliti dan insinyur yang sering menulis tentang evaluasi LLM, AI safety, tata kelola AI, provenance | 2 | Laboratorium eval LLM akademis, praktisi tata kelola AI |

## 3. Panduan Percakapan

### Pembukaan (JANGAN jelaskan Sabdo)

> "Kami sedang mencoba memahami bagaimana tim AI merepresentasikan dan mengaudit proses pengambilan keputusan mereka. Boleh kami belajar dari pengalaman Anda?"

### Pertanyaan kunci (sesuaikan per segmen)

1. **Penemuan:** Ceritakan bagaimana sistem Anda mencapai keputusan hari ini — dari input ke output. Apa yang terjadi di antaranya?
2. **Rasa sakit:** Apa bagian tersulit tentang menjelaskan atau mengaudit keputusan setelah dibuat?
3. **Solusi saat ini:** Bagaimana Anda merepresentasikan ini hari ini? (Cari format ad-hoc, solusi buatan sendiri)
4. **Biaya:** Apa yang rusak ketika Anda perlu melacak keputusan lintas model, framework, atau waktu?
5. **Kosakata:** Apa sebutan Anda untuk ini? "Jejak keputusan"? "Jejak audit"? "Provenans penalaran"? "Provenans keputusan"? Yang lain?
6. **Ambang:** Jika format standar ada untuk ini, apa yang perlu dicakup agar Anda mempertimbangkannya?

### Apa yang TIDAK boleh dikatakan

- ❌ "Protokol Sabdo adalah spesifikasi deliberasi terbuka..."
- ❌ "Kami memiliki implementasi referensi di Python..."
- ❌ "Model kami menggunakan Klaim → Bukti → HasilVerifikasi..."

### Apa yang harus dikatakan

- ✅ "Kami sedang menjajaki apakah ada kebutuhan untuk format bersama untuk jejak keputusan."
- ✅ "Apakah format seperti ini akan membantu dengan apa yang Anda bangun?"
- ✅ "Apa yang hilang dari gambaran ini?"

## 4. Keputusan yang Harus Diinformasikan Setiap Percakapan

| Tipe percakapan | Keputusan kunci | Pertanyaan untuk dijawab |
|-----------------|-----------------|--------------------------|
| **Pemelihara framework** | Format pertukaran vs spesifikasi runtime | Apakah spesifikasi perlu mendefinisikan bagaimana deliberasi berjalan, atau hanya bagaimana output direpresentasikan? |
| **Tim AI yang diatur** | Kelengkapan objek | Apakah Klaim, Bukti, dan HasilVerifikasi cukup untuk kebutuhan audit? Apa yang kurang? |
| **Peneliti evaluasi** | Lingkup Jejak Deliberasi | Apakah jejak lengkap (state langkah-demi-langkah) perlu ada di v0.1, atau ringkasan sudah cukup? |
| **Praktisi tata kelola** | Persyaratan kepatuhan | Field, jaminan, atau metadata apa yang diharapkan regulator? |

## 5. Organisasi Kandidat (Ilustratif, Bukan Preskriptif)

**Tier 1 (Pembangun perkakas):**
- LangGraph / LangChain — framework paling relevan; kemampuan ekspor
- Arize AI — observabilitas LLM; pahami kebutuhan format trace
- Guardrails AI / NVIDIA NeMo Guardrails — perspektif alat tata kelola
- Braintrust — evaluasi dan tracing LLM

**Tier 2 (Pengguna nyata):**
- Fintech: tim keputusan kredit di bank/fintech (mis., Affirm, Upstart, atau bank tradisional)
- Healthtech: dukungan keputusan klinis (mis., Ooda, Viz.ai, atau tim AI rumah sakit)
- Enterprise: tim platform AI internal di perusahaan yang diatur

**Tier 3 (Influencer):**
- Peneliti evaluasi LLM (lab akademis yang mengerjakan benchmark penalaran)
- Praktisi tata kelola AI (orang yang menulis tentang audit AI, responsible AI)

## 6. Kriteria Keberhasilan Fase Validasi

- [ ] 8 percakapan selesai dengan catatan yang terdokumentasi
- [ ] Setiap percakapan dikategorikan: sinyal kuat / sinyal lemah / invalidasi
- [ ] Kosakata dipetakan: istilah apa yang sebenarnya digunakan praktisi?
- [ ] 3 celah teratas dalam spesifikasi saat ini diidentifikasi dari umpan balik
- [ ] Keputusan go/no-go: lanjut ke revisi v0.1 atau pivot

## 7. Garis Waktu

| Minggu | Aktivitas |
|--------|-----------|
| 1 | Identifikasi + kontak 12 kandidat (harapkan 60% respons) |
| 2-3 | Lakukan 8 percakapan (2-3 per minggu) |
| 3 | Sintesis temuan, identifikasi celah spesifikasi |
| 4 | Keputusan go/no-go + revisi spesifikasi jika lanjut |
