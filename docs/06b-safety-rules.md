# Clinical & Regulatory Safety Rules: ReportSaathi
*References: `docs/01-problem.md`, `docs/02-research.md`, `docs/03-scope.md`, `docs/04-design.md`, `docs/05-prd.md`, `docs/06-architecture.md`*

---

## 1. Regulatory Context & Scope of Authority

ReportSaathi operates strictly as a **Health Information and Patient Comprehension Support Tool**. It is deliberately architected to operate within the **Educational Safe Harbor** of Indian healthcare regulations:

1. **Telemedicine Practice Guidelines (TPG), 2020 (MoHFW / NMC):** Clause 1.1.3 & 3.3 mandate that *only Registered Medical Practitioners (RMPs) can diagnose, prescribe, or adjust medication.* Artificial Intelligence or software algorithms cannot independently practice medicine or alter treatments.
2. **CDSCO Medical Device Rules, 2017 & SaMD Framework:** To remain exempt from Class B/C/D Software as a Medical Device (SaMD) licensing, the application does not perform diagnostic inference, disease risk stratification, or clinical decision support (CDS).
3. **Drugs and Magic Remedies (Objectionable Advertisements) Act, 1954:** Strictly prohibits making claims to "cure" or "reverse" any of the 54 scheduled conditions (including diabetes, hypertension, and heart disease).
4. **Digital Personal Data Protection (DPDP) Act, 2023:** Requires explicit consent, purpose limitation, and strict data minimization for health data.

---

## 2. Inviolable Clinical Safety Rules

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    THE EIGHT INVIOLABLE SAFETY LAWS                        │
├─────────┬───────────────────────────────┬──────────────────────────────────┤
│ Rule #  │ Rule Title                    │ Enforcement Mechanism            │
├─────────┼───────────────────────────────┼──────────────────────────────────┤
│ Rule 1  │ Zero Prescription Alteration  │ Hardcoded non-modifiable doses   │
├─────────┼───────────────────────────────┼──────────────────────────────────┤
│ Rule 2  │ Non-Diagnostic Safe Harbor    │ Zero symptom/disease inference   │
├─────────┼───────────────────────────────┼──────────────────────────────────┤
│ Rule 3  │ Whitelisted Formulary Gate    │ Unlisted drugs blocked from auto │
├─────────┼───────────────────────────────┼──────────────────────────────────┤
│ Rule 4  │ Mandatory Human Verification  │ No raw OCR processed to advice   │
├─────────┼───────────────────────────────┼──────────────────────────────────┤
│ Rule 5  │ Red Flag Triage Matrix        │ High-contrast emergency callouts │
├─────────┼───────────────────────────────┼──────────────────────────────────┤
│ Rule 6  │ Deterministic Audio Synthesis │ Rigid template mad-lib assembly  │
├─────────┼───────────────────────────────┼──────────────────────────────────┤
│ Rule 7  │ Ephemeral Data Purge          │ Auto-deletion within 15 min / 24h│
├─────────┼───────────────────────────────┼──────────────────────────────────┤
│ Rule 8  │ Clinical Review Board Notice  │ Named RMP medical sign-off       │
└─────────┴───────────────────────────────┴──────────────────────────────────┘
```

---

### Rule 1: The Zero-Prescription Modification Invariant
- **Rule Statement:** The system shall **never** advise a user to change, increase, reduce, divide, or discontinue any prescribed tablet, syrup, or injection.
- **Implementation:**
  - The software has no input fields or algorithmic branches for dosage titrations.
  - If a patient asks: *"Can I stop my BP medicine because my readings are normal?"*, the system provides an immutable response: *"Never stop or change blood pressure medication without consulting your treating doctor. Normal readings mean the medicine is working as intended."*

### Rule 2: The Non-Diagnostic Safe Harbor
- **Rule Statement:** The system shall **never** diagnose an illness, predict disease progression, or calculate clinical risk scores.
- **Implementation:**
  - The system describes therapeutic categories solely in terms of maintenance: e.g., *"Helps manage blood glucose"* instead of *"You have severe uncontrolled diabetes."*
  - No symptom-checker questionnaires or differential diagnosis trees are permitted in the codebase.

### Rule 3: Whitelisted Deterministic Formulary Gate
- **Rule Statement:** Automated chronotherapy schedules shall **only** be generated for molecules present in the clinically verified Top-100 Chronic Formulary Database.
- **Implementation:**
  - If an uploaded prescription contains an unrecognized drug token (e.g., an off-formulary oncology drug, immunosuppressant, or psychiatric medication), the system **must not guess**.
  - The UI flags the item with an amber banner: *"Unverified Medicine: Please consult your doctor or local pharmacist for the timing of this specific tablet."* It is excluded from the automated schedule.

### Rule 4: Mandatory Human-in-the-Loop Verification
- **Rule Statement:** Raw OCR output shall **never** be presented as medical truth without explicit patient or caregiver verification.
- **Implementation:**
  - Screen 2 enforces an unskippable confirmation screen.
  - The user must explicitly view the extracted brand names and tap `"Confirm Medicines"` before the schedule and audio synthesis pipeline executes.

---

## 3. Clinical Red Flag Triage Matrix

The system must clearly separate **benign expected sensations** (harmless bodily adaptations) from **critical emergency red flags** to prevent both cyberchondria and delayed emergency care.

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    CHRONIC MEDICINE SAFETY TRIAGE MATRIX                   │
├─────────────────────┬──────────────────────────┬───────────────────────────┤
│ Active Molecule     │ Benign Expected Sensation│ Emergency Red-Flag        │
│ & Common Brands     │ (Reassurance Provided)   │ (Immediate Action Needed) │
├─────────────────────┼──────────────────────────┼───────────────────────────┤
│ Metformin           │ • Mild nausea            │ • Deep, rapid breathing   │
│ (Geminor, Glycomet) │ • Loose stools or gas    │ • Extreme drowsiness      │
│                     │   (Usually passes in 1wk)│ • Severe lactic acidosis  │
├─────────────────────┼──────────────────────────┼───────────────────────────┤
│ Glimepiride         │ • Mild hunger after food │ • Sudden severe sweating  │
│ (Amaryl, Geminor)   │ • Slight headache        │ • Shaking hands, confusion│
│                     │                          │ • Hypoglycemia collapse   │
├─────────────────────┼──────────────────────────┼───────────────────────────┤
│ Telmisartan         │ • Mild lightheadedness   │ • Swelling of lips/tongue │
│ (Telvas, Telma)     │   when standing up fast  │ • Difficulty breathing    │
│                     │                          │ • Severe fainting         │
├─────────────────────┼──────────────────────────┼───────────────────────────┤
│ Amlodipine          │ • Mild flushing/warmth   │ • Severe ankle swelling   │
│ (Amlopres, Stamlo)  │ • Slight ankle heaviness │ • Chest heaviness/pain    │
│                     │   by late evening        │                           │
├─────────────────────┼──────────────────────────┼───────────────────────────┤
│ Atorvastatin        │ • Mild morning muscle    │ • Severe, unexplained     │
│ (Atorva, Storvas)   │   stiffness              │   muscle pain/dark urine  │
│                     │                          │   (Rhabdomyolysis sign)   │
├─────────────────────┼──────────────────────────┼───────────────────────────┤
│ Thyroxine           │ • Mild alertness change  │ • Palpitations, chest pain│
│ (Thyronorm, Eltroxin│                          │ • Profuse sweating, tremor│
└─────────────────────┴──────────────────────────┴───────────────────────────┘
```

### UI Presentation Rules for Red Flags:
1. **Benign Sensations** are rendered inside warm neutral containers (`#FEF3C7`, amber border) labeled: *"सामान्य लक्षण (Normal sensations: These usually settle in a few days)"*.
2. **Emergency Red Flags** are rendered inside high-contrast red alert callouts (`#FEE2E2`, border `2px solid #DC2626`) labeled: *"⚠️ खतरे के संकेत (Emergency Warning Signs: Seek immediate medical care if these occur)"*.

---

## 4. Deterministic Audio Script Assembly Rules

To eliminate hallucination risks associated with generative AI, all audio scripts are constructed using **strict Mad-Lib sentence templates**.

### Standard Hindi Script Template
```text
"नमस्ते [Patient_Name or 'जी']। 
आपके डॉक्टर के पर्चे के अनुसार आपकी दवाइयों का समय इस प्रकार है:

[FOR EACH MEDICINE IN MORNING_SLOT]:
सुबह नाश्ते के समय [Medicine_Brand_Name] लें। इसे [Meal_Timing_Instruction_Hindi]।

[FOR EACH MEDICINE IN NIGHT_SLOT]:
रात को भोजन के बाद [Medicine_Brand_Name] लें। यह [Indication_Purpose_Hindi] के लिए है।

[IF HYPOGLYCEMIA_RISK_PRESENT]:
सावधानी: यदि अचानक पसीना छूटे, हाथ कांपें या घबराहट हो, तो तुरंत मीठी कैंडी या ग्लूकोज लें।

[STATUTORY_OUTRO]:
किसी भी बदलाव से पहले अपने डॉक्टर से सलाह अवश्य लें।"
```

### Verbatim Integrity Check
Before audio synthesis begins, the constructed script is validated against a regular expression whitelist. **No unvetted external strings or open LLM outputs can be piped to the TTS model.**

---

## 5. DPDP Act 2023 Data Scrubbing & Ephemeral Storage Policy

To comply with Section 6, 7, and 8 of the **Digital Personal Data Protection Act, 2023**:

1. **Immediate Image Deletion:**
   - Uploaded prescription images stored in `/tmp/reportsaathi/uploads/` are processed in-memory.
   - The file on disk is securely scrubbed and unlinked (`os.remove()`) immediately after OCR extraction finishes, or within a maximum timeout of **15 minutes**.
2. **24-Hour Ephemeral Session TTL:**
   - Generated schedules and temporary Opus audio files stored in `/tmp/reportsaathi/audio/` are purged automatically upon session expiry (24 hours from creation).
   - A cron worker executes every hour:
     ```sql
     DELETE FROM ephemeral_sessions WHERE expires_at < CURRENT_TIMESTAMP;
     ```
3. **Zero Third-Party Data Transmission:**
   - No health data, extracted drug names, or audio transcripts are transmitted to external marketing platforms, analytic SDKs, or cloud storage buckets.

---

## 6. Clinical Governance & Legal Accountability

- **Named Clinical Review Board:** All formulary rules, chronotherapy meal timings, and translated warning strings are signed off by a panel of Registered Medical Practitioners (RMPs) licensed under the National Medical Commission (NMC).
- **Mandatory Displayed Disclaimer:** Every screen, downloaded image, and WhatsApp forward must contain:
  > *"सूचनात्मक सेवा: यह सारिणी केवल सामान्य जानकारी के लिए है। यह डॉक्टर की सलाह या पर्चे को नहीं बदलती। दवा बदलने से पहले अपने चिकित्सक से परामर्श लें।"*  
  > *(Educational service: This schedule is for general information only. It does not replace or modify your doctor's prescription. Consult your doctor before making any changes.)*
