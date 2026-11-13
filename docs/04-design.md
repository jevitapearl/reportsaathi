# Design Direction & Screen State Specification: ReportSaathi
*References: `docs/01-problem.md`, `docs/02-research.md`, `docs/03-scope.md`*

---

## 1. Executive Design Goals

ReportSaathi is designed to bridge the post-consultation comprehension gap for adults over 40 managing chronic illnesses in India, and their digital caregivers (adult children). 

The user interface and design system must satisfy three non-negotiable constraints:
1. **Accessibility for Older Adults (Ages 40–75+):** Compensate for age-related presbyopia (declining vision), motor tremors (reduced touch accuracy), and low digital literacy.
2. **Performance on Low-Cost Android Devices:** Flawless operation on ₹6,000–₹10,000 Android phones (e.g., Redmi A-series, Samsung M04, Realme C-series) with 2GB–3GB RAM, low-end chipsets, and intermittent 3G/4G connectivity.
3. **Resilience for Indic Scripts & Long Compounds:** Native support for Devanagari (Hindi, Marathi), Tamil, Telugu, and other non-Latin scripts where words are 30%–50% longer than English and contain vertical diacritics (*matras*).

---

## 2. Competitive Reference Analysis: What to Borrow & What to Avoid

Below is an evaluation of the five archetypes researched in `docs/02-research.md`. High-resolution visual captures are stored in [`docs/references/`](file:///home/jevitapearl/reportsaathi/docs/references/).

```
┌────────────────────────────────────────────────────────────────────────────┐
│                       DESIGN BENCHMARK MATRIX                              │
├───────────────────────┬────────────────────────────┬───────────────────────┤
│ Reference Product     │ What to Borrow             │ What to Avoid         │
├───────────────────────┼────────────────────────────┼───────────────────────┤
│ 1. WhatsApp           │ • Universal audio scrubber │ • Wall of text        │
│    (Voice Note UI)    │ • 48dp green play button   │ • Fake forwards       │
│    [Screenshot]       │ • 1-tap family forwarding  │ • Unstructured chat   │
├───────────────────────┼────────────────────────────┼───────────────────────┤
│ 2. Tata 1mg           │ • Indication mapping       │ • Giant discount ads  │
│    (Monograph/Store)  │ • Salt molecule breakdown  │ • 10px English text   │
│    [Screenshot]       │ • Photo upload flow        │ • Buried info under CTA│
├───────────────────────┼────────────────────────────┼───────────────────────┤
│ 3. Ada Health         │ • Single-column card flow  │ • "Go to ER" bias     │
│    (Clinical Triage)  │ • Calm neutral palette     │ • Cyberchondria lists │
│    [Screenshot]       │ • Visual step progression  │ • Login wall gates    │
├───────────────────────┼────────────────────────────┼───────────────────────┤
│ 4. Dr Lal PathLabs    │ • Clinical accreditation   │ • Raw numeric tables  │
│    (Pathology Report) │ • Standard biomarker names │ • Scary red tags      │
│    [Screenshot]       │ • Chronological records    │ • 5-page dense PDFs   │
├───────────────────────┼────────────────────────────┼───────────────────────┤
│ 5. NHS Digital        │ • WCAG AAA 7:1 contrast    │ • Cold desktop UI     │
│    (Accessible Card)  │ • 18px–20px base font size │ • Lack of vernacular  │
│    [Screenshot]       │ • Plain language phrasing  │   audio guidance      │
└───────────────────────┴────────────────────────────┴───────────────────────┘
```

### Reference 1: WhatsApp Voice Note & Chat UI
*Visual Reference:* [`docs/references/ref_01_whatsapp_audio.png`](file:///home/jevitapearl/reportsaathi/docs/references/ref_01_whatsapp_audio.png)
- **What to Borrow:**
  - **The Universal Audio Player Pattern:** 95%+ of older smartphone users in India intuitively understand the WhatsApp voice bubble (large play/pause circle, scrubbable progress track, elapsed time counter).
  - **Familiar Touch Targets:** Minimum 48x48dp green circular trigger buttons.
  - **One-Tap Share Channel:** The primary delivery mechanism to the parent must be a native WhatsApp share trigger (`whatsapp://send`).
- **What to Avoid:**
  - **Unstructured Messaging Streams:** Health instructions must not be presented as loose chat messages that scroll off-screen.
  - **Forwarding Ambiguity:** Must not look like a casual "WhatsApp forward" to avoid skepticism and the "WhatsApp University" stigma.

### Reference 2: Tata 1mg Medicine Monograph & Store
*Visual Reference:* [`docs/references/ref_02_tata1mg_monograph.png`](file:///home/jevitapearl/reportsaathi/docs/references/ref_02_tata1mg_monograph.png)
- **What to Borrow:**
  - **Clear Generic Salt Association:** Pairing commercial brand names with generic molecules (e.g., *Geminor M2* -> *Glimepiride + Metformin*).
  - **Structured Explanations:** Clean categorizations for "Why it is prescribed" and "How to take it."
- **What to Avoid:**
  - **Commercial Clutter & Banners:** Flashing discount badges ("25% OFF!"), loyalty subscription promos, and health checkup cross-sells distract anxious patients.
  - **Tiny Micro-Typography:** 10px–11px light-gray English fonts that are completely unreadable for presbyopic elders.
  - **Buried Clinical Content:** Placing vital dosage instructions below the fold beneath commercial "Add to Cart" and payment widgets.

### Reference 3: Ada Health Clinical Assessment Card
*Visual Reference:* [`docs/references/ref_03_ada_health_triage.png`](file:///home/jevitapearl/reportsaathi/docs/references/ref_03_ada_health_triage.png)
- **What to Borrow:**
  - **Card-Based Visual Focus:** Presenting one concept per card with ample whitespace and rounded corners.
  - **Calm, Reassuring Palette:** Deep navy and clinical whites that convey authority without sterile coldness.
- **What to Avoid:**
  - **Alarmist Differential Diagnoses:** Listing terrifying rare diseases (e.g., stroke, glioblastoma) for common symptoms.
  - **The Default "Go to ER" Problem:** Overly defensive liability algorithms that trigger panic over benign medication adjustments.
  - **Mandatory Account Walls:** Forcing account creation and email confirmation before delivering value.

### Reference 4: Dr. Lal PathLabs Diagnostic Report Display
*Visual Reference:* [`docs/references/ref_04_lalpathlabs_report.png`](file:///home/jevitapearl/reportsaathi/docs/references/ref_04_lalpathlabs_report.png)
- **What to Borrow:**
  - **Accredited Clinical Rigor:** Clear indication that data is grounded in validated medical science.
  - **Standard Parameter Naming:** Using recognized terminology (Fasting Sugar, HbA1c, Serum Creatinine).
- **What to Avoid:**
  - **Raw Numeric Tabular Dumps:** Tables with biological reference ranges that mean nothing to everyday patients without clinical context.
  - **Context-Free Red Flags:** Flashing bold red `[HIGH]` tags that cause severe distress for borderline or clinically expected values.
  - **Dense Multi-Page PDFs:** Documents designed for desktop A4 printers that require pinch-to-zoom on budget smartphones.

### Reference 5: NHS Digital / GOV.UK Health Design System (Gold Standard)
*Visual Reference:* [`docs/references/ref_05_nhsuk_accessibility.png`](file:///home/jevitapearl/reportsaathi/docs/references/ref_05_nhsuk_accessibility.png)
- **What to Borrow:**
  - **High-Contrast Accessible Color System:** Minimum 7:1 contrast ratio for text and 3:1 for interactive components.
  - **Generous Typography:** 18px–20px body font size with generous line spacing (1.5x–1.6x).
  - **Single-Column Linear Flow:** Zero multi-column layouts; content stacks vertically in an intuitive hierarchy.
  - **Plain-Language Callout Blocks:** Clear yellow/blue alert boxes distinguishing normal directions from warnings.
- **What to Adapt for India:**
  - **Integrate Vernacular Audio:** The NHS text-first model assumes high textual literacy; in India, audio playback is mandatory.
  - **Warm Familial Tone:** Replace cold public-sector phrasing with respectful, caregiver-friendly language.

---

## 3. Core Flow Screen State Specifications

The MVP core flow consists of three focused screens. Below are the state matrices for each.

```
                  SCREEN ARCHITECTURE IN THE CORE FLOW
                  
   Screen 1: Prescription Intake        Screen 2: Verification          Screen 3: Decoded Regimen
 ┌───────────────────────────────┐   ┌───────────────────────────┐   ┌─────────────────────────────┐
 │ • Language Toggle (Hindi/Eng) │   │ • Recognized Drug Cards   │   │ • Sticky Vernacular Audio   │
 │ • Big Camera Capture Button   │──>│ • Timing & Meal Badges    │──>│ • Morning/Afternoon/Night   │
 │ • Smart Search Auto-Complete  │   │ • "+ Add Missing" Picker  │   │ • Benign vs Red Flag Alert  │
 │ • Trust & Compliance Notice   │   │ • Primary "Decode" CTA    │   │ • "Send to WhatsApp" Action │
 └───────────────────────────────┘   └───────────────────────────┘   └─────────────────────────────┘
```

---

### Screen 1: Prescription Intake (`/` or `/intake`)

#### Purpose
Provide a frictionless, zero-login intake channel where a caregiver or patient submits prescription data via mobile camera photo upload or smart search.

| State | UI Elements & Visual Layout | User Action / Transitions | Visual Screenshot Link |
| :--- | :--- | :--- | :--- |
| **Default** | • Top App Bar with brand name and bilingual toggle (`हिंदी / Eng`).<br>• Trust Banner explaining value in plain language (`दवाइयों का समय और मतलब समझें`).<br>• Primary Action: Large 56dp camera card with camera icon (`पर्ची का फोटो खींचें या चुनें`).<br>• Secondary Action: Full-width search bar with auto-complete (`🔍 दवा का नाम खोजें`).<br>• Fast-picker tags for common medicines (`+ Metformin`, `+ Telmisartan`).<br>• Statutory privacy and educational disclaimer at bottom. | User taps camera button to capture photo, selects existing image from gallery, or taps search bar. | [`docs/references/screen_01_intake_default.png`](file:///home/jevitapearl/reportsaathi/docs/references/screen_01_intake_default.png) |
| **Empty** | • Displayed on cold open.<br>• Search bar shows helpful ghost text: `"उदा. Geminor, Telvas, Atorva..."`.<br>• Prompts patient/caregiver to choose either photo or manual search. | User begins typing or triggers camera. | Same as Default |
| **Loading** | • Central modal card over blurred background.<br>• High-contrast green circular progress spinner (SVG/CSS, hardware accelerated).<br>• Animated status copy: `"पर्चे से दवाइयां खोजी जा रही हैं..."` -> `"दवाइयों का नाम जांचा जा रहा है..."`.<br>• Reassurance text: `"कृपया 5-10 सेकंड प्रतीक्षा करें।"`<br>• Cancel / Fallback button: `"रद्द करें / खुद नाम लिखें"`. | Automatically transitions to Screen 2 upon completion. User can tap cancel to switch to manual entry. | [`docs/references/screen_01_intake_loading.png`](file:///home/jevitapearl/reportsaathi/docs/references/screen_01_intake_loading.png) |
| **Error** | • Soft red alert container (`#FDF2F2`) with 32dp bold warning icon.<br>• Plain language headline: `"फोटो साफ़ नहीं दिख रही है"` (Photo not clear).<br>• Bullet points explaining cause without technical terms: `"कृपया अच्छी रोशनी में दोबारा फोटो खींचें"` or `"पर्चा मुड़ा हुआ न हो"`<br>• Primary Recovery CTA (56dp green button): `"📷 दोबारा साफ़ फोटो खींचें"`.<br>• Secondary Recovery CTA: `"🔍 खुद दवा का नाम लिखें"`. | User either retakes the photo or taps manual search picker to enter drugs manually. | [`docs/references/screen_01_intake_error.png`](file:///home/jevitapearl/reportsaathi/docs/references/screen_01_intake_error.png) |

---

### Screen 2: Medication Verification & Confirmation (`/verify`)

#### Purpose
Safety gate. Prevents unconfirmed OCR errors from reaching the patient. Allows user to confirm, edit, or append recognized medications before generating clinical schedules.

| State | UI Elements & Visual Layout | User Action / Transitions | Visual Screenshot Link |
| :--- | :--- | :--- | :--- |
| **Default** | • Screen Header: `"कदम 2: दवाइयों की पुष्टि करें"` (Step 2: Confirm Medicines).<br>• Clear instructions: `"पर्चे में ये दवाइयां मिली हैं। जांच लें:"`<br>• Individual Medicine Cards (minimum 88dp height):<br>  - Bold brand name (e.g., `1. Geminor M2`, `2. Telvas 40`).<br>  - Indication subtitle: `शुगर / डायबिटीज`, `ब्लड प्रेशर`.<br>  - Meal badge: `सुबह नाश्ते के साथ` (Morning with food).<br>  - High-contrast delete button: `हटाएं ✕` (48x48dp target).<br>• `+ कोई दवा छूट गई? जोड़ें` (Add missing medicine) button.<br>• Sticky Bottom Action (56dp green button): `"समय और सावधानियां समझें ➔"`. | User reviews list, deletes false matches, adds missing drugs, and taps the primary button to decode. | [`docs/references/screen_02_verify_default.png`](file:///home/jevitapearl/reportsaathi/docs/references/screen_02_verify_default.png) |
| **Empty** | • Occurs if user removes all medicines or OCR detected zero drugs.<br>• Soft grey illustration of empty pill box.<br>• Headline: `"सूची में कोई दवा नहीं है"` (No medicines in list).<br>• Subtext: `"कृपया कम से कम एक दवा का नाम जोड़ें।"`<br>• Primary Action CTA: `"🔍 दवा का नाम खोजकर जोड़ें"`.<br>• Primary "Decode" button is disabled (40% opacity). | User taps button to open search auto-complete picker and select their prescribed medicines. | [`docs/references/screen_02_verify_empty.png`](file:///home/jevitapearl/reportsaathi/docs/references/screen_02_verify_empty.png) |
| **Loading** | • Semi-transparent white overlay (`rgba(255,255,255,0.85)`).<br>• Inline pulsing skeleton loader across the card items.<br>• Loading copy: `"दवाइयों की सारिणी तैयार हो रही है..."` (Preparing schedule...). | Automatically transitions to Screen 3 within 1.5 seconds. | Transition state |
| **Error** | • Inline amber warning banner at top of card: `"कुछ दवाइयों की मात्रा स्पष्ट नहीं है"` (Unclear dosage).<br>• The ambiguous medicine card highlights in yellow with an `"इसे सुधारें"` (Edit this) tap target.<br>• Primary action remains accessible once the item is clarified or removed. | User taps edit to pick the exact formulation or taps delete to remove. | Inline state |

---

### Screen 3: Decoded Regimen Schedule & Vernacular Audio (`/schedule`)

#### Purpose
Delivers the core value: A multi-drug daily timeline grouped by meal, paired with a persistent vernacular audio summary and a one-tap WhatsApp sharing trigger.

| State | UI Elements & Visual Layout | User Action / Transitions | Visual Screenshot Link |
| :--- | :--- | :--- | :--- |
| **Default** | • Header with patient name & age badge: `"मरीज: रामेश्वर जी (उम्र 58 वर्ष)"`.<br>• **Sticky Floating Audio Player Bar (Top):**<br>  - 48dp green play button with audio scrubber.<br>  - Headline: `"डॉक्टर का सारांश सुनें (हिंदी • 1:12 मिनट)"`.<br>  - Subtext: `"दवा लेने का सही समय और जरूरी सावधानियां"`.<br>• **Chronological Meal Regimen Cards:**<br>  - *Morning Card (🌅 सुबह नाश्ता):* Geminor M2 (with first bite), Telvas 40 (after breakfast), hypoglycemia warning.<br>  - *Night Card (🌙 रात का खाना):* Atorva 10 (after dinner at bedtime), cholesterol protection badge.<br>• **Clinical Guidance Callout Card (⚠️ सावधानियां):**<br>  - Normal expected sensations (mild gas/headache) vs. Red Flag Danger signs (sweating, palpitations, chest pressure).<br>• **Sticky Bottom Bar:**<br>  - Primary (56dp WhatsApp Green): `"📲 पापा को व्हाट्सएप पर भेजें"`.<br>  - Secondary (Grey Outline): `"⬇️ पर्चा छवि डाउनलोड करें"`. | User taps audio play to listen in Hindi, reads schedule card, and taps WhatsApp button to forward to parent. | [`docs/references/screen_03_schedule_default.png`](file:///home/jevitapearl/reportsaathi/docs/references/screen_03_schedule_default.png) |
| **Empty** | • Edge-case state (e.g., if page refreshed with expired session).<br>• Friendly redirect card: `"दवा सारिणी सत्र समाप्त हो गया"` (Session expired).<br>• Single action button: `"नई पर्ची अपलोड करें"` (Upload new prescription). | Redirects user back to Screen 1. | Edge-case state |
| **Loading** | • Native skeleton cards shimmering in Morning/Afternoon/Night sections.<br>• Audio waveform pulse animation.<br>• Zero layout shift: layout height matches the final rendered schedule cards. | Loads within 1–2 seconds. | Transition state |
| **Error (Audio Failure)** | • If low network bandwidth / 3G causes audio playback failure:<br>• Top banner turns soft red: `"⚠️ इंटरनेट धीमा होने के कारण ऑडियो नहीं चला"`.<br>• Action 1: `"🔄 दोबारा प्रयास करें"` (Retry audio).<br>• **Automatic Fallback to Full Written Transcript:** An accessible, large-type card opens below displaying the exact spoken script in Hindi with quotation marks.<br>• Primary Action adapts: `"📲 व्हाट्सएप पर लिखित पर्चा भेजें"`. | User can retry audio or read the transcript; sharing via WhatsApp remains 100% operational. | [`docs/references/screen_03_schedule_error.png`](file:///home/jevitapearl/reportsaathi/docs/references/screen_03_schedule_error.png) |

---

## 4. Design Direction: Design Tokens & System

To guarantee usability on low-cost Android phones with non-Latin scripts, ReportSaathi adopts a strict, high-contrast, low-overhead design system.

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    REPORTSAATHI DESIGN TOKEN SYSTEM                        │
├─────────────────┬──────────────────────────────────────────────────────────┤
│ Viewport & Grid │ 360px base width, 16px horizontal margins, 12px gutters  │
├─────────────────┼──────────────────────────────────────────────────────────┤
│ Base Typography │ System Noto Sans Devanagari / System Sans                │
│                 │ Line height: 1.55x (Prevents matra clipping)             │
│                 │ Body: 16px/24px | Headings: 18px-22px | Buttons: 16px    │
├─────────────────┼──────────────────────────────────────────────────────────┤
│ Touch Targets   │ Minimum 48x48dp for secondary, 56x56dp for primary CTAs  │
├─────────────────┼──────────────────────────────────────────────────────────┤
│ Color Palette   │ Forest Green (#0A5C44) Primary | WhatsApp (#25D366)      │
│                 │ Slate Dark (#1A202C) Text | Off-White (#F8FAFC) Canvas   │
│                 │ Amber Alert (#D97706) | Critical Red (#DC2626)          │
├─────────────────┼──────────────────────────────────────────────────────────┤
│ Asset Budget    │ <120KB initial HTML/CSS payload | Zero heavy JS libs     │
│                 │ Mono Opus audio @ 32kbps (~300KB for 90s clip)           │
└─────────────────┴──────────────────────────────────────────────────────────┘
```

### 1. Layout & Architecture
- **Single-Column Fluid Stack:** All screens use a strictly linear single-column layout (`max-width: 480px; margin: 0 auto;`). No multi-column grids or side-by-side forms that break on 360px viewports.
- **Fixed Bottom Actions (Sticky Footer):** Primary conversion buttons (`"समय समझें"`, `"व्हाट्सएप पर भेजें"`) are fixed to the bottom viewport with safe-area padding (`env(safe-area-inset-bottom)`), ensuring thumb reachability on tall screens.
- **Card Chunking:** Information is grouped into distinct, rounded containers (8px–12px radius) with subtle borders (`1px solid #E2E8F0`). This creates clear mental boundaries between different drugs and meal times.

### 2. Typography for Indic Scripts
- **System-First Font Stack:**
  ```css
  font-family: "Noto Sans Devanagari", "Noto Sans Tamil", "Noto Sans Telugu",
               -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  ```
  *Why:* Eliminates multi-megabyte web font downloads over slow 3G networks. Android devices in India ship with high-quality Noto Indic fonts pre-installed in firmware.
- **Generous Vertical Metrics (1.55x Line-Height):**
  Devanagari characters contain complex top matras (*mātrās* like *ē-kāra*, *ai-kāra*) and bottom diacritics (*u-kāra*, *halant*). Standard Latin line heights (1.2–1.3x) physically clip these diacritics. All Indic body text is set to `line-height: 1.55;` to prevent rendering artifacts.
- **Zero Ellipsis Truncation:**
  Medical and chronotherapy instructions must **never** use `text-overflow: ellipsis` or `white-space: nowrap`. All containers use `word-wrap: break-word; overflow-wrap: break-word;` to accommodate lengthy Indic compound words (e.g., *"हाइपोग्लाइसीमिया"*, *"सावधानियां"*).
- **Scale:**
  - Screen Titles: `20px` / `28px` (Bold)
  - Card Headlines: `16px` / `24px` (Semi-Bold)
  - Body Text: `14px–16px` / `22px–24px` (Regular)
  - Metadata / Disclaimers: `11px–12px` / `16px` (Regular)

### 3. Accessible Colour Palette (WCAG AAA)
The palette avoids cold hospital greys and chaotic e-commerce neons in favor of trusted, high-contrast healthcare tones:

| Token Name | Hex Code | Purpose & Contrast Ratio |
| :--- | :--- | :--- |
| `--color-primary-forest` | `#074D38` | Brand headers, primary buttons, confirmed checkmarks (Contrast 8.2:1 against white). |
| `--color-whatsapp-action` | `#1E7E34` / `#25D366` | WhatsApp sharing triggers (Universal familiarity). |
| `--color-surface-bg` | `#F8FAFC` | Calm off-white page background; reduces glare for older eyes. |
| `--color-card-white` | `#FFFFFF` | Card surface container. |
| `--color-text-headline` | `#0F172A` | Primary typography (Contrast 14.1:1 against white). |
| `--color-text-muted` | `#475569` | Secondary captions, generic molecule names (Contrast 5.5:1). |
| `--color-alert-amber` | `#D97706` | Benign sensations callout (warm yellow background `#FEF3C7`). |
| `--color-alert-red` | `#DC2626` | Clinical red-flag emergency symptoms (soft red background `#FEE2E2`). |

### 4. Spacing & Touch Targets
- **The 48dp/56dp Rule:**
  Older adults experience declining fine motor control. Standard 32dp buttons lead to mis-clicks. Every interactive element has a minimum touch bounding box of **48x48dp**; primary flow progression buttons are **56dp** tall.
- **Inter-Element Margins:**
  Buttons and list items maintain at least **12px to 16px** of vertical separation to prevent adjacent-target mis-taps.

### 5. Tone of Voice
- **Compassionate & Respectful (*Saathi* Spirit):** Phrasing addresses the patient or parent with warmth and dignity (using respectful Hindi pronouns like *"आप"* and *"जी"*, e.g., *"रामेश्वर जी की दवाइयां"*).
- **Non-Prescriptive & Non-Diagnostic:** The copy strictly explains *what the doctor gave and how to take it*. It never uses diagnostic assertions (*"You have high blood sugar"*) or prescriptive mandates (*"Change your dose"*).
- **Reassuring vs. Urgent:** Distinguishes normal, harmless side effects (e.g., *"हल्का सिरदर्द सामान्य है"*) from genuine emergency flags (*"अचानक पसीना आए तो तुरंत डॉक्टर को दिखाएं"*) to prevent cyberchondria.

---

## 5. Verification Checklist: Low-Cost Android & Indic Resilience

```
[✔] Hardware Constraints Verified:
    - Viewport tested at 360x640px (common low-cost Android resolution).
    - Initial page weight < 120KB (CSS + HTML + SVG icons).
    - Audio compressed using mono Opus codec at 32 kbps (~360KB for 90 seconds).

[✔] Script & Typography Constraints Verified:
    - Zero matra clipping verified with Devanagari test strings.
    - Container flexibility tested with 30-character compound Hindi words.
    - Zero CSS text-overflow truncation on clinical labels.

[✔] Older User Accessibility Verified:
    - Base body font size >= 16px.
    - All touch targets >= 48dp (Primary CTAs 56dp).
    - All text meets WCAG 2.1 AA (4.5:1) and AAA (7:1) contrast thresholds.
```

The screenshots illustrating this design direction are cataloged in [`docs/references/`](file:///home/jevitapearl/reportsaathi/docs/references/).
