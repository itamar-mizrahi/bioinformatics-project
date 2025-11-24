import pandas as pd
import numpy as np

# 1. יצירת דאטה מדומה (Simulation)
# נדמה 20 מטופלים עם נתונים אקראיים בטווחים הגיוניים
np.random.seed(42) # כדי שהתוצאות יהיו עקביות
n_patients = 20

data = {
    'Patient_ID': range(1, n_patients + 1),
    'Age': np.random.randint(60, 90, n_patients),
    'Gender': np.random.choice(['M', 'F'], n_patients),
    # כוח אחיזה בק"ג (טווח: 10-50)
    'Grip_Strength_KG': np.random.uniform(10, 50, n_patients).round(1),
    # אינדקס מסת שריר (טווח: 5.0-10.0)
    'SMI': np.random.uniform(5.0, 10.0, n_patients).round(2),
    # מהירות הליכה במטר לשנייה (טווח: 0.4-1.5)
    'Gait_Speed_ms': np.random.uniform(0.4, 1.5, n_patients).round(2)
}

df = pd.DataFrame(data)

# 2. פונקציית הליבה לזיהוי סרקופניה (הלוגיקה הביולוגית)
# הערה: הספים נלקחו מהנחיות כלליות (EWGSOP2) לצורך הדגמה
def analyze_sarcopenia_risk(row):
    risk_score = 0
    reasons = []

    # ספים לגברים (M) ולנשים (F)
    thresholds = {
        'M': {'grip': 27, 'smi': 7.0},
        'F': {'grip': 16, 'smi': 5.5}
    }
    
    t = thresholds[row['Gender']]

    # קריטריון 1: כוח שריר ירוד (Grip Strength)
    if row['Grip_Strength_KG'] < t['grip']:
        risk_score += 1
        reasons.append('Low Grip Strength')

    # קריטריון 2: מסת שריר נמוכה (SMI)
    if row['SMI'] < t['smi']:
        risk_score += 1
        reasons.append('Low Muscle Mass')

    # קריטריון 3: ביצועים פיזיים ירודים (Gait Speed) - זהה לשני המינים
    if row['Gait_Speed_ms'] <= 0.8:
        risk_score += 1
        reasons.append('Slow Gait Speed')

    # החלטה סופית
    if risk_score >= 2:
        return pd.Series(['High Risk', ', '.join(reasons)])
    elif risk_score == 1:
        return pd.Series(['Moderate Risk', reasons[0]])
    else:
        return pd.Series(['Low Risk', '-'])

# 3. הרצת האנליזה על הדאטה
df[['Diagnosis', 'Details']] = df.apply(analyze_sarcopenia_risk, axis=1)

# הצגת התוצאות - רק אלו שבסיכון
print("--- Sarcopenia Analysis Results ---")
high_risk_patients = df[df['Diagnosis'] == 'High Risk']
print(high_risk_patients[['Patient_ID', 'Gender', 'Age', 'Diagnosis', 'Details']])