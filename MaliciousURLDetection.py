import pandas as pd
import re
from urllib.parse import urlparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import svm, metrics
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import pickle

# ---------------- LOAD DATA ----------------
df = pd.read_csv('Dataset/malicious_phish.csv', nrows=20000)

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
    return 1 if re.search(r'login|bank|account|update|free|bonus', url) else 0

def digit_count(url): return sum(c.isnumeric() for c in url)
def letter_count(url): return sum(c.isalpha() for c in url)

def fd_length(url):
    try:
        return len(urlparse(url).path.split('/')[1])
    except:
        return 0

def shortening_service(url):
    return 1 if re.search(r'bit\.ly|tinyurl|t\.co|goo\.gl', url) else 0

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

# ---------------- SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

# ---------------- SVM ----------------
svm_model = svm.SVC(kernel='linear')
svm_model.fit(X_train, y_train)
y_pred = svm_model.predict(X_test)

print("SVM Accuracy:", metrics.accuracy_score(y_test, y_pred))

# ---------------- FEATURE IMPORTANCE ----------------
importances = abs(svm_model.coef_[0])

plt.figure(figsize=(10,5))
plt.bar(range(len(importances)), importances)
plt.xticks(range(len(importances)), X.columns, rotation=90)
plt.title("Feature Importance (SVM)")
plt.tight_layout()
plt.show()

# ---------------- RANDOM FOREST ----------------
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

print("Random Forest Accuracy:", metrics.accuracy_score(y_test, y_pred_rf))

# ---------------- SAVE MODEL ----------------
pickle.dump(rf, open("model.pkl", "wb"))
pickle.dump(lb, open("label_encoder.pkl", "wb"))

print("Model saved successfully!")

# ---------------- OPTIONAL XGBOOST ----------------
try:
    import xgboost as xgb

    xgb_model = xgb.XGBClassifier(
        learning_rate=0.1,
        max_depth=3,
        n_estimators=100,
        eval_metric='mlogloss'
    )

    xgb_model.fit(X_train, y_train)
    y_pred_xgb = xgb_model.predict(X_test)

    print("XGBoost Accuracy:", metrics.accuracy_score(y_test, y_pred_xgb))

except:
    print("XGBoost not installed — skipping.")