# System Architecture & Technical Specification: ReportSaathi
*References: `docs/01-problem.md`, `docs/02-research.md`, `docs/03-scope.md`, `docs/04-design.md`, `docs/05-prd.md`*

---

## 1. Architectural Principles & Constraints

To deliver an instant, zero-cost, accessible health explainer on low-cost Android hardware in India, the system follows four architectural tenets:
1. **Clinical Determinism Over Generative Hallucinations:** Clinical advice, meal chronotherapy, and danger warnings are 100% deterministic, governed by a pre-vetted database. AI is strictly constrained to perception tasks (OCR and text-to-speech).
2. **Ephemeral Privacy by Design (DPDP Act 2023 Compliance):** No persistent storage of uploaded prescription images or personal identity. All session data lives in-memory with a 24-hour TTL.
3. **Sub-120KB Payload Budget:** Fast load over 3G cellular connections on budget Android phones without heavy JavaScript frameworks.
4. **100% Free & Open-Source Toolchain:** Zero proprietary API fees; zero recurring WhatsApp Business API charges.

---

## 2. Stack Evaluation & Recommendation

We evaluate two full-stack architectures built entirely on free and open-source foundations.

```
┌────────────────────────────────────────────────────────────────────────────┐
│                        STACK COMPARISON MATRIX                             │
├───────────────────────┬────────────────────────────┬───────────────────────┤
│ Dimension             │ Option A: Fullstack TS     │ Option B: Python      │
│                       │ (Next.js 15 / Node.js)     │ (FastAPI + PWA/HTML5) │
├───────────────────────┼────────────────────────────┼───────────────────────┤
│ Frontend Bundle Size  │ 85KB–160KB (React runtime) │ < 25KB (Vanilla/PWA)  │
├───────────────────────┼────────────────────────────┼───────────────────────┤
│ Low-Cost Android Perf │ Moderate (V8 JS parsing)   │ Maximum (HTML-first)  │
├───────────────────────┼────────────────────────────┼───────────────────────┤
│ OCR & TTS Integration │ External API / C++ bindings│ Native Python bindings│
│                       │ (Tesseract.js is heavy)    │ (PyTesseract, Piper)  │
├───────────────────────┼────────────────────────────┼───────────────────────┤
│ Deterministic Models  │ Zod schemas                │ Pydantic v2 (Fastest) │
├───────────────────────┼────────────────────────────┼───────────────────────┤
│ Free Hosting Memory   │ High (~300MB RAM Node)     │ Low (~120MB RAM)      │
└───────────────────────┴────────────────────────────┴───────────────────────┘
```

### Option A: Fullstack TypeScript (Next.js 15 App Router + Node.js)
- **Frontend:** Next.js / React 19, Tailwind CSS.
- **Backend:** Node.js serverless route handlers.
- **OCR/TTS:** `tesseract.js` (WebAssembly client-side or Node wrapper) + browser Web Speech API.
- **Pros:** Single-language codebase; rapid component development; rich ecosystem.
- **Cons:**
  - `tesseract.js` WASM download is huge (15MB–25MB for language traineddata), crashing low-end Android browsers with 2GB RAM.
  - Browser Web Speech API has inconsistent, robotic Hindi voice quality across fragmented Android OEMs (Xiaomi, Samsung, Realme).
  - Next.js server runtime consumes 250MB–400MB memory, straining free-tier hosting limits.

### Option B: Python Lightweight Backend (FastAPI) + Modern Vanilla JS / PWA *(RECOMMENDED)*
- **Frontend:** Lightweight Semantic HTML5, CSS3 Custom Properties (Design Tokens), Vanilla TypeScript/JavaScript (zero framework overhead, total payload < 25KB).
- **Backend:** FastAPI (Python 3.12, Uvicorn, Pydantic v2).
- **OCR:** Server-side Tesseract OCR v5 (`pytesseract`) / PaddleOCR with optimized Indic language models.
- **TTS:** Piper TTS / Edge-TTS (high-clarity neural Hindi & English voices encoded in 32kbps mono Opus).
- **Data Store:** SQLite with WAL mode (ephemeral in-memory database).
- **Pros:**
  - **Ultra-Lightweight Client:** Total page bundle is < 25KB gzipped. Operates smoothly on entry-level Android devices without UI lag.
  - **Native ML/OCR Capabilities:** Python provides battle-tested bindings for OCR pipelines, image preprocessing (OpenCV / PIL), and neural voice synthesis.
  - **Low Memory Footprint:** FastAPI container runs comfortably within 150MB RAM, fitting easily within free hosting tiers (Render, Fly.io, or Oracle Cloud Free Tier).
- **Cons:** Requires managing frontend and backend codebases, though the frontend is simple enough to be served directly as static assets from FastAPI.

### Recommendation
**Adopt Option B (FastAPI + Lightweight Semantic PWA).**  
It provides the fastest initial load on 3G, eliminates heavy WASM client downloads, and runs native neural audio synthesis with zero third-party API dependencies.

---

## 3. High-Level System Architecture

```
                       REPORTSAATHI SYSTEM TOPOLOGY
                       
 [Low-Cost Android Client]
   │  • Lightweight Semantic HTML5 / CSS Design Tokens (<25KB)
   │  • Client-side image compression (<300KB)
   │  • HTML5 Audio Player & WhatsApp Click-to-Chat URI
   │
   │ HTTPS / TLS 1.3
   ▼
 [FastAPI Gateway / Web Server (Uvicorn)]
   ├── CORS / Rate Limiting / Security Headers
   ├── Ephemeral Session Token Auth (HMAC-SHA256)
   └── Static Asset Serving
         │
         ├──> [Perception Pipeline (AI / ML)]
         │     ├── Image Normalization (OpenCV: Deskew, Contrast)
         │     └── Text Extraction (Tesseract OCR v5 - Eng + Hin)
         │
         ├──> [Deterministic Core (100% Non-AI Code)]
         │     ├── Token Normalizer & Fuzzy Matcher (Levenshtein < 2)
         │     ├── Clinically Validated Top-100 Formulary DB (SQLite)
         │     ├── Regimen Chronotherapy Synthesizer (Morning/Night Rules)
         │     └── Script Template Assembler (Pre-vetted Medical Text)
         │
         ├──> [Audio Engine (AI / Neural Synthesis)]
         │     └── Piper TTS / Edge-TTS (Hindi 'hi_IN', English 'en_IN')
         │         └── Mono Opus Audio Encoder (32 kbps)
         │
         └──> [Ephemeral Cache (In-Memory / SQLite WAL)]
               └── Auto-purge after 24 hours (Zero Persistent PII)
```

---

## 4. Deterministic Code vs. AI Model Matrix

To prevent medical hallucinations, AI is strictly restricted to perception tasks. Clinical logic is 100% deterministic code.

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    DETERMINISTIC VS. AI LOGIC MATRIX                       │
├────────────────────────────┬───────────────┬───────────────────────────────┤
│ System Component           │ Logic Type    │ Operational Implementation    │
├────────────────────────────┼───────────────┼───────────────────────────────┤
│ Image Preprocessing        │ Deterministic │ OpenCV: Grayscale, deskew,    │
│                            │ Code          │ adaptive thresholding.        │
├────────────────────────────┼───────────────┼───────────────────────────────┤
│ Prescription Text OCR      │ AI Model      │ Tesseract OCR v5 / PaddleOCR  │
│                            │               │ neural character recognition. │
├────────────────────────────┼───────────────┼───────────────────────────────┤
│ Drug Candidate Matching    │ Deterministic │ Fuzzy token matching against  │
│                            │ Code          │ whitelisted formulary DB.     │
├────────────────────────────┼───────────────┼───────────────────────────────┤
│ Human Verification Gate    │ Deterministic │ UI check requiring explicit   │
│                            │ Code          │ user confirmation tap.        │
├────────────────────────────┼───────────────┼───────────────────────────────┤
│ Chronotherapy & Scheduling │ Deterministic │ Hardcoded clinical meal rules │
│                            │ Code          │ (Before/With/After food).     │
├────────────────────────────┼───────────────┼───────────────────────────────┤
│ Side Effects & Red Flags   │ Deterministic │ Pre-vetted medical strings;   │
│                            │ Code          │ zero dynamic generation.      │
├────────────────────────────┼───────────────┼───────────────────────────────┤
│ Audio Script Assembly      │ Deterministic │ Mad-lib sentence templating   │
│                            │ Code          │ with verified drug variables. │
├────────────────────────────┼───────────────┼───────────────────────────────┤
│ Audio Voice Synthesis      │ AI Model      │ Piper neural TTS model        │
│                            │               │ generating speech waveforms.  │
├────────────────────────────┼───────────────┼───────────────────────────────┤
│ WhatsApp Link Generator    │ Deterministic │ URI encoding of formatted text│
│                            │ Code          │ and signed access token.      │
└────────────────────────────┴───────────────┴───────────────────────────────┘
```

---

## 5. Ephemeral Data Model (SQLite Schema)

All data is stored in an ephemeral SQLite database with an automated 24-hour cleanup cron job.

```sql
-- 1. Ephemeral Client Session
CREATE TABLE ephemeral_sessions (
    session_id TEXT PRIMARY KEY,           -- UUIDv4
    session_token TEXT NOT NULL,          -- HMAC-SHA256 signature
    language_code TEXT DEFAULT 'hi',      -- 'hi' (Hindi) or 'en' (English)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL         -- Current time + 24 Hours
);

-- 2. Prescription Upload Job
CREATE TABLE prescription_uploads (
    upload_id TEXT PRIMARY KEY,           -- UUIDv4
    session_id TEXT NOT NULL REFERENCES ephemeral_sessions(session_id) ON DELETE CASCADE,
    ocr_raw_text TEXT,                    -- Raw extracted text tokens
    status TEXT NOT NULL,                 -- 'processing', 'completed', 'failed'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Pre-Vetted Clinical Formulary (Read-Only Static Whitelist)
CREATE TABLE formulary_drugs (
    formulary_id TEXT PRIMARY KEY,        -- e.g., 'FORM_MET_GLIM_01'
    brand_aliases TEXT NOT NULL,          -- JSON Array: ["Geminor M2", "Glimisave M2"]
    generic_name TEXT NOT NULL,           -- "Glimepiride (2mg) + Metformin (500mg)"
    therapeutic_category TEXT NOT NULL,   -- 'diabetes', 'hypertension', 'cardiac', 'thyroid'
    chronotherapy_slot TEXT NOT NULL,     -- 'morning_with_food', 'morning_after_food', 'bedtime'
    indication_hi TEXT NOT NULL,          -- "ब्लड शुगर / डायबिटीज नियंत्रण"
    indication_en TEXT NOT NULL,          -- "Blood sugar control"
    meal_instruction_hi TEXT NOT NULL,    -- "नाश्ते के पहले निवाले के साथ लें"
    meal_instruction_en TEXT NOT NULL,    -- "Take with the first bite of breakfast"
    benign_sensations_hi TEXT,            -- "हल्का पेट खराब या मतली सामान्य है"
    benign_sensations_en TEXT,            -- "Mild stomach upset is normal initially"
    red_flags_hi TEXT NOT NULL,           -- "अचानक पसीना छूटे या चक्कर आए तो मीठा खाएं"
    red_flags_en TEXT NOT NULL            -- "If sudden sweating occurs, take sugar immediately"
);

-- 4. User-Confirmed Medication Regimen
CREATE TABLE verified_medications (
    med_id TEXT PRIMARY KEY,              -- UUIDv4
    session_id TEXT NOT NULL REFERENCES ephemeral_sessions(session_id) ON DELETE CASCADE,
    formulary_id TEXT NOT NULL REFERENCES formulary_drugs(formulary_id),
    confirmed_brand_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Synthesized Schedule & Audio Artifact
CREATE TABLE generated_schedules (
    schedule_id TEXT PRIMARY KEY,         -- UUIDv4
    session_id TEXT NOT NULL REFERENCES ephemeral_sessions(session_id) ON DELETE CASCADE,
    schedule_json TEXT NOT NULL,          -- Structured JSON of morning/afternoon/night slots
    audio_path TEXT,                      -- Local filepath to temporary .opus file
    audio_duration_seconds INTEGER,
    share_token TEXT UNIQUE NOT NULL,     -- Cryptographic token for public read-only access
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_expiry ON ephemeral_sessions(expires_at);
CREATE INDEX idx_schedules_share ON generated_schedules(share_token);
```

---

## 6. API Specification & Endpoints

All endpoints use standard JSON payloads and return strict HTTP status codes.

### 1. Initialize Ephemeral Session
- **Endpoint:** `POST /api/v1/sessions`
- **Request:**
  ```json
  { "language_code": "hi" }
  ```
- **Response (201 Created):**
  ```json
  {
    "session_id": "c8b417e2-411a-4d2a-89aa-0e2417d4efb1",
    "session_token": "hmac_signature_string",
    "expires_at": "2026-11-14T12:00:00Z"
  }
  ```

### 2. Upload Prescription Image for Extraction
- **Endpoint:** `POST /api/v1/prescriptions/upload`
- **Headers:** `X-Session-ID`, `X-Session-Token`, `Content-Type: multipart/form-data`
- **Payload:** `file` (Image binary, max 10MB)
- **Response (200 OK):**
  ```json
  {
    "upload_id": "9d1b6cf0-781e-450f-96a9-83561a0d7831",
    "status": "completed",
    "matched_medications": [
      {
        "formulary_id": "FORM_MET_GLIM_01",
        "detected_brand": "Geminor M2",
        "generic_name": "Glimepiride + Metformin",
        "indication": "ब्लड शुगर / डायबिटीज",
        "default_slot": "morning_with_food",
        "confidence": 0.94
      },
      {
        "formulary_id": "FORM_TELVAS_40",
        "detected_brand": "Telvas 40",
        "generic_name": "Telmisartan (40mg)",
        "indication": "ब्लड प्रेशर (BP)",
        "default_slot": "morning_after_food",
        "confidence": 0.89
      }
    ],
    "unmatched_tokens": []
  }
  ```

### 3. Smart Auto-Complete Drug Search
- **Endpoint:** `GET /api/v1/formulary/search?q={query}&lang={hi|en}`
- **Response (200 OK):**
  ```json
  [
    {
      "formulary_id": "FORM_ATORVA_10",
      "brand_name": "Atorva 10",
      "generic_name": "Atorvastatin (10mg)",
      "indication": "कोलेस्ट्रॉल और दिल की सुरक्षा"
    }
  ]
  ```

### 4. Confirm Verified Medication List & Generate Schedule
- **Endpoint:** `POST /api/v1/regimens/decode`
- **Headers:** `X-Session-ID`, `X-Session-Token`
- **Request:**
  ```json
  {
    "confirmed_formulary_ids": ["FORM_MET_GLIM_01", "FORM_TELVAS_40", "FORM_ATORVA_10"]
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "schedule_id": "3e9b1102-39c2-4a0b-96d5-bb909405d452",
    "share_token": "a1f9e8d7c6b5",
    "schedule": {
      "morning": [
        { "name": "Geminor M2", "instruction": "नाश्ते के पहले निवाले के साथ लें" },
        { "name": "Telvas 40", "instruction": "नाश्ता पूरा करने के बाद पानी से लें" }
      ],
      "afternoon": [],
      "night": [
        { "name": "Atorva 10", "instruction": "रात को भोजन के बाद सोने से पहले लें" }
      ],
      "red_flags": [
        "यदि अचानक बहुत तेज पसीना आए या चक्कर आएं तो तुरंत मीठी कैंडी खाएं।"
      ]
    },
    "audio": {
      "audio_url": "/api/v1/audio/3e9b1102-39c2-4a0b-96d5-bb909405d452.opus",
      "duration_seconds": 72,
      "language": "hi"
    },
    "whatsapp_share_url": "https://wa.me/?text=..."
  }
  ```

### 5. Stream Synthesized Audio
- **Endpoint:** `GET /api/v1/audio/{schedule_id}.opus`
- **Response (200 OK):** Audio stream (`Content-Type: audio/ogg; codecs=opus`, `Content-Length: 294912`).

### 6. Public Read-Only View for WhatsApp Recipient
- **Endpoint:** `GET /s/{share_token}`
- **Response (200 OK):** Static semantic HTML rendered with the schedule card and embedded audio player. Zero login or cookie requirements.

---

## 7. Third-Party Services & Open-Source Tools

Every capability is fulfilled using 100% free or open-source software:

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    OPEN-SOURCE CAPABILITY MAPPING                          │
├────────────────────┬───────────────────────────────────┬───────────────────┤
│ Capability         │ Selected Open-Source Tool         │ License & Source  │
├────────────────────┼───────────────────────────────────┼───────────────────┤
│ Image OCR          │ Tesseract OCR v5 + traineddata    │ Apache 2.0        │
│                    │ (Language packs: eng, hin)        │ Google OpenSource │
├────────────────────┼───────────────────────────────────┼───────────────────┤
│ Audio Synthesis    │ Piper TTS (Fast neural voice)     │ MIT License       │
│                    │ Fallback: Edge-TTS Python engine  │ Microsoft Neural  │
├────────────────────┼───────────────────────────────────┼───────────────────┤
│ Image Processing   │ OpenCV-Python (headless) + Pillow │ Apache 2.0 / HPND │
├────────────────────┼───────────────────────────────────┼───────────────────┤
│ Messaging Delivery │ Direct WhatsApp Click-to-Chat URI │ Open Web Standard │
│                    │ (wa.me link generation)           │ (Zero Meta fees)  │
├────────────────────┼───────────────────────────────────┼───────────────────┤
│ Ephemeral Database │ SQLite 3 with WAL Mode            │ Public Domain     │
├────────────────────┼───────────────────────────────────┼───────────────────┤
│ Web Application    │ FastAPI + Uvicorn (ASGI)          │ MIT License       │
└────────────────────┴───────────────────────────────────┴───────────────────┘
```

---

## 8. Deployment & Hosting (Free Tier)

The system is containerized as a single Docker image:
- **Base Image:** `python:3.12-slim-bookworm`
- **OS Packages:** `tesseract-ocr`, `tesseract-ocr-hin`, `ffmpeg`, `libopus0`.
- **Target Free Hosts:**
  - **Option 1 (Recommended):** Oracle Cloud Always Free Compute (VM.Standard.A1.Flex, ARM64, 4 OCPUs, 24GB RAM, forever free). Plenty of headroom for OCR and Piper TTS.
  - **Option 2:** Render.com Free Web Service (512MB RAM, spinning down on idle).
  - **Option 3:** Fly.io Free Launch tier (256MB micro-VM).

---

## 9. Environment Variables (`.env.example`)

```bash
# Server Configuration
ENVIRONMENT="production"
PORT=8000
HOST="0.0.0.0"
BASE_URL="https://reportsaathi.org"

# Security & Session Authentication
# Generate with: openssl rand -hex 32
SESSION_SECRET_KEY="replace_with_secure_64_character_hex_key"
SESSION_TTL_HOURS=24

# OCR & TTS Configuration
TESSERACT_CMD="/usr/bin/tesseract"
TESSDATA_PREFIX="/usr/share/tesseract-ocr/5/tessdata"
PIPER_MODEL_PATH_HI="/app/models/piper/hi_IN-hindi-medium.onnx"
PIPER_MODEL_PATH_EN="/app/models/piper/en_IN-cpc-medium.onnx"

# Storage & Temporary Paths
TEMP_UPLOAD_DIR="/tmp/reportsaathi/uploads"
TEMP_AUDIO_DIR="/tmp/reportsaathi/audio"
SQLITE_DB_PATH="/tmp/reportsaathi/ephemeral.db"

# Safety Limits
MAX_UPLOAD_SIZE_BYTES=10485760 # 10MB
OCR_TIMEOUT_SECONDS=15
```

---

## 10. Open Questions (Unresolved Items)

Rather than making unsupported assumptions, the following operational and technical questions are flagged for resolution during user testing:
1. **WhatsApp URL Length Constraints:** Does WhatsApp for Android on ultra-low-cost devices truncate pre-filled URI strings if the prescription summary exceeds 1,000 characters? *(Needs physical hardware verification on Android Go).*
2. **Offline Audio Playback:** Should the web application register a Service Worker Cache API to allow audio playback to continue if a rural patient loses internet connectivity mid-way through listening?
3. **Regional Dialect Acceptance:** Will older patients in semi-urban Uttar Pradesh and Bihar find standard Modern High Hindi audio natural, or is a colloquial Hindustani phrasing preferred?
4. **Pharma Excipient Nuance:** When patients input combination pills with identical salts but differing release profiles (e.g., Metformin IR vs. Metformin SR/PR), can a simple dropdown prompt clarify this without causing user confusion?
