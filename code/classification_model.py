import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Load your dataset
df = pd.read_csv("ideology_data.csv")
print(df)

# Map textual labels to binary labels: 0 for moderate, 1 for extreme.
label_to_int = {
    "ideologically_moderate": 0,
    "ideologically_extreme": 1
}
df["label_encoded"] = df["label"].map(label_to_int)

# Define your feature columns
features = [
    "cognitive_rigid_score",
    "external_blame_score",
    "social_hostility_score",
    "buzzword_density",
    "emotional_intensity",
    "identity_fusion_score",
    "conspiratorial_thinking_score"
]

X = df[features]
y = df["label_encoded"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate model performance
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
