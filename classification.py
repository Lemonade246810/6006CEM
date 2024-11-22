# -*- coding: utf-8 -*-
"""Classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-W6CUKQVMv79RBZXh4lgdlMAaLzQzuxW
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
url = "flight_delays.csv"
df = pd.read_csv(url)
df

# Step 1: Data Preprocessing
# Handling missing values by dropping rows where 'DelayMinutes' is null since it's the target variable
df_clean = df.dropna(subset=['DelayMinutes'])

# Filling missing values for DelayReason
df_clean['DelayReason'].fillna('Unknown', inplace=True)

# Convert time-related columns like 'ScheduledDeparture', 'ActualDeparture' into datetime format
df_clean['ScheduledDeparture'] = pd.to_datetime(df_clean['ScheduledDeparture'], errors='coerce')
df_clean['ActualDeparture'] = pd.to_datetime(df_clean['ActualDeparture'], errors='coerce')
df_clean['ScheduledArrival'] = pd.to_datetime(df_clean['ScheduledArrival'], errors='coerce')
df_clean['ActualArrival'] = pd.to_datetime(df_clean['ActualArrival'], errors='coerce')

# Feature engineering: Create new time-related features like the delay in departure/arrival
df_clean['DepartureDelay'] = (df_clean['ActualDeparture'] - df_clean['ScheduledDeparture']).dt.total_seconds() / 60.0
df_clean['ArrivalDelay'] = (df_clean['ActualArrival'] - df_clean['ScheduledArrival']).dt.total_seconds() / 60.0

# Drop original time columns (if not needed) and non-predictive columns
df_clean = df_clean.drop(columns=['ScheduledDeparture', 'ActualDeparture', 'ScheduledArrival', 'ActualArrival',
                                  'FlightID', 'FlightNumber', 'TailNumber'])

# Convert categorical variables to numeric via Label Encoding
label_cols = ['Airline', 'Origin', 'Destination', 'DelayReason', 'AircraftType', 'Cancelled', 'Diverted']

label_encoders = {}
for col in label_cols:
    df_clean[col] = df_clean[col].astype(str)
    le = LabelEncoder()
    df_clean[col] = le.fit_transform(df_clean[col])
    label_encoders[col] = le  # Save the label encoder for inverse_transform if needed

# Step 2: Classification Problem
# Define a classification target: Example, classify if a delay is "Long" (>30 mins) or "Short" (<=30 mins)
df_clean['DelayCategory'] = df_clean['DelayMinutes'].apply(lambda x: 1 if x > 30 else 0)  # 1 = Long, 0 = Short
X_clf = df_clean.drop(columns=['DelayMinutes', 'DelayCategory'])  # Features for classification
y_clf = df_clean['DelayCategory']  # Target for classification

# Split the data into training and test sets for classification
X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(X_clf, y_clf, test_size=0.3, random_state=42)

# Train Random Forest Classifier
rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
rf_clf.fit(X_train_clf, y_train_clf)

# Predict and Evaluate Random Forest Classifier
y_pred_rf_clf = rf_clf.predict(X_test_clf)
acc_rf_clf = accuracy_score(y_test_clf, y_pred_rf_clf)
print(f"Random Forest Classifier Accuracy: {acc_rf_clf}")
print(classification_report(y_test_clf, y_pred_rf_clf))

# Train K-Nearest Neighbors Classifier
knn_clf = KNeighborsClassifier(n_neighbors=5)
knn_clf.fit(X_train_clf, y_train_clf)

# Predict and Evaluate KNN Classifier
y_pred_knn_clf = knn_clf.predict(X_test_clf)
acc_knn_clf = accuracy_score(y_test_clf, y_pred_knn_clf)
print(f"KNN Classifier Accuracy: {acc_knn_clf}")
print(classification_report(y_test_clf, y_pred_knn_clf))

# Confusion Matrix for Both Classifiers
conf_matrix_rf = confusion_matrix(y_test_clf, y_pred_rf_clf)
conf_matrix_knn = confusion_matrix(y_test_clf, y_pred_knn_clf)

# Visualize Confusion Matrices
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
sns.heatmap(conf_matrix_rf, annot=True, fmt='d', cmap='Blues')
plt.title("Random Forest Classifier Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.subplot(1, 2, 2)
sns.heatmap(conf_matrix_knn, annot=True, fmt='d', cmap='Greens')
plt.title("KNN Classifier Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()