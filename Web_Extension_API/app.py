from flask import Flask, request, jsonify, render_template
import pandas as pd
import re
from urllib.parse import urlparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.preprocessing import LabelEncoder
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------------- LOAD DATA ----------------
df = pd.read_csv('malicious_phish.csv', nrows=20000)

# ---------------- FEATURE FUNCTIONS ----------------
def contains_ip_address(url):
    return 1 if re.search(r'(\d{1,3}\.){3}\d{1,3}', url) else 0

def abnormal_url(url):
    hostname = urlparse(url).hostname
    return 1 if hostname and hostname in url else 0

def count_dot(url): return url.count('.')
def count_www(url): return url.count('www')
def count_atrate(url): return url.count('@')
def no_of_dir(url): return urlparse(url).path.count('/')
def no_of_embed(url): return urlparse(url).path.count('//')
def count_https(url): return url.count('https')
def count_http(url): return url.count('http')
def count_per(url): return url.count('%')
def count_ques(url): return url.count('?')
def count_hyphen(url): return url.count('-')
def count_equal(url): return url.count('=')
def url_length(url): return len(str(url))
def hostname_length(url): return len(urlparse(url).netloc)

def suspicious_words(url):
    return 1 if re.search('login|bank|account|update|free|bonus', url) else 0

def digit_count(url): return sum(c.isnumeric() for c in url)
def letter_count(url): return sum(c.isalpha() for c in url)

def fd_length(url):
    try:
        return len(urlparse(url).path.split('/')[1])
    except:
        return 0

def shortening_service(url):
    return 1 if re.search('bit\.ly|tinyurl|t\.co|goo\.gl', url) else 0

# ---------------- APPLY FEATURES ----------------
df['use_of_ip'] = df['url'].apply(contains_ip_address)
df['abnormal_url'] = df['url'].apply(abnormal_url)
df['count.'] = df['url'].apply(count_dot)
df['count-www'] = df['url'].apply(count_www)
df['count@'] = df['url'].apply(count_atrate)
df['count_dir'] = df['url'].apply(no_of_dir)
df['count_embed_domian'] = df['url'].apply(no_of_embed)
df['short_url'] = df['url'].apply(shortening_service)
df['count-https'] = df['url'].apply(count_https)
df['count-http'] = df['url'].apply(count_http)
df['count%'] = df['url'].apply(count_per)
df['count?'] = df['url'].apply(count_ques)
df['count-'] = df['url'].apply(count_hyphen)
df['count='] = df['url'].apply(count_equal)
df['url_length'] = df['url'].apply(url_length)
df['hostname_length'] = df['url'].apply(hostname_length)
df['sus_url'] = df['url'].apply(suspicious_words)
df['fd_length'] = df['url'].apply(fd_length)
df['count-digits'] = df['url'].apply(digit_count)
df['count-letters'] = df['url'].apply(letter_count)

# ---------------- LABEL ----------------
lb = LabelEncoder()
df["url_type"] = lb.fit_transform(df["type"])

X = df[['use_of_ip','abnormal_url','count.','count-www','count@',
        'count_dir','count_embed_domian','short_url','count-https',
        'count-http','count%','count?','count-','count=',
        'url_length','hostname_length','sus_url','fd_length',
        'count-digits','count-letters']]

y = df['url_type']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

svm_model = svm.SVC(kernel='linear')
svm_model.fit(X_train, y_train)

# ---------------- FEATURE EXTRACT ----------------
def extract_features(url):
    return [
        contains_ip_address(url),
        abnormal_url(url),
        count_dot(url),
        count_www(url),
        count_atrate(url),
        no_of_dir(url),
        no_of_embed(url),
        shortening_service(url),
        count_https(url),
        count_http(url),
        count_per(url),
        count_ques(url),
        count_hyphen(url),
        count_equal(url),
        url_length(url),
        hostname_length(url),
        suspicious_words(url),
        fd_length(url),
        digit_count(url),
        letter_count(url)
    ]

def predict_url(url):
    f = extract_features(url)
    p = rf.predict([f])[0]
    return lb.inverse_transform([p])[0]

# ---------------- WEB HOME ----------------
@app.route('/')
def home():
    return render_template("index.html")

# ---------------- API ROUTE ----------------
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    url = data.get("url")

    result = predict_url(url)

    if result in ['benign','defacement']:
        msg = "URL IS SAFE!"
    else:
        msg = "URL IS MALICIOUS!"

    # Important: keep both keys so extension & web work
    return jsonify({
        "result": msg,
        "result_str": msg
    })

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)