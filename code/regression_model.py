import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load your dataset
df = pd.read_csv("ideology_data.csv")

# Map textual labels to continuous ideology scores.
# You can adjust these mappings as needed.
label_to_score = {
    "ideologically_extreme": 70,
    "ideologically_moderate": 35,
    # Add additional mappings if you include more labels.
}
df["ideology_score"] = df["label"].map(label_to_score)

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
y = df["ideology_score"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate model performance
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Mean Squared Error (MSE):", mse)
print("R² Score:", r2)

# OPTIONAL: View feature coefficients for interpretability
coef_df = pd.DataFrame({
    "Feature": features,
    "Coefficient": model.coef_
}).sort_values(by="Coefficient", ascending=False)
print("\nFeature Importance (Linear Coefficients):")
print(coef_df)
