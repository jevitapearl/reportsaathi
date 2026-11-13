# Core Flow & Feature Scope: ReportSaathi
*References: `docs/01-problem.md`, `docs/02-research.md`*

---

## 1. The Single Core Flow

### Objective & Definition
Transform an unreadable or confusing prescription into an immediate, crystal-clear, plain-language **Visual Daily Schedule Card** and a **60–90 second Vernacular Audio Summary** (Hindi/English) for patients over 40 and their family caregivers—explaining what each medicine is for, exact meal/timing chronotherapy, and normal sensations vs. warning signs—without diagnosing, altering dosages, or interfering with doctor orders.

### The Linear 5-Step Core Flow
```
 ┌───────────────┐     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
 │    STEP 1     │     │    STEP 2     │     │    STEP 3     │     │    STEP 4     │     │    STEP 5     │
 │ Input Ingest  │ ──> │ Human Verify  │ ──> │ Formulary Map │ ──> │ Regimen Decode│ ──> │ Output Deliver│
 │ Photo / Search│     │ Confirm Drugs │     │ Pre-vetted DB │     │ Group Schedule│     │ Card + Audio  │
 └───────────────┘     └───────────────┘     └───────────────┘     └───────────────┘     └───────────────┘
```

1. **Step 1: Input Ingest (Caregiver or Patient)**
   - The user opens a lightweight, zero-login mobile web link.
   - Chooses preferred audio language (Hindi / English).
   - Uploads a photo of the prescription OR types/selects medicines using a smart auto-complete search bar.
2. **Step 2: Human-in-the-Loop Verification (Safety Gate)**
   - System displays the identified medicines (e.g., *"1. Geminor M2, 2. Telvas 40, 3. Atorva 10"*).
   - User verifies or edits the list with one tap before decoding begins. No unconfirmed OCR guesses are processed.
3. **Step 3: Deterministic Formulary Mapping**
   - Verified medicines are mapped to a clinically reviewed knowledge base of the top 100 chronic disease formulations in India.
   - Extracts plain-language indication, meal-timing rules, common benign side effects, and critical red flags.
4. **Step 4: Regimen Synthesis (Solving Polypharmacy)**
   - The system synthesizes the individual medicines into a unified, chronologically grouped 24-hour daily timeline (Morning, Afternoon, Night, Bedtime) with explicit meal markers (before food, with food, after food).
5. **Step 5: Multi-Modal Output Delivery**
   - Displays a clean, color-coded **Visual Schedule Card**.
   - Plays a **60–90 second vernacular audio explainer**.
   - Provides a 1-tap **"Share to WhatsApp"** button to forward the visual schedule and audio link directly to the aging parent or family member.

---

## 2. Feature & Sub-Feature Decomposition

```
ReportSaathi Capabilities
├── 1. Intake & Input Capture
│   ├── 1.1 Mobile camera prescription photo capture
│   ├── 1.2 Digital PDF / image upload
│   ├── 1.3 Smart auto-complete drug search picker
│   ├── 1.4 Clinic EMR / QR code auto-population
│   └── 1.5 Voice-input search (speech-to-text drug name)
├── 2. Extraction & Safety Verification
│   ├── 2.1 OCR for printed/digital prescriptions
│   ├── 2.2 OCR for cursive handwritten prescriptions
│   ├── 2.3 Human-in-the-loop verification/confirmation screen
│   └── 2.4 Low-confidence image fallback prompt
├── 3. Clinical Knowledge Engine
│   ├── 3.1 Pre-vetted compendium of top 100 Indian chronic formulations
│   ├── 3.2 Plain-language indication mapper ("Why it matters")
│   ├── 3.3 Chronotherapy / meal-timing rulebook
│   ├── 3.4 Benign sensations vs. red-flag warning database
│   ├── 3.5 Automated drug-drug interaction checker engine
│   ├── 3.6 Unconstrained real-time generative AI clinical advice
│   └── 3.7 Lab report biomarker plain-language explainer
├── 4. Presentation & Audio Synthesis
│   ├── 4.1 Visual Daily Schedule Card (meal & time grouped)
│   ├── 4.2 Scripted vernacular audio explainer (Hindi & English)
│   ├── 4.3 Multi-dialect regional language audio (Tamil, Telugu, Bengali, etc.)
│   ├── 4.4 Tablet appearance / blister strip visual matching
│   └── 4.5 Doctor/Clinic co-branded header
├── 5. Adherence & Caregiver Tools
│   ├── 5.1 One-tap WhatsApp share / download card as image
│   ├── 5.2 Automated WhatsApp / SMS daily dose reminders
│   ├── 5.3 Missed dose logging & adherence tracker
│   └── 5.4 One-click pharmacy refill reordering
├── 6. Regulatory & Security Infrastructure
│   ├── 6.1 Ephemeral zero-login session architecture
│   ├── 6.2 User account creation & family profiles
│   ├── 6.3 DPDP-compliant consent banner & privacy notice
│   ├── 6.4 Conspicuous educational disclaimer (TPG 2020 safe harbor)
│   └── 6.5 ABHA (Ayushman Bharat Health Account) linking
└── 7. Clinical Actions & Interventions (Regulatory Boundary)
    ├── 7.1 Symptom checker / differential diagnosis engine
    ├── 7.2 Dosage alteration / modification suggestions
    ├── 7.3 Generic brand / molecule substitution recommender
    ├── 7.4 Direct prescription of Schedule H/X drugs
    └── 7.5 Commercial health data monetization to pharma/insurers
```

---

## 3. Scope Categorization: MVP, Later, and Never

### NEVER Scope: Hard Regulatory & Clinical Red Lines
*Strictly prohibited to ensure patient safety and maintain compliance with the Telemedicine Practice Guidelines (2020), CDSCO Medical Device Rules (2017), Drugs & Cosmetics Act (1940), and DPDP Act (2023).*

| Feature | Category | Reason for "NEVER" |
| :--- | :--- | :--- |
| **Dosage Modification / Alteration Advice** | Clinical | **Direct violation of NMC Ethics & TPG 2020.** Recommending a patient change or skip a dose constitutes unauthorized medical practice. Classifies software as high-risk Class C/D SaMD under CDSCO. |
| **Symptom Checker / Diagnostic Triage** | Clinical | **Causes severe cyberchondria / catastrophic panic** (as evidenced by WebMD/Ada analysis in `02-research.md`). Software diagnosing illness requires clinical device licensing and expands outside medicine explanation. |
| **Automated Generic / Brand Substitution** | Commercial / Clinical | **Destroys clinical and user trust.** Recommending brand switches triggers fierce consumer backlash (as seen with 1mg/PharmEasy upselling) and ignores specific excipient/bioavailability nuances determined by the treating doctor. |
| **Direct Prescribing / Schedule H/X Dispensing** | Regulatory | **Illegal under Drugs & Cosmetics Act, 1940.** Only a Registered Medical Practitioner (RMP) can prescribe. |
| **Second-Guessing Doctor Judgment** | Clinical | Telling a patient their doctor made an error undermines the therapeutic relationship and creates massive product liability. |
| **Unconstrained Generative AI Advice** | Technical / Safety | Open-ended LLMs produce dangerous hallucinations and sycophantic validation of medical errors. Explanations must be strictly grounded in verified clinical databases. |
| **Selling Patient Health Data / Phone Numbers** | Legal / Privacy | Violates Digital Personal Data Protection Act, 2023 (attracting fines up to ₹250 Crore). |

---

### MVP Scope: The Ruthlessly Pruned Core Flow
*The absolute bare minimum required to deliver end-to-end value safely and validate whether caregivers and patients find plain-language multi-drug schedules useful.*

| Feature | Sub-Feature | Reason for Inclusion in MVP |
| :--- | :--- | :--- |
| **1. Ingest** | `1.1` Printed Prescription Photo Upload<br>`1.3` Smart Search Drug Picker | Photo upload provides effortless entry for digital/printed slips; search picker acts as a fail-safe when photos are blurry or handwriting is messy. |
| **2. Verification** | `2.3` User Confirmation Screen<br>`2.4` Low-confidence Fallback | Guarantees patient safety. The system never generates advice based on unconfirmed OCR guesses. |
| **3. Knowledge Engine** | `3.1` Top 100 Indian Formulations DB<br>`3.2` Plain Indication Mapper<br>`3.3` Chronotherapy Rules<br>`3.4` Benign Sensations vs. Red Flags | Covers >80% of urban chronic polypharmacy cases (metformin, amlodipine, telmisartan, atorvastatin, thyroxine, etc.) with 100% deterministic clinical accuracy. |
| **4. Synthesis & Output** | `4.1` Visual Daily Schedule Card<br>`4.2` Vernacular Audio (Hindi & English) | Solves polypharmacy by organizing the day into Morning/Afternoon/Night meal slots; audio bridges literacy and technical jargon barriers. |
| **5. Delivery** | `5.1` One-Tap WhatsApp Share & Image Download | Enables the digital caregiver (adult child) to instantly transmit the schedule card and audio clip to their parent's WhatsApp chat. |
| **6. Compliance** | `6.1` Ephemeral Zero-Login Architecture<br>`6.3` DPDP Consent Banner<br>`6.4` Educational Clinical Disclaimer | Eliminates onboarding drop-off; satisfies DPDP Act data minimization requirements; shields from SaMD/TPG liability. |

---

### LATER Scope: Scalability, Habit-Building & Partnerships
*High-value enhancements that are valuable for scaling the business, but unnecessary to prove core user value on Day 1.*

| Feature | Sub-Feature | Reason for Deferral to "LATER" |
| :--- | :--- | :--- |
| **Cursive Handwriting OCR** | `2.2` ML Cursive Handwriting Model | Highly prone to OCR errors on messy Indian prescriptions (<50% accuracy). Complex and expensive to build; smart search picker solves this in MVP without risk. |
| **Clinic / EMR Integration** | `1.4` EMR API / QR Code Sync | B2B enterprise sales cycles take 3–6 months. MVP can validate user demand directly via caregiver web upload before integrating into hospital EMRs. |
| **Additional Regional Languages** | `4.3` Tamil, Telugu, Marathi, Bengali, Kannada | Hindi and English cover ~65%+ of the initial target demographic of urban digital caregivers. Expanding language models can follow initial traction. |
| **Automated Pill Reminders** | `5.2` Scheduled WhatsApp / SMS Reminders | Reminders build habit retention, but do not solve the core post-consultation understanding gap. Incurs recurring WhatsApp Business API messaging fees. |
| **Lab Report Plain Explainer** | `3.7` Biomarker Interpretation Engine | High value, but expands scope beyond medicines. Best introduced as "Phase 2" once the prescription explainer is battle-tested. |
| **User Accounts & Profiles** | `6.2` Persistent Family Health Locker | Requiring account creation/passwords creates massive onboarding friction. Can be added when users return for second prescriptions. |
| **ABHA Digital Health Sync** | `6.5` ABDM Gateway Integration | Involves heavy government sandbox certification and compliance audits; not required for an educational web tool. |
| **Pill Shape/Color Visualizer** | `4.4` Pill Appearance Matching | High catalog maintenance overhead across hundreds of generic pharmaceutical manufacturers in India. Visual icons on schedule cards suffice for MVP. |
| **Drug Interaction Checker** | `3.5` Dynamic Multi-Drug Contraindication | Complex clinical decision support that borders on SaMD Class B regulation. High liability risk; MVP focuses on meal-timing chronotherapy. |

---

## 4. Ruthless MVP Pruning & Challenges

We explicitly challenged every candidate feature in the MVP against the test: **"Can the core flow work without it?"**

```
┌────────────────────────────────────────────────────────────────────────────┐
│                       RUTHLESS MVP PRUNING AUDIT                           │
├──────────────────────────────┬────────────┬────────────────────────────────┤
│ Candidate Feature            │ Decision   │ Pruning Rationale              │
├──────────────────────────────┼────────────┼────────────────────────────────┤
│ Native Android/iOS App       │ ✂️ CUT     │ Web app requires 0MB download; │
│                              │            │ links open instantly.          │
├──────────────────────────────┼────────────┼────────────────────────────────┤
│ User Account / Password      │ ✂️ CUT     │ Eliminates 40%+ drop-off.      │
│                              │            │ Ephemeral session is safer.    │
├──────────────────────────────┼────────────┼────────────────────────────────┤
│ Cursive Handwriting OCR      │ ✂️ CUT     │ High hallucination/error rate; │
│                              │            │ Smart search picker is safer.  │
├──────────────────────────────┼────────────┼────────────────────────────────┤
│ WhatsApp Daily Push Alarms   │ ✂️ CUT     │ Habit feature, not explainer;  │
│                              │            │ Burns Meta API fees on Day 1.  │
├──────────────────────────────┼────────────┼────────────────────────────────┤
│ Open-Ended Generative AI     │ ✂️ CUT     │ Risk of hallucination;         │
│                              │            │ Deterministic DB is 100% safe. │
├──────────────────────────────┼────────────┼────────────────────────────────┤
│ Lab Report Decoder           │ ✂️ CUT     │ Expands scope; defer to Phase 2│
├──────────────────────────────┼────────────┼────────────────────────────────┤
│ 10 Regional Languages        │ ✂️ CUT     │ Hindi + English covers initial │
│                              │            │ test cohort.                   │
└──────────────────────────────┴────────────┴────────────────────────────────┘
```

### The Pruned, Battle-Ready MVP Experience:
1. Caregiver opens link on mobile browser.
2. Snaps a photo of the printed prescription slip (or taps 3 drug names in the smart search bar).
3. Taps **"Confirm Medicines"**.
4. Within 3 seconds, sees a color-coded **Daily Schedule Card** (Morning / Lunch / Night) and taps **"Play Audio"** to hear a 60-second summary in Hindi.
5. Taps **"Send to Papa on WhatsApp"** to forward the image and audio note.
