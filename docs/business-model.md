# Sabdo Pandito Ratu — Business Model Canvas

**Identity:** Open Deliberation Specification with reference runtime (Linux + Red Hat model)

---

## 0. The Flywheel

```
Runtime gratis (Apache 2.0)
        ↓
Developer mencoba → deliberation traces
        ↓
Benchmark & knowledge bertambah
        ↓
Specification makin matang (Claim → Trace → WisdomScore)
        ↓
Lebih banyak implementasi (langsung + pihak ketiga)
        ↓
Nilai sertifikasi & compliance meningkat
        ↓
Pendapatan (certification + consulting + enterprise)
        ↓
Investasi kembali ke specification & community
        ↓
(kembali ke atas — loop)
```

**Prinsip:** Pendapatan harus mempercepat flywheel, bukan mengalihkan perhatian darinya. Setiap revenue stream harus bisa diuji dengan: *"Apakah ini membuat spesifikasi lebih diadopsi atau tidak?"*

**Metrik utama (tahap awal):**
> Apakah ada satu proyek di luar organisasi kita yang memilih mengimplementasikan Sabdo Specification karena mereka merasa itu menyelesaikan masalah mereka?

Bukan MRR. Bukan ARR. Tapi **adopsi eksternal** — karena itu satu-satunya yang menggerakkan flywheel.

---

## 1. Customer Segments

| Segment | Description | Willingness to pay | Priority |
|---------|-------------|-------------------|----------|
| **Tool builders** | Framework AI (LangGraph, CrewAI, AutoGen), evaluation tools, governance platforms | Low (mereka open source) | **Anchor** (adoption) |
| **AI application builders** | Perusahaan yang build di atas LLM, butuh audit trail + multi-model portability | Medium | **High** (revenue) |
| **Enterprise regulated** | Bank, RS, pemerintah yang butuh compliance + audit | High | **High** (revenue) |
| **AI vendors** | OpenAI, Anthropic, Google, DeepSeek | Low (mereka punya format sendiri) | Late follower |

---

## 2. Value Propositions

| Segment | Value |
|---------|-------|
| Tool builders | Standard protocol untuk deliberation data — interoperabilitas antar tool |
| AI app builders | Auditable decisions, ganti model kapan saja tanpa ubah sistem |
| Enterprise regulated | Trust: certification "Sabdo Verified", compliance-ready audit trail |
| AI vendors | Ecosystem compatibility — "Supports Sabdo Protocol" sebagai badge |

---

## 3. Channels

| Channel | Purpose |
|---------|---------|
| GitHub (`sabdo/specification`) | Community adoption, spec distribution |
| GitHub (`sabdo/runtime-python`) | Reference implementation, developer onboarding |
| Conference talks (KubeCon, FAccT, NeurIPS) | Thought leadership, recruitment |
| Academic papers (P4 output) | Credibility, research validation |
| Direct enterprise sales | Revenue (high-touch) |
| Partnership dengan agent frameworks | Distribution via integration |

---

## 4. Customer Relationships

| Segment | Model | Cost |
|---------|-------|------|
| Tool builders | **Community** — open source, free | Low (self-serve) |
| AI app builders | **Self-serve** — docs, examples, SDK | Low |
| Enterprise regulated | **High-touch** — sales, support, certification | High margin |

---

## 5. Revenue Streams

| Stream | Description | Model | Timeline |
|--------|-------------|-------|----------|
| **AI Decision Assessment** (replaces "Benchmark Service") | Diagnosis: "AI Anda memberikan jawaban inkonsisten? Kami analisis deliberation quality-nya pakai Sabdo framework." | Project-based | P4 selesai |
| **Compatibility Review** (early compliance) | Tinjau implementasi deliberation engine klien, beri laporan kompatibilitas terhadap Sabdo Specification | Project-based | Bisa mulai sebelum P5 |
| **Sabdo Verified certification** | Badge resmi + compliance test pass | Annual fee per org | P5 selesai |
| **Enterprise deployment pack** | RBAC, audit log, SSO, support SLA | Annual subscription | P5 selesai |
| **Training & workshops** | Deliberation governance implementation | Per-session | P4 selesai |
| **Trademark licensing** | "Sabdo Protocol compatible" untuk commercial use | Royalty | Setelah standar mapan |

**Revenue stream pertama & paling cepat:** Bukan benchmark — tapi **AI Decision Assessment**. Benchmark ada di belakang layar. Yang dijual adalah diagnosis dan kejelasan. Bisa dimulai sebagai jasa konsultasi sebelum P4 fully built.

**Yang dimaksud bukan hanya "menjual hasil spesifikasi", melainkan dokumentasi itu sendiri adalah produk.** Spesifikasi, panduan referensi, panduan kepatuhan, dan panduan implementasi adalah deliverable utama, bukan lampiran.

---

## 6. Key Resources

| Resource | Type | Moat? |
|----------|------|-------|
| **Specification** | IP/Knowledge | **Yes** — kalau jadi standar |
| **Compliance Test Suite** | IP/Code | **Yes** — otoritas untuk validasi |
| **Reference runtime** | Code | **No** — commodity bisa diganti |
| **Benchmark dataset** | Data | **Medium** — tumbuh via kontribusi |
| **Trademark "Sabdo"** | Legal | **Yes** — kendali atas nama |
| **Community trust** | Social | **Yes** — butuh waktu bertahun-tahun |

---

## 7. Key Activities

| Activity | Priority | Untuk apa |
|----------|----------|-----------|
| Stabilkan spec + dokumentasi (Claim → Trace → WisdomScore) | **Highest** | Foundation seluruh ekosistem — dokumentasi adalah produk |
| Bangun compliance test suite | **High** | Otoritas + compatibility review revenue |
| P4 AI Decision Assessment platform | **High** | Bukti empiris + revenue pertama |
| Community management + anchor adoption | **High** | Satu implementasi eksternal > seribu stars |
| Enterprise sales | **Medium** | Revenue jangka panjang |

---

## 8. Key Partnerships

| Partner | Why | Value for them | Value for Sabdo |
|---------|-----|----------------|-----------------|
| Agent frameworks (LangGraph, CrewAI) | Anchor adoption | Ekosistem deliberation | Distribution + credibility |
| Evaluation tools (Arize, Patronus) | Integrasi compliance | Standar input/output | Ecosystem reach |
| Research institutions | Benchmark validation | Publikasi + dataset | Academic credibility |
| Cloud providers | Managed runtime hosting | New service offering | Distribution |

---

## 9. Cost Structure

| Item | Estimate (yearly) | Notes |
|------|-------------------|-------|
| Core maintainer (1 FTE) | $80-120k | Spec + runtime |
| Infrastructure (CI, hosting) | $5-15k | GitHub, cloud |
| Community management | $20-40k | Part-time |
| Legal (trademark) | $5-10k | Filing + protection |
| Marketing (conferences) | $10-20k | 2-3 conferences/year |

**Total estimated burn: $120-205k/year** — sangat lean untuk infrastructure play.

---

## 10. Key Metrics

**North Star:** Satu proyek di luar organisasi yang mengimplementasikan Sabdo Specification karena itu menyelesaikan masalah mereka.

| Metric | Target (Year 1) | Target (Year 3) |
|--------|-----------------|-----------------|
| Independent spec implementations | 2 (Python reference + 1 eksternal) | 3+ (Python, Rust, TypeScript) |
| Frameworks with Sabdo integration | 1 (LangGraph) | 3+ |
| External spec adoption (North Star) | **1 proyek** | 10+ |
| AI Decision Assessment clients | 2 | 20+ |
| Enterprise certifications issued | 0 | 5+ |
| Compatibility Reviews | 2 | 15+ |
| GitHub stars | — | 5k+ |

---

## 11. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Membangun standar yang belum dibutuhkan** | **Fatal** | Anchor partnership + P4 sebagai proof — jangan nunggu spek sempurna, cari satu implementasi eksternal dulu |
| No one adopts the spec | **Fatal** | Anchor partnership with LangGraph first |
| Another standard emerges | **Fatal** | Move fast, P4 benchmark as proof |
| AGPL adoption friction | **Medium** | Keep runtime Apache 2.0, spec CC BY |
| Enterprise too slow to materialize | **Medium** | AI Decision Assessment as bridging revenue |
| Maintainer burnout | **Medium** | Community contributors, focus scope |
