# Product Requirements Document (PRD): ReportSaathi
*References: `docs/01-problem.md`, `docs/02-research.md`, `docs/03-scope.md`, `docs/04-design.md`*

---

## 1. Document Overview & Context

- **Product Name:** ReportSaathi (रिपोर्ट साथी)
- **Document Version:** 1.0 (MVP Specification)
- **Target Audience:** Adults over 40 with chronic non-communicable diseases (diabetes, hypertension, cardiac conditions) and their primary family caregivers (adult sons/daughters, ages 25–45).
- **Geographic & Legal Context:** India (compliant with DPDP Act 2023, Telemedicine Practice Guidelines 2020, and CDSCO Medical Device Rules 2017).

---

## 2. Product Vision & Goals

### Vision
To ensure that no patient in India leaves a medical consultation confused about their daily medications, by providing an instant, multi-drug daily schedule card and a 60–90 second vernacular audio explanation directly to their phone.

### Primary Goals
1. **Bridge the Post-Consultation Comprehension Gap:** Convert rushed, technical, or handwritten doctor prescriptions into plain-language daily schedules in under 60 seconds.
2. **Solve Polypharmacy (Multi-Drug Regimens):** Provide a unified 24-hour daily timeline (Morning / Afternoon / Night) that groups 2–6 concurrent chronic medications with clear meal-timing chronotherapy.
3. **Overcome Age & Literacy Barriers via Audio:** Deliver a high-quality, pre-scripted 60–90 second audio summary in Hindi and English with universal WhatsApp-style controls.
4. **Empower the Digital Caregiver Proxy:** Enable adult children to decode their parents' prescriptions remotely and forward the schedule and audio note in one tap to their parent's WhatsApp.
5. **Zero Friction & High Accessibility:** Deliver the experience via a zero-login mobile web application optimized for low-cost Android smartphones (360px viewport, <120KB initial payload).

### Non-Goals (Strict Out-of-Scope Boundaries)
1. **NO Clinical Diagnosis:** The product will NEVER evaluate symptoms, offer differential diagnoses, or tell a patient what illness they have.
2. **NO Dosage Modifications or Prescription Changes:** The product will NEVER advise increasing, reducing, or discontinuing any prescribed drug. All doctor orders are treated as inviolable.
3. **NO Commercial Brand Substitutions:** The product will NEVER recommend alternative brands or generic switches, avoiding commercial conflicts of interest.
4. **NO E-Commerce / Pharmacy Dispensing:** The MVP does not sell medicines, deliver pills, or partner with chemists for transactional fulfillment.
5. **NO Unconstrained Open-Ended LLM Advice:** Medical explanations must be strictly deterministically grounded in a pre-vetted formulary; free-form generative AI chatting on medical topics is forbidden.
6. **NO Persistent Patient Profiling / Data Monetization:** Zero patient profiling, zero advertising, and zero data selling to pharmaceutical companies or insurers.

---

## 3. User Personas & User Stories

### Persona 1: Rohit (32, The Digital Caregiver)
- **Profile:** Software engineer living in Bengaluru; parents (aged 62 and 58) live in Lucknow.
- **Pain Point:** His father was prescribed three new tablets for high blood pressure and diabetes. His father calls him confused about whether *Telvas 40* is taken before or after breakfast and whether *Geminor M2* can cause dizziness. Rohit cannot read the doctor's handwriting on the photo sent on WhatsApp.
- **Goal:** Wants an instant, clear, decoded summary of the exact schedule and precautions that he can review and forward back to his father's WhatsApp.

### Persona 2: Rameshwar Ji (58, The Chronic Patient)
- **Profile:** Small shop owner in Lucknow with Type 2 diabetes and hypertension.
- **Pain Point:** Has presbyopia (struggles with small English print), doctor spent 2 minutes with him in a crowded OPD, pharmacist scribbled numbers on paper envelopes that smeared.
- **Goal:** Prefers listening to a clear audio note in Hindi explaining when to take each tablet and what to do if he feels dizzy or sweaty.

---

### User Stories & Acceptance Criteria

#### US-01: Printed Prescription Capture & Upload
> **As a** digital caregiver,  
> **I want to** take a photo of my parent's printed hospital prescription slip or upload an image,  
> **So that** the system can automatically extract the list of prescribed medicines without me typing them manually.

- **Acceptance Criteria:**
  1. User can trigger the device camera or select an existing JPG/PNG/WebP image from the gallery.
  2. The upload handles files up to 10MB and compresses them client-side before transmission.
  3. Image processing initiates immediately and displays an animated progress state with reassuring copy.
  4. If the image is blurry, skewed, or unreadable, the system displays an accessible error screen with clear guidance and a fallback to manual search.

#### US-02: Smart Drug Auto-Complete Search
> **As a** caregiver or patient with a handwritten or blurry prescription slip,  
> **I want to** quickly search for medicine names with intelligent auto-complete,  
> **So that** I can build my medicine list even if camera OCR fails.

- **Acceptance Criteria:**
  1. Search input triggers after typing 2 characters.
  2. Auto-complete searches across the top 100 Indian chronic brand names and their generic molecules (e.g., typing *"Gemin"* suggests *"Geminor M2 - Glimepiride + Metformin"*).
  3. Selecting a search result adds the drug to the verification list with its default standard chronotherapy tags.

#### US-03: Medication Verification & Human-in-the-Loop Confirmation
> **As a** user,  
> **I want to** review and confirm the list of recognized medicines before decoding begins,  
> **So that** OCR errors or misidentifications are caught and corrected before any advice is generated.

- **Acceptance Criteria:**
  1. Displays each recognized medicine in an individual card with brand name, salt composition, and indication badge.
  2. Each card provides a single-tap 48x48dp delete button (`हटाएं ✕`).
  3. An `+ Add missing medicine` button allows adding additional drugs via auto-complete.
  4. The primary `"Decode Schedule"` button is disabled if zero valid medicines are present.
  5. The system never generates clinical schedules from unconfirmed OCR guesses.

#### US-04: Multi-Drug Daily Schedule Generation
> **As a** patient or caregiver,  
> **I want to** see all confirmed medications organized into a single chronological 24-hour daily timeline,  
> **So that** I know exactly which pills to take together at breakfast, lunch, dinner, or bedtime.

- **Acceptance Criteria:**
  1. Synthesizes medications into chronological meal-based blocks: Morning / Breakfast, Afternoon / Lunch, Evening / Dinner, and Bedtime.
  2. Each drug entry indicates: Brand name, plain-language purpose (e.g., *"Blood sugar control"*), and relation to food (*"With first bite of meal"*, *"After food"*).
  3. Combined lifestyle precautions are highlighted (e.g., *"Keep glucose candy handy for sudden sweating/dizziness"*).

#### US-05: Vernacular Audio Explanation (Hindi & English)
> **As an** older patient with diminished eyesight or limited English reading literacy,  
> **I want to** tap a single play button to hear a 60–90 second audio explanation in Hindi,  
> **So that** I understand my medicine schedule without reading dense text.

- **Acceptance Criteria:**
  1. Persistent floating audio player bar at the top of the schedule screen with a minimum 48x48dp play/pause button.
  2. Audio streams within 3 seconds of page load on standard 3G/4G connections.
  3. Audio script follows a pre-vetted, compassionate, respectful template addressing the patient.
  4. If audio playback fails due to network constraints, an automatic accessible full-text transcript card is displayed below with a retry button.

#### US-06: One-Tap WhatsApp Forwarding
> **As a** digital caregiver,  
> **I want to** tap a single button to forward the complete schedule card and audio link to my parent on WhatsApp,  
> **So that** they can access it instantly inside their most familiar app.

- **Acceptance Criteria:**
  1. Tapping `"Send to WhatsApp"` constructs a pre-formatted WhatsApp deep-link (`whatsapp://send?text=...` / `https://wa.me/`).
  2. The message includes a polite greeting in Hindi, a summary of morning/night timings, and a direct link to the interactive visual card and audio player.
  3. The link opens without requiring account creation or login on the recipient's phone.

---

## 4. Numbered Functional Requirements (FR)

### Ingest & Language (FR-01 to FR-03)
- **FR-01: Language Selection:** The system shall support Hindi and English, with a sticky toggle on Screen 1 that switches the entire UI, typography, and audio synthesis target immediately.
- **FR-02: Image Capture & Client-Side Optimization:** The system shall accept JPG, PNG, and WebP prescription images up to 10MB, auto-orient the image, and resize it to a maximum of 1920px on the longest dimension before uploading to minimize data transfer on mobile networks.
- **FR-03: Smart Auto-Complete Formulary Search:** The search input shall query an indexed local/edge database of the top 100 Indian chronic brand names and generic salts, returning matched results within 100ms.

### Parsing & Verification (FR-04 to FR-06)
- **FR-04: Printed Prescription Text Extraction (OCR):** The system shall process uploaded printed hospital prescription images through an OCR extraction pipeline and match recognized text tokens against the approved formulary dictionary.
- **FR-05: Mandatory Verification Screen:** The system shall require the user to explicitly tap a confirmation button on the recognized medication list before advancing to schedule generation.
- **FR-06: Low-Confidence & Fallback Handling:** If OCR confidence on any line is below 75%, or if no formulary match is found, the system shall flag the line as unverified and prompt the user to search manually.

### Clinical Synthesis & Schedule (FR-07 to FR-09)
- **FR-07: Deterministic Chronotherapy Mapping:** The system shall map each verified medication to deterministic, medically validated rules:
  - Morning (Breakfast): Sulfonylureas (with food), SGLT2 inhibitors (morning), ACE-I/ARBs (morning/after breakfast), Thyroid hormone (empty stomach 30 mins before breakfast).
  - Night (Dinner/Bedtime): Statins (cholesterol synthesis peak at night), anti-hypertensives dosed at bedtime.
- **FR-08: Visual Schedule Card Generation:** The system shall render a responsive, color-coded daily schedule card organizing medications into chronological meal containers with icons and dosage badges.
- **FR-09: Precaution & Warning Categorization:** The system shall categorize medication advisories into:
  - *Benign sensations:* Expected, self-limiting side effects (e.g., harmless urine discoloration, mild initial nausea).
  - *Red-flag danger signs:* Critical symptoms requiring immediate medical consultation (e.g., hypoglycemia shakiness, severe swelling, chest heaviness).

### Audio Synthesis & Delivery (FR-10 to FR-12)
- **FR-10: Deterministic Script Assembly & Audio Synthesis:** The system shall construct audio scripts using pre-approved clinical sentence templates (substituting confirmed drug names and timings) and synthesize audio in high-clarity Hindi/English voice models.
- **FR-11: Audio Player Controls:** The audio player shall feature play/pause, a touch-draggable scrubber bar, elapsed/total time indicators, and support standard HTML5 Audio APIs.
- **FR-12: Full Text Transcript Fallback:** If audio fails to load within 5 seconds, the system shall automatically reveal an accessible full-text transcript of the spoken advice.

### Sharing, Compliance & Privacy (FR-13 to FR-15)
- **FR-13: WhatsApp Deep-Linking:** The system shall generate a `wa.me` sharing URI containing a formatted textual summary and a secure access token link.
- **FR-14: Ephemeral Zero-Login Architecture:** The system shall store session data temporarily in-memory or in an ephemeral cache with a time-to-live (TTL) of 24 hours. No permanent patient database, phone number directory, or user tracking table shall be maintained in MVP.
- **FR-15: Statutory Clinical Disclaimers:** Every screen and shared message shall conspicuously feature the statutory notice: *"Educational information only. ReportSaathi does not provide medical advice or modify doctor prescriptions. Consult your doctor for any changes."*

---

## 5. Non-Functional Requirements (NFR)

### NFR-01: Performance & Latency
- The initial web application bundle (HTML + CSS + JS) shall weigh less than **120KB** gzipped.
- Time to First Contentful Paint (FCP) shall be **< 1.5 seconds** on a 3G mobile network (1.6 Mbps download, 300ms RTT).
- Complete OCR extraction and formulary matching shall execute in **< 8 seconds**.
- Audio synthesis and playback buffering shall start within **< 4 seconds**.
- The end-to-end journey from photo upload to schedule display shall take **< 45 seconds**.

### NFR-02: Network & Bandwidth Efficiency
- Audio files shall be encoded in **mono Opus / AAC at 32 kbps**, resulting in an audio payload of **< 360KB** for a 90-second explanation.
- Uploaded images shall be compressed client-side to **< 300KB** before transmission.

### NFR-03: Low-Cost Android Device Compatibility
- The application shall run smoothly on Android 8.0+ devices with **2GB RAM** and entry-level chipsets (MediaTek Helio A22 / Unisoc SC9863A).
- UI layout shall be fully responsive on viewport widths ranging from **320px to 480px** (tested at 360x640px base).
- All touch targets shall maintain a minimum bounding box of **48x48dp** (Primary action buttons: **56dp** height).

### NFR-04: Accessibility & Indic Typography
- All text and interactive elements shall satisfy **WCAG 2.1 AAA contrast ratio (7:1)** against their background surfaces (minimum 4.5:1 for large headings).
- All Devanagari and non-Latin typography shall enforce a minimum **line-height of 1.55x** to prevent vertical clipping of matras and diacritics.
- No clinical copy or drug names shall use `text-overflow: ellipsis`.

### NFR-05: Data Privacy & Security (DPDP Act 2023)
- No personally identifiable health data, uploaded prescription images, or phone numbers shall be persisted to permanent storage.
- All network communications shall be strictly encrypted over **TLS 1.3**.
- Prescription images stored in temporary storage during OCR processing shall be automatically scrubbed and permanently deleted immediately after extraction (max retention: 15 minutes).

---

## 6. Safety Requirements (SR)

- **SR-01: Absolute Prohibition on Dosing Alterations:** The system must never suggest changing, halving, doubling, or skipping any medication dose.
- **SR-02: Absolute Prohibition on Clinical Diagnoses:** The system must never infer or display disease diagnoses from uploaded prescriptions (e.g., it must not say *"You have severe diabetes"*). It only states the therapeutic category (e.g., *"Helps manage blood sugar"*).
- **SR-03: Mandatory Formulary Whitelist:** Only medications explicitly present in the clinically validated top 100 formulary database can generate automated chronotherapy schedules. Any unlisted drug must be flagged for manual physician verification.
- **SR-04: Emergency Red-Flag Prominence:** Symptoms representing life-threatening adverse reactions (e.g., anaphylaxis, severe hypoglycemia, angioedema) must be displayed in high-contrast red callouts with explicit instructions to seek immediate in-person emergency care.
- **SR-05: Named Clinical Review Board:** The application footer and about modal must display the credentials of the Registered Medical Practitioner (RMP) board that validated the formulary rules to ensure regulatory accountability under the National Medical Commission (NMC) guidelines.

---

## 7. Success Metrics & KPIs

```
┌────────────────────────────────────────────────────────────────────────────┐
│                       REPORTSAATHI SUCCESS METRICS                         │
├─────────────────────────┬───────────────────┬──────────────────────────────┤
│ Metric Category         │ KPI Name          │ MVP Target Goal              │
├─────────────────────────┼───────────────────┼──────────────────────────────┤
│ North Star Metric       │ Decoded Regimens  │ 500 verified regimens/week   │
│                         │ Listened/Shared   │                              │
├─────────────────────────┼───────────────────┼──────────────────────────────┤
│ Funnel Conversion       │ Intake -> Verify  │ > 80% completion             │
│                         │ Verify -> Decode  │ > 85% completion             │
├─────────────────────────┼───────────────────┼──────────────────────────────┤
│ Engagement & Utility    │ Audio Play Rate   │ > 70% of decoded schedules   │
│                         │ WhatsApp Share    │ > 45% of decoded schedules   │
├─────────────────────────┼───────────────────┼──────────────────────────────┤
│ Safety & Accuracy       │ OCR Discard Rate  │ < 5% unreadable errors       │
│                         │ Clinical Errors   │ ZERO reported safety events  │
├─────────────────────────┼───────────────────┼──────────────────────────────┤
│ User Comprehension      │ Post-Use Survey   │ > 85% caregivers report      │
│                         │ Confidence Score  │ "Complete timing clarity"    │
└─────────────────────────┴───────────────────┴──────────────────────────────┘
```
