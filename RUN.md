<![CDATA[# 🚀 ThreatShield — Execution Guide

> **A beginner-friendly, step-by-step guide to running every component of ThreatShield.**
> All commands are copy-paste ready. Follow them in order.

---

## 📋 Prerequisites

Before you begin, make sure you have:

- [x] **Python 3.8+** — Check: `python3 --version`
- [x] **pip** — Check: `pip --version`
- [x] **Git** — Check: `git --version`
- [x] **Google Chrome** or **Brave** browser (for the extension)

---

## Part 1: Running the ML Training Script

> This trains the models (SVM, Random Forest, XGBoost) and saves `model.pkl`.

### Step 1 — Clone & Navigate

```bash
git clone https://github.com/swatambra-sahu/Malicious-URL-Detection.git
cd Malicious-URL-Detection
```

### Step 2 — Create & Activate Virtual Environment

```bash
python3 -m venv env
```

**macOS / Linux:**
```bash
source env/bin/activate
```

**Windows:**
```bash
env\Scripts\activate
```

> ✅ You should see `(env)` at the start of your terminal prompt.

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Run the Training Script

```bash
python3 MaliciousURLDetection.py
```

**Expected Output:**
```
SVM Accuracy: 0.9573...
Random Forest Accuracy: 0.9918...
Model saved successfully!
XGBoost Accuracy: 0.9792...     # (only if xgboost is installed)
```

> 📦 This generates `model.pkl` and `label_encoder.pkl` in the project root.

### Step 5 — Deactivate (When Done)

```bash
deactivate
```

---

## Part 2: Running the Data Exploration Script

> This visualizes the dataset and generates word clouds for each URL category.

```bash
source env/bin/activate        # Activate env if not already active
pip install wordcloud           # Install wordcloud dependency
python3 loadData.py
deactivate
```

> 📊 Word clouds will pop up for Benign, Phishing, Malware, and Defacement URLs.

---

## Part 3: Running the Flask Backend + Web UI

> This starts the live API server and web interface.

### Step 1 — Navigate to the Backend Folder

```bash
cd Web_Extension_API_localhost
```

### Step 2 — Create & Activate Virtual Environment

```bash
python3 -m venv env
source env/bin/activate         # macOS/Linux
# env\Scripts\activate          # Windows
```

### Step 3 — Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Run the Flask Server

```bash
python3 app.py
```

> ⏳ **Wait ~1-2 minutes** — The server trains the Random Forest model on ~651K URLs at startup.

**Expected Terminal Output:**
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Step 5 — Open the Web UI

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

Enter any URL in the scanner and click **"Scan URL"** to test!

### Step 6 — Stop the Server

Press `Ctrl + C` in the terminal to stop the server.

```bash
deactivate                      # Exit the virtual environment
```

---

## Part 4: Loading the Chrome Extension

> This adds ThreatShield as a browser extension with one-click scanning.

### Prerequisites

- ✅ Flask server must be **running** (see Part 3 above)

### Step 1 — Open Extension Manager

- **Chrome:** Go to `chrome://extensions/`
- **Brave:** Go to `brave://extensions/`

### Step 2 — Enable Developer Mode

Toggle **"Developer mode"** ON (top-right corner of the page).

### Step 3 — Load the Extension

1. Click **"Load unpacked"**
2. Select the **`Web_Extension_API_localhost/`** folder
3. ThreatShield will appear in your extensions list

### Step 4 — Pin & Use

1. Click the **puzzle piece icon** 🧩 in the Chrome toolbar
2. Click the **pin icon** 📌 next to ThreatShield
3. Click the **ThreatShield icon** — it auto-fills the current tab's URL
4. Click **"Scan URL"** or press **Enter**

### Step 5 — Remove the Extension (When Done)

1. Go to `chrome://extensions/`
2. Find ThreatShield
3. Click **"Remove"**

---

## Part 5: Using the Deployed Version

> ThreatShield is also deployed on PythonAnywhere — no local server needed.

### Load the Deployed Extension

1. Go to `chrome://extensions/`
2. Enable **Developer Mode**
3. Click **"Load unpacked"**
4. Select the **`Web_Extension_API_Deployed/`** folder

> 🌐 This version connects to `https://swatambra.pythonanywhere.com/predict` — no local server required.

---

## Part 6: Running Jupyter Notebooks

> Interactive notebooks for exploring data and training models.

```bash
source env/bin/activate
pip install jupyter
```

### ML Training Notebook

```bash
jupyter notebook MaliciousURLDetection.ipynb
```

### Data Loading Notebook

```bash
jupyter notebook loadData.ipynb
```

### Backend Notebook

```bash
cd Web_Extension_API_localhost
jupyter notebook app.ipynb
```

---

## 🔧 Troubleshooting

| Issue | Solution |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` inside the activated virtual environment |
| Server hangs on startup | Normal — wait 1-2 minutes for model training to complete |
| Extension shows "Connection Failed" | Ensure the Flask server is running on `http://127.0.0.1:5000` |
| `TkAgg` error with `loadData.py` | Install tkinter: `brew install python-tk` (macOS) or `sudo apt install python3-tk` (Linux) |
| XGBoost not found | Install it: `pip install xgboost` (optional — only needed for XGBoost evaluation) |
| Port 5000 already in use | Kill the existing process: `lsof -i :5000` then `kill -9 <PID>` |

---

## 📝 Quick Reference Commands

```bash
# Full setup from scratch (localhost)
git clone https://github.com/swatambra-sahu/Malicious-URL-Detection.git
cd Malicious-URL-Detection/Web_Extension_API_localhost
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3 app.py
# → Open http://127.0.0.1:5000 in browser
```

```bash
# Quick restart (if env already exists)
cd Malicious-URL-Detection/Web_Extension_API_localhost
source env/bin/activate
python3 app.py
```

---

<div align="center">

*Need help? Open an issue on GitHub or contact the maintainer.*

</div>
]]>
