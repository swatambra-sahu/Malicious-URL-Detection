
## 📌 Overview

**ThreatShield** is an end-to-end malicious URL detection system that uses a **Random Forest classifier** trained on **651,191 real-world URLs** to classify web addresses into four threat categories — **Benign**, **Phishing**, **Malware**, and **Defacement** — with **99.18% accuracy**.

The system extracts **20 lexical features** from raw URL strings (no external API calls or page rendering required), making classification **instantaneous and privacy-preserving**. Users interact with the model through a sleek **dark-themed Web UI** or a **Chrome Extension** that auto-scans the current tab.

### Why This Matters

> Malicious URLs are the #1 delivery mechanism for phishing, malware distribution, and credential harvesting attacks. Traditional blacklist-based approaches fail against zero-day threats. ThreatShield demonstrates that **machine learning can proactively identify malicious URLs** from their structural patterns alone — no page content analysis needed.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Real-Time Detection** | Classifies any URL in milliseconds via REST API |
| 🤖 **ML-Based Classification** | Random Forest trained on 651K URLs with 99.18% accuracy |
| 🧬 **20 Lexical Features** | Extracts structural URL patterns — no external lookups needed |
| 🌐 **Flask Web UI** | Dark-themed single-page app with scan history & login flow |
| 🧩 **Chrome Extension** | Manifest V3 extension with auto tab-URL detection |
| ✅ **Trusted Domain Whitelist** | Instant bypass for known-safe domains (Google, Amazon, etc.) |
| 📊 **Confidence Scoring** | Returns prediction probability alongside the classification |
| 🏠 **Localhost + Deployed** | Two extension variants — local dev and pythonanywhere-hosted |

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.8+ |
| **ML Framework** | Scikit-learn (RandomForestClassifier) |
| **Data Processing** | Pandas, NumPy |
| **Backend API** | Flask, Flask-CORS |
| **Web UI** | HTML5, Tailwind CSS (CDN), Lucide Icons |
| **Chrome Extension** | Manifest V3, chrome.storage, chrome.tabs API |
| **Visualization** | Matplotlib, WordCloud |
| **Serialization** | Pickle (model + label encoder) |
| **Deployment** | PythonAnywhere (cloud), localhost (dev) |

---

## 🔄 Project Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        USER INTERACTION LAYER                        │
│                                                                      │
│   ┌─────────────────────┐       ┌──────────────────────────────┐    │
│   │   Chrome Extension  │       │       Flask Web UI            │    │
│   │   (Manifest V3)     │       │   (templates/index.html)      │    │
│   │                     │       │                                │    │
│   │  • Auto-detect URL  │       │  • URL scanner form           │    │
│   │  • Scan history     │       │  • Scan history dashboard     │    │
│   │  • Dark theme UI    │       │  • Frontend auth (localStorage│    │
│   └────────┬────────────┘       └──────────────┬─────────────────┘    │
│            │                                   │                     │
│            │        POST /predict               │                     │
│            │        { "url": "..." }            │                     │
│            └──────────────┬─────────────────────┘                     │
└───────────────────────────┼──────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        FLASK BACKEND (app.py)                        │
│                                                                      │
│   1. Receive URL via POST /predict                                   │
│   2. Check Trusted Domain Whitelist ──→ If trusted → return "benign" │
│   3. Extract 20 lexical features from the URL string                 │
│   4. Feed feature vector to trained RandomForest model               │
│   5. Return JSON: { result_str, predicted_class, confidence }        │
└──────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     ML MODEL LAYER                                   │
│                                                                      │
│   RandomForestClassifier (100 estimators, random_state=42)           │
│   Trained on ~651K URLs with stratified sampling (max 100K/class)    │
│                                                                      │
│   Input:  20-feature vector (lexical URL properties)                 │
│   Output: Class label (benign/phishing/malware/defacement)           │
│           + Confidence score (probability %)                         │
└──────────────────────────────────────────────────────────────────────┘
```

### System Flow

```
User enters URL → Extension/Web UI sends POST request → Flask backend receives URL
→ Trusted domain check → Feature extraction (20 lexical features)
→ Random Forest prediction → Returns class + confidence → UI displays result
```

---

## 📊 Dataset

| Property | Detail |
|---|---|
| **Source** | [Kaggle — Malicious URLs Dataset](https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset) |
| **Total URLs** | **651,191** |
| **Columns** | `url` (string), `type` (class label) |
| **Classes** | 4 — Benign, Defacement, Phishing, Malware |

### Class Distribution

| Category | Count | Description |
|---|---|---|
| **Benign** | 428,103 (65.7%) | Legitimate, safe URLs |
| **Defacement** | 96,457 (14.8%) | Hacked/modified website URLs |
| **Phishing** | 94,111 (14.5%) | URLs designed to steal credentials |
| **Malware** | 32,520 (5.0%) | URLs hosting/distributing malicious software |

> **Note:** Stratified sampling caps each class at 100,000 rows during backend training to manage memory while maintaining balanced representation.

---

## 🧬 Feature Engineering

ThreatShield extracts **20 lexical features** directly from the URL string — no network requests, page rendering, or WHOIS lookups required:

| # | Feature | Rationale |
|---|---|---|
| 1 | `use_of_ip` | Attackers use raw IP addresses to hide domain identity |
| 2 | `abnormal_url` | Checks if hostname matches the URL (WHOIS-inspired) |
| 3 | `count.` | More dots → more subdomains → higher suspicion |
| 4 | `count-www` | Safe URLs typically have exactly one `www` |
| 5 | `count@` | `@` in URLs causes browsers to ignore everything before it |
| 6 | `count_dir` | Multiple directory levels suggest obfuscation |
| 7 | `count_embed_domain` | Embedded `//` indicates hidden redirects |
| 8 | `short_url` | URL shorteners (bit.ly, tinyurl) hide malicious targets |
| 9 | `count-https` | Legitimate sites use HTTPS; malicious ones often don't |
| 10 | `count-http` | Multiple `http` occurrences indicate suspicious structure |
| 11 | `count%` | URL-encoded spaces (%) are common in malicious URLs |
| 12 | `count?` | Excessive query parameters suggest data exfiltration |
| 13 | `count-` | Hyphens in domains mimic legitimate brand names |
| 14 | `count=` | Assignment operators enable parameter manipulation |
| 15 | `url_length` | Attackers use long URLs to obscure the real domain |
| 16 | `hostname_length` | Longer hostnames correlate with malicious intent |
| 17 | `sus_url` | Presence of keywords: "login", "bank", "PayPal", etc. |
| 18 | `fd_length` | Length of the first directory path segment |
| 19 | `count-digits` | Excessive digits suggest auto-generated domains |
| 20 | `count-letters` | Inflated letter counts indicate obfuscation attempts |

---

## 🤖 Model Details

### Models Evaluated

| Model | Accuracy | Training Feasibility | Production Status |
|---|---|---|---|
| **Random Forest** | **99.18%** | ✅ Fast (~1-2 min on 651K rows) | ✅ **Production** |
| **XGBoost** | 97.92% | ✅ Fast | ⚙️ Evaluated |
| **SVM (Linear)** | 95.73% | ❌ O(n²)–O(n³) on 651K rows | ❌ Removed |

### Why Random Forest?

1. **Highest accuracy** — 99.18% on the test set, outperforming both SVM and XGBoost
2. **Ensemble robustness** — Combines 100 decision trees, reducing overfitting on complex URL patterns
3. **Fast inference** — Millisecond-level predictions, critical for real-time Chrome extension use
4. **Feature importance** — Built-in feature ranking helps understand which URL traits are most suspicious
5. **Practical training time** — Trains on 651K URLs in ~1-2 minutes (vs. SVM which hung indefinitely)

### Why SVM Was Removed

SVM's O(n²)–O(n³) training complexity made it impractical for the full dataset. The Flask server trains the model at startup — SVM caused the server to hang indefinitely, making deployment impossible.

---

## 📈 Results

### Accuracy Comparison

| Model | Accuracy |
|---|---|
| 🏆 **Random Forest** | **99.18%** |
| XGBoost | 97.92% |
| SVM (Linear) | 95.73% |

> **Evaluation Metric:** Accuracy — the percentage of correct predictions across all test samples (stratified 80/20 train-test split with `random_state=42`).

### Key Takeaway

The Random Forest model correctly classifies **over 99 out of every 100 URLs** in the test set, while maintaining fast-enough training for server-startup deployment. This makes it ideal for real-time threat detection in resource-constrained browser extensions.

---

## 🚀 Installation

### Prerequisites

- **Python 3.8+** installed on your system
- **pip** package manager
- **Google Chrome** or **Brave** browser (for the extension)
- **Git** (to clone the repository)

### Step 1 — Clone the Repository

```bash
git clone https://github.com/swatambra-sahu/Malicious-URL-Detection.git
cd Malicious-URL-Detection
```

### Step 2 — Set Up Virtual Environment

```bash
python3 -m venv env
```

Activate it:

```bash
# macOS / Linux
source env/bin/activate

# Windows
env\Scripts\activate
```

### Step 3 — Install Dependencies

```bash
cd Web_Extension_API_localhost
pip install -r requirements.txt
```

> **Dependencies:** flask, flask-cors, pandas, scikit-learn

### Step 4 — Run the Flask Server

```bash
python app.py
```

> ⚠️ **Note:** The server takes **~1-2 minutes to start** because the Random Forest model trains on ~651K rows at startup. Wait until you see `Running on http://127.0.0.1:5000` in the terminal.

### Step 5 — Open the Web UI

Navigate to **http://127.0.0.1:5000** in your browser.

### Step 6 — Load the Chrome Extension (Optional)

1. Open `chrome://extensions/` (or `brave://extensions/`)
2. Enable **Developer Mode** (toggle in top-right)
3. Click **"Load unpacked"**
4. Select the `Web_Extension_API_localhost/` folder
5. Pin the ThreatShield extension and click it to scan URLs

---

## 💻 Usage

### Scanning a URL via Web UI

1. Start the Flask server (`python app.py`)
2. Open `http://127.0.0.1:5000`
3. Enter a URL in the scanner input field
4. Click **"Scan URL"** or press **Enter**
5. View the result: threat category + confidence score

### Scanning via Chrome Extension

1. Ensure the Flask server is running
2. Click the ThreatShield extension icon in your toolbar
3. The current tab's URL is **auto-filled**
4. Click **"Scan URL"** — results appear inline with scan history

### API Usage (Direct)

```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

**Response:**
```json
{
  "result": "URL IS SAFE!",
  "result_str": "URL IS SAFE!",
  "predicted_class": "benign",
  "confidence": 100
}
```

### Running the Training Script (Standalone)

```bash
# From project root, activate env first
source env/bin/activate
pip install -r requirements.txt
python MaliciousURLDetection.py
```

This trains SVM, Random Forest, and (optionally) XGBoost, then saves `model.pkl` and `label_encoder.pkl` to the project root.

### Running the Data Exploration Script

```bash
python loadData.py
```

Generates word clouds for each URL category (Benign, Phishing, Malware, Defacement).

---

## 📁 Folder Structure

```
Malicious-URL-Detection/
│
├── 📄 README.md                          # This file — project documentation
├── 📄 RUN.md                             # Step-by-step execution guide
├── 📄 PROJECT_REPORT.md                  # Detailed academic project report
├── 📄 requirements.txt                   # Root-level Python dependencies
├── 📄 .gitignore                         # Git ignore rules
│
├── 📊 Dataset/
│   └── malicious_phish.csv               # Full dataset (651K URLs, ~45 MB)
│
├── 🐍 MaliciousURLDetection.py           # ML training script — SVM, Random Forest, XGBoost
├── 🐍 loadData.py                        # Data exploration + word cloud generation
├── 📓 MaliciousURLDetection.ipynb        # Jupyter notebook (interactive version)
├── 📓 loadData.ipynb                     # Jupyter notebook for data loading/visualization
│
├── 🧠 model.pkl                          # Serialized Random Forest model (~9.3 MB)
├── 🏷️ label_encoder.pkl                  # Serialized LabelEncoder for class mapping
│
├── 🌐 Web_Extension_API_localhost/       # Flask backend + Chrome extension (LOCAL)
│   ├── app.py                            # Flask server with /predict endpoint
│   ├── app.ipynb                         # Notebook version of the backend
│   ├── requirements.txt                  # Backend-specific dependencies
│   ├── malicious_phish.csv               # Dataset copy for backend training
│   ├── templates/
│   │   └── index.html                    # Web UI (dark-themed SPA)
│   ├── manifest.json                     # Chrome extension manifest (localhost)
│   ├── popup.html                        # Extension popup HTML
│   ├── popup.js                          # Extension logic + API calls
│   ├── popup.css                         # Extension styling (dark theme)
│   ├── background.js                     # Extension background service worker
│   ├── icon.png / icon1.png / icon2.png  # Extension icons
│   └── HOW_TO_RUN.md                     # Detailed setup guide for this component
│
├── ☁️ Web_Extension_API_Deployed/        # Flask backend + Chrome extension (DEPLOYED)
│   ├── (same structure as localhost)      # Points to pythonanywhere.com backend
│   └── manifest.json                     # host_permissions → pythonanywhere URL
│
├── 📐 diagrams/                          # System architecture diagrams (.drawio)
│   ├── 01_system_architecture.drawio
│   ├── 02_dfd_level0.drawio
│   ├── 03_dfd_level1.drawio
│   ├── 04_dfd_level2.drawio
│   ├── 05_sequence_diagram.drawio
│   ├── 06_use_case_diagram.drawio
│   ├── 07_er_diagram.drawio
│   ├── 08_block_diagram.drawio
│   ├── 09_activity_diagram.drawio
│   └── 10_component_diagram.drawio
│
└── 📄 Leveraging_Machine_Learning_for_   # Reference research paper (text)
    Threat_Detection_....txt
```

---

## 🌟 Why This Project Is Impressive

### For Recruiters & Evaluators

- **End-to-end ML pipeline** — From raw data → feature engineering → model training → API serving → browser-native deployment
- **Production-grade architecture** — REST API, CORS handling, trusted domain whitelist, confidence scoring
- **Real-world deployment** — Hosted on PythonAnywhere with a fully functional Chrome Extension (Manifest V3)
- **99.18% accuracy** on a 651K-row real-world dataset — not a toy project

### How It Stands Out

| Traditional Projects | ThreatShield |
|---|---|
| Train a model in a notebook | **Deploys the model as a live API** |
| Show accuracy metrics | **Users scan real URLs in real-time** |
| Static analysis | **Chrome Extension with auto-URL detection** |
| Single model | **Evaluated 3 models, chose the best for production** |
| No deployment | **Deployed on PythonAnywhere + Chrome Web Store ready** |

> *"This project demonstrates real-world ML deployment — from research to a cybersecurity tool that users can install in their browser."*

---

## 🔮 Future Improvements

- [ ] **Deep Learning models** — Train LSTM/CNN on raw URL character sequences for even higher accuracy
- [ ] **Network features** — Add WHOIS age, DNS records, SSL certificate info for richer feature sets
- [ ] **Real-time model updates** — Implement online learning to adapt to emerging threats
- [ ] **Batch scanning** — Support scanning multiple URLs simultaneously via CSV upload
- [ ] **Browser notification alerts** — Proactive warnings when navigating to malicious sites
- [ ] **User feedback loop** — Allow users to report false positives/negatives to improve the model
- [ ] **Mobile app** — React Native wrapper for on-the-go URL scanning
- [ ] **Threat intelligence integration** — Cross-reference with VirusTotal, Google Safe Browsing APIs

---

## ⚠️ Known Notes

- **Startup time** — The Flask server takes ~1-2 minutes to start because the model trains on ~651K rows at startup.
- **Bare domains** — The Chrome extension auto-prepends `https://` to inputs like `amazon.com`. For best results, always include the scheme (`https://`).
- **Login/signup** — The web UI authentication is front-end only (localStorage). There is no backend auth.
- **Extension permissions** — Requires `tabs`, `storage`, `activeTab`, and `scripting` permissions + host access to the API URL.

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ for Cybersecurity**

*ThreatShield — Because every click deserves protection.*

</div>
]]>
