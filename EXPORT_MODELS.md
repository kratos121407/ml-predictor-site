# How to export your trained models from Colab

Run the matching block at the END of each notebook (after your models are
trained), then download the generated file and send it back to me.

---

## 1. Wine Quality — add this cell

Uses whichever combo (scaled vs not) you found was best. Adjust the
model/scaler variable names below if yours differ.

```python
import joblib

wine_bundle = {
    "model": best_model_scaled,       # or best_model if scaling didn't help
    "scaler": scaler,                 # set to None if you did NOT use scaling
    "feature_order": list(X.columns), # exact column order the model expects
}

joblib.dump(wine_bundle, "wine_quality.pkl")

from google.colab import files
files.download("wine_quality.pkl")
```

---

## 2. AI Hiring Decision — add this cell

This dataset's features depend on your training data's unique Skills and
Job Roles, so we bundle everything needed to rebuild the same encoding at
prediction time.

```python
import joblib

hiring_bundle = {
    "model": best_model,                       # your chosen final model
    "skill_columns": list(skills_encoded.columns),  # exact skill dummy columns
    "job_roles": ["AI Researcher", "Data Scientist", "Software Engineer", "Cybersecurity Analyst"],
    "education_levels": ["B.Sc", "B.Tech", "M.Tech", "MBA", "PhD"],
    "certifications": list(df_raw["Certifications"].unique()) if "df_raw" in dir() else None,
    "feature_order": list(X.columns),          # exact column order the model expects
}

joblib.dump(hiring_bundle, "hiring_model.pkl")

from google.colab import files
files.download("hiring_model.pkl")
```

> Note: if `df_raw` isn't defined in your notebook (i.e. you overwrote `df`
> before dropping Certifications), just run
> `print(df["Certifications"].unique())` from before that step and paste the
> list in manually.

---

## 3. Fake Job Postings — add this cell

This one needs the fitted TF-IDF vectorizer and the exact one-hot column
list too, since predictions on new text require the same vocabulary.

```python
import joblib

job_postings_bundle = {
    "model": model_RF,                     # or whichever model performed best
    "tfidf": tfidf,                        # fitted TfidfVectorizer
    "encoded_columns": list(encoded_df.columns),  # exact one-hot columns from training
    "numeric_columns": list(numeric_df.columns),  # exact numeric columns from training
    "categorical_cols": categorical_cols,  # ["location","department",...]
}

joblib.dump(job_postings_bundle, "job_postings_model.pkl")

from google.colab import files
files.download("job_postings_model.pkl")
```

---

## What to send back

Upload the resulting `.pkl` file(s) here (one at a time is fine). Once I
have each one, I'll:
1. Drop it into the site's `models/` folder
2. Read the categories/vocabulary out of it
3. Build the matching input form with correct dropdown options

Start with **wine_quality.pkl** — it's the fastest to get working end-to-end.
