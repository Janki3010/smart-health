import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("/home/rl22/smart-health/app/model/medical_dataset1.csv - Sheet1 (1).csv")

# 1. Split blood pressure into systolic and diastolic
df[['systolic_bp', 'diastolic_bp']] = df['blood_pressure'].str.split('/', expand=True).astype(int)
df.drop('blood_pressure', axis=1, inplace=True)

# 2. Convert smoking to binary
df['smoking_habit'] = df['smoking_habit'].map({'yes': 1, 'no': 0})

# 3. Combine symptoms into one column (text OR one-hot vector later)
df['combined_symptoms'] = df[['symptom_1', 'symptom_2', 'symptom_3']].fillna('').agg(' '.join, axis=1)
df.drop(['symptom_1', 'symptom_2', 'symptom_3'], axis=1, inplace=True)

# Optional: encode symptoms into features (e.g., via Tfidf, CountVectorizer)
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
symptom_features = vectorizer.fit_transform(df['combined_symptoms'])

# Save vectorizer to reuse in prediction
joblib.dump(vectorizer, "/home/rl22/smart-health/app/model/symptom_vectorizer.pkl")

# 4. Combine numeric features
numeric_features = df[['age', 'weight', 'glucose_level', 'insulin_level', 'systolic_bp', 'diastolic_bp', 'smoking_habit']].values

# 5. Final feature matrix
import scipy
X = scipy.sparse.hstack([numeric_features, symptom_features])  # combine numeric + symptom

# 6. Encode labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df['disease'])

# Save encoder
joblib.dump(label_encoder, "/home/rl22/smart-health/app/model/label_encoder.pkl")

# 7. Train model
model = RandomForestClassifier()
model.fit(X, y)
joblib.dump(model, "/home/rl22/smart-health/app/model/disease_model.pkl")

print("✅ Model trained and saved.")



# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# import joblib
#
# # Load real dataset
# df = pd.read_csv("Symptom-severity.csv")  # Use actual file name
# X = df.drop("Disease", axis=1)
# y = df["Disease"]
#
# # Train model
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# model = RandomForestClassifier()
# model.fit(X_train, y_train)
#
# # Save model
# joblib.dump(model, "/home/rl22/smart-health/app/model/disease_model2.pkl")
# print("Model trained using real dataset")

#
# import pandas as pd
# from sklearn.tree import DecisionTreeClassifier
# import joblib
#
# # Sample symptoms-disease dataset
# data = [
#     {"fever": 1, "headache": 1, "sore_throat": 1, "cough": 0, "fatigue": 0, "disease": "Flu"},
#     {"fever": 0, "headache": 0, "sore_throat": 0, "cough": 1, "fatigue": 0, "disease": "Cold"},
#     {"fever": 1, "headache": 1, "sore_throat": 0, "cough": 1, "fatigue": 1, "disease": "COVID-19"},
#     {"fever": 0, "headache": 0, "sore_throat": 0, "cough": 0, "fatigue": 1, "disease": "Fatigue"},
# ]
#
# df = pd.DataFrame(data)
# X = df.drop("disease", axis=1)
# y = df["disease"]
#
# model = DecisionTreeClassifier()
# model.fit(X, y)

joblib.dump(model, "/home/rl22/smart-health/app/model/disease_model.pkl")
print("Model trained and saved")
