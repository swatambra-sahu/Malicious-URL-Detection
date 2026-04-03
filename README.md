# ThreatShield — URL Threat Detection

## Introduction

ThreatShield is a URL threat detection system powered by a `RandomForestClassifier` (scikit-learn) trained on ~651K URLs (with stratified sampling capping each class at 100K rows) from the `malicious_phish.csv` dataset. It classifies URLs into four categories — **Benign**, **Phishing**, **Malware**, and **Defacement** — and returns a confidence score.

The project includes three components:
- **Flask Backend** (`Web_Extension_API/app.py`) — serves the `/predict` API and trains the model at startup.
- **Web UI** (`Web_Extension_API/templates/index.html`) — a dark-themed single-page application with a URL scanner and front-end login/signup.
- **Chrome Extension** (`Web_Extension_API/popup.html`, `popup.js`, `popup.css`, `manifest.json`) — a Manifest V3 extension with matching dark theme, auto tab-URL detection, and persistent scan history.

### Why URL Threat Detection?

The risk of malicious URLs lies in the fact that they can be used by attackers to carry out a wide range of cyber attacks, including phishing attacks, malware distribution, and credential harvesting. By using machine learning, it is possible to identify and classify malicious URLs, enabling security professionals to block them before they can cause harm.

## Technology Stack

| Component | Technology |
|---|---|
| ML Model | `RandomForestClassifier` (scikit-learn) |
| Backend | Flask, pandas, numpy |
| Web UI | Tailwind CSS (CDN), Lucide icons, dark theme (`#0a0e17` bg, `#00ff88` accent) |
| Chrome Extension | Manifest V3, `chrome.storage.local`, `chrome.tabs` API |
| Dataset | `malicious_phish.csv` (~651K URLs) |

## Architecture

### Flask Backend (`Web_Extension_API/app.py`)
- Serves the `/predict` API endpoint — accepts a URL, returns `result_str`, `predicted_class`, and `confidence`.
- Trains the `RandomForestClassifier` at startup using the full dataset with stratified sampling (max 100K rows per class).
- Includes a trusted domain whitelist for known legitimate domains (Google, Amazon, Microsoft, etc.) that bypasses ML classification.
- Serves the web UI via Flask template rendering.

### Web UI (`Web_Extension_API/templates/index.html`)
- Single-page application with a dark theme (`#0a0e17` background, `#00ff88` accent).
- Front-end-only login/signup flow using `localStorage` (stored under the key `ts_user`) — no backend authentication.
- URL scanner with scan history and result display showing predicted category and confidence.

### Chrome Extension (`Web_Extension_API/popup.*`, `manifest.json`)
- Manifest V3 extension named "ThreatShield" that communicates with the Flask `/predict` endpoint.
- Matching dark theme, auto-detects the current tab's URL on popup open.
- Stores the last 5 scan results in `chrome.storage.local` for persistent history.
- 10-second fetch timeout via `AbortController`, auto-prepends `https://` to bare domain inputs.

## Methodology
The project has been divided into 4 parts:
<details>
  <summary> 1. Data Acquisition: </summary>

The source of the dataset is https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset?resource=download
This file consists of 651,191 URLs, out of which 428103 benign or safe URLs, 96457 defacement URLs, 94111 phishing URLs, and 32520 malware URLs. It has two columns comprising of url and a type which signifies the class of maliciousness.

    * Defacement URLs are URLs of websites that have been hacked and their content has been replaced or modified by the hacker.
    
    * Phishing URLs are malicious websites that are designed to deceive users into giving sensitive information.
    
    * Malware URLs are URLs that host or distribute malware, which refers to malicious software designed to harm or exploit computer systems. Malware can include viruses, Trojans, ransomware, spyware, and other types of harmful software. 
</details>

<details>
  <summary> 2. Data Preprocessing/Feature Engineering: </summary>
  The success of any ML model depends on the quality of training data and the quality of features fed into the model. Certain features must be available to analysts in order to create proactive models to identify malicious URLs. Simple URL strings can be used to extract these features, which can be lexical, content, or network. In this project, only lexical features are being used. 
  
  The lexical features include the elements of the URL string. They are determined by how the URL looks or seems different in users’ eyes and the URL’s textual properties. These include statistical properties such as the length of the URL, length of the domain, number of special characters, and number of digits in the URL.
  
* contains_ip_address: Generally cyber attackers use an IP address in place of the domain name to hide the identity of the website. this feature will check whether the URL has IP address or not.
* abnormal_url: This feature can be extracted from the WHOIS database. For a legitimate website, identity is typically part of its URL.
* google_index: In this feature, we check whether the URL is indexed in google search console or not.
* Count . : The phishing or malware websites generally use more than two sub-domains in the URL. Each domain is separated by dot (.). If any URL contains more than three dots(.), then it increases the probability of a malicious site.
* Count-www: Generally most of the safe websites have one www in its URL. This feature helps in detecting malicious websites if the URL has no or more than one www in its URL.
* count@: The presence of the “@” symbol in the URL ignores everything previous to it.
* Count_dir: The presence of multiple directories in the URL generally indicates suspicious websites.
* Count_embed_domain: The number of the embedded domains can be helpful in detecting malicious URLs. It can be done by checking the occurrence of “//” in the URL.
* Suspicious words in URL: Malicious URLs generally contain suspicious words in the URL such as PayPal, login, sign in, bank, account, update, bonus, service, ebayisapi, token, etc. We have found the presence of such frequently occurring suspicious words in the URL as a binary variable i.e., whether such words present in the URL or not.
* Short_url: This feature is created to identify whether the URL uses URL shortening services like bit. \ly, goo.gl, go2l.ink, etc.
* Count_https: Generally malicious URLs do not use HTTPS protocols as it generally requires user credentials and ensures that the website is safe for transactions. So, the presence or absence of HTTPS protocol in the URL is an important feature.
* Count_http: Most of the time, phishing or malicious websites have more than one HTTP in their URL whereas safe sites have only one HTTP.
* Count%: As we know URLs cannot contain spaces. URL encoding normally replaces spaces with symbol (%). Safe sites generally contain less number of spaces whereas malicious websites generally contain more spaces in their URL hence more number of %.
* Count?: The presence of symbol (?) in URL denotes a query string that contains the data to be passed to the server. More number of ? in URL definitely indicates suspicious URL.
* Count-: Phishers or cybercriminals generally add dashes(-) in prefix or suffix of the brand name so that it looks genuine URL.
* Count=: Presence of equal to (=) in URL indicates passing of variable values from one form page t another. It is considered as riskier in URL as anyone can change the values to modify the page.
* url_length: Attackers generally use long URLs to hide the domain name. We found the average length of a safe URL is 74.
* hostname_length: The length of the hostname is also an important feature for detecting malicious URLs.
* First directory length: This feature helps in determining the length of the first directory in the URL. So looking for the first ‘/’ and counting the length of the URL up to this point helps in finding the first directory length of the URL. For accessing directory level information we need to install python library TLD. You can check this link for installing TLD.
* Length of top-level domains: A top-level domain (TLD) is one of the domains at the highest level in the hierarchical Domain Name System of the Internet. For example, in the domain name www.example.com, the top-level domain is com. So, the length of TLD is also important in identifying malicious URLs. As most of the URLs have .com extension. TLDs in the range from 2 to 3 generally indicate safe URLs.
* Count_digits: The presence of digits in URL generally indicate suspicious URLs. Safe URLs generally do not have digits so counting the number of digits in URL is an important feature for detecting malicious URLs.
* Count_letters: The number of letters in the URL also plays a significant role in identifying malicious URLs. As attackers try to increase the length of the URL to hide the domain name and this is generally done by increasing the number of letters and digits in the URL.

  
</details>

<details>
  <summary> 3. Machine Learning </summary>

The production model used in ThreatShield is **Random Forest**, which is a machine-learning algorithm used for classification, regression, and other tasks. It is an ensemble learning method that works by combining multiple decision trees to make predictions. It is resistant to overfitting and performs well on complex datasets.

During initial research, SVM and XGBoost were also evaluated. SVM was later removed from the production backend because its O(n²)–O(n³) training complexity made it impractical on the full ~651K-row dataset (causing server startup to hang indefinitely). Random Forest was chosen for its balance of accuracy (99.18%) and training speed.

</details>

<details>
  <summary> 4. Results </summary>
Evaluation Metric: Accuracy (the percentage of correct decisions among all correct samples)
  
  The accuracy obtained from the models are: 
  
  SVM Accuracy: 95.73%
  Random Forest Accuracy: 99.18%
  XGBoost Accuracy: 97.92%
 
</details>

<details>
  <summary> 5. Conclusion </summary>


  The Random Forest algorithm has proven to be effective in detecting malicious URLs in the current dataset. The model has been deployed in the ThreatShield application — accessible via both a web UI and a Chrome extension — providing real-time URL threat detection. The trusted domain whitelist adds an additional layer of accuracy for well-known legitimate domains.

  There is always room for improvement. By introducing network features, we can gain a better understanding of the URLs' behavior and potentially improve the classification accuracy. Fine-tuning hyperparameters and expanding the dataset can further enhance performance.

</details>

## Setup & Run

For detailed setup instructions (virtual environment, dependencies, running the Flask server, and loading the Chrome extension), see **[`Web_Extension_API/HOW_TO_RUN.md`](Web_Extension_API/HOW_TO_RUN.md)**.

**Quick start:**
```sh
cd Web_Extension_API
pip install -r requirements.txt
python app.py
```
Then open **http://127.0.0.1:5000** in your browser.

## Known Notes

- **Startup time**: The Flask server takes ~1–2 minutes to start because the RandomForest model trains on ~651K rows at startup.
- **Bare domains**: The Chrome extension auto-prepends `https://` to inputs like `amazon.com` to avoid `urlparse` issues in the backend. For best results, always include the scheme.
- **Login/signup**: The authentication flow in the web UI is front-end only — stored in `localStorage` under `ts_user`. There is no backend authentication.
- **Chrome extension permissions**: Requires `tabs`, `storage`, `activeTab`, and `scripting` permissions, plus host access to `http://127.0.0.1:5000/*`.
