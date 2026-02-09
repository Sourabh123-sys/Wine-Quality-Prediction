from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load trained model
model = pickle.load(open("model.pkl", "rb"))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form values
        features = [
            float(request.form['fixed_acidity']),
            float(request.form['volatile_acidity']),
            float(request.form['citric_acid']),
            float(request.form['residual_sugar']),
            float(request.form['chlorides']),
            float(request.form['free_sulfur_dioxide']),
            float(request.form['total_sulfur_dioxide']),
            float(request.form['density']),
            float(request.form['ph']),
            float(request.form['sulphates']),
            float(request.form['alcohol'])
        ]

        # Create DataFrame with column names (IMPORTANT)
        columns = [
            'fixed acidity',
            'volatile acidity',
            'citric acid',
            'residual sugar',
            'chlorides',
            'free sulfur dioxide',
            'total sulfur dioxide',
            'density',
            'pH',
            'sulphates',
            'alcohol'
        ]

        input_df = pd.DataFrame([features], columns=columns)

        prediction = model.predict(input_df)[0]

        if prediction >= 6:
            result = "Good Quality Wine"
        else:
            result = "Bad Quality Wine"

        return render_template("index.html", result=result)

    except Exception as e:
        print("ERROR:", e)
        return render_template("index.html", result="Prediction Failed")

if __name__ == "__main__":
    app.run(debug=True)
