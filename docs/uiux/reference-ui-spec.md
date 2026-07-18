# Reference UI Specification — Layout & Geometry

> This document reverse-engineers the approved UI reference.
> This is NOT a design suggestion. This is the target layout.
> The purpose is to preserve layout proportions, spacing, hierarchy, and overall visual language while replacing content with Sabdo Pandito Ratu.

---

## Desktop Canvas

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Navigation Bar                                                           │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│                  Hero                                                    │
│                                                                          │
│                  Council Network                                         │
│                                                                          │
│                  Question Panel                                          │
│                                                                          │
└────────────────────────────────────────────────────────────────────────────┘
```

- Everything centered
- Max content width: **1280px**
- Never stretch content edge-to-edge

## Navigation

- Height: **72px**
- Transparent, glass effect, blur

## Hero

- Centered, max width: **900px**
- Heading: ~**64px**, Bold (700)
- Subtitle: ~**22px**, opacity 80%
- Gap between heading & subtitle: **20px**
- Below hero → council gap: **48px**

## Council

- Council diameter: **620px**
- Centered horizontally

## Question Panel

- Width: **900px**
- Below council, gap: **48px**
- Internal padding: **28px**

## Verdict

- Max width: **1280px**
- 2-column grid: left (summary, reasoning, transcript) + right (confidence, wisdom, consensus, bias, ethics, recommendations)
- Cards radius: **20px**, glass

## Design Intent

The user should immediately perceive: *"This is an intelligent deliberation system."*

Must not resemble: ChatGPT, Claude, Gemini, Perplexity, generic SaaS landing page.
