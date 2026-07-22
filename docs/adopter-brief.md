# Sabdo: Ringkasan untuk Adopter

## Apa itu Sabdo?

Sabdo adalah **spesifikasi terbuka** untuk deliberasi dan verifikasi keputusan AI. Ia mendefinisikan format standar untuk merepresentasikan klaim, bukti, dan hasil verifikasi — sehingga sistem AI yang berbeda dapat memproduksi dan mengonsumsi jejak deliberasi dalam bahasa yang sama.

**Lingkup:** Sabdo hanya menentukan *format output* dari deliberasi. Ia tidak menentukan bagaimana deliberasi terjadi (LLM mana, framework mana, prompt mana).

## Format Inti (Draf v0.1)

### Klaim
```json
{
  "id": "c001",
  "text": "Tenaga surya mengurangi emisi karbon secara signifikan.",
  "source_advisor_id": "ra_001",
  "source_persona": "analis_rational",
  "confidence": 0.85,
  "extracted_entities": ["tenaga", "surya", "karbon", "emisi"],
  "parent_response_id": ""
}
```

### Bukti
```json
{
  "id": "e001",
  "text": "IEA 2025: Adopsi tenaga surya mengurangi emisi karbon sebesar 40%.",
  "source_ref": "Laporan IEA Renewables 2025",
  "source_type": "data_source",
  "provider": "ra_001",
  "timestamp": "2026-07-22T10:30:00Z"
}
```

### HasilVerifikasi
```json
{
  "claim_id": "c001",
  "status": "terverifikasi",
  "support_ratio": 0.5,
  "confidence": 0.48,
  "matched_evidence": ["Laporan IEA Renewables 2025"],
  "provenance": [
    {
      "claim_id": "c001",
      "evidence_id": "e001",
      "match_type": "kata_kunci",
      "match_score": 0.83,
      "verified_at": "2026-07-22T10:30:05Z"
    }
  ]
}
```

## Apa yang Dimungkinkan

- **Interoperabilitas:** Sistem AI mana pun dapat mengeluarkan klaim + bukti dalam format ini; alat mana pun dapat mengonsumsi dan memvisualisasikannya
- **Auditabilitas:** Lingkungan yang diatur dapat melacak setiap keputusan kembali ke klaim spesifik dan bukti pendukung
- **Komposabilitas:** Banyak penasihat dapat berkontribusi klaim, verifikator terpisah dapat mengevaluasinya, dan aggregator dapat menghasilkan vonis akhir

## Pertanyaan untuk Anda

1. **Kesesuaian format:** Apakah format Klaim/Bukti/Verifikasi ini cocok dengan alat yang Anda bangun? Jika tidak, apa yang kurang?

2. **Biaya integrasi:** Berapa banyak usaha yang diperlukan untuk mengeluarkan ketiga objek ini dari sistem Anda? Apa yang akan memudahkan integrasi?

3. **Fitur prioritas:** Apa satu hal yang Anda butuhkan sebelum mengadopsi standar seperti ini di produksi?

4. **Upaya serupa:** Apakah Anda mengetahui standar atau format lain di ruang ini yang harus kami selaraskan?

---

**Spesifikasi:** `docs/specs/claim-spec-v0.1.md` (terbuka, Apache 2.0)
**Implementasi referensi:** `examples/minimal_verification.py` (nol dependensi, 180 baris)
**Uji kepatuhan:** `compliance/runner.py` (JSON in/out, agnostik bahasa)
