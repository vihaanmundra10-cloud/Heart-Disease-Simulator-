import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



#Read the CSV file and create a DataFrame

df = pd.read_csv('cleveland_data.csv')

# I don't think this is really necessary, but I want to make sure the columns are named correctly. I don't want to have to deal with the fact that the first row is the header and not the data.
# df = pd.DataFrame(df)

#Formatting the CSV 

df.columns = ["age",
 "sex",
 "cp",
 "trestbps",
 "chol",
 "fbs",
 "restecg",

 #resting ECG result. 0 = normal. 1 = ST-T wave abnormality. 2 = probable or definite left ventricular hypertrophymaximum heart rate achieved.
 "thalach",
#maximum heart rate achieved
 
 "exang",
 #exercise-induced angina, where 1 = yes and 0 = no.
 "oldpeak",
 #ST depression induced by exercise relative to rest.
 "slope",
 #slope of the peak exercise ST segment. 1 = upsloping 2 = flat 3 = downsloping
 "ca",
 #number of major vessels colored by fluoroscopy, usually 0 to 3.
 "thal", 
 #thalassemia result 3 = normal. 6 = fixed defect. 7 = reversible defect ----> an inherited blood disorder that causes the body to produce insufficient or abnormal hemoglobin, the protein in red blood cells that carries oxygen
 "target" 
 #0 = no heart disease, 1 = heart disease, 3, 4 = severity of heart disease
 ]
print("\n\n\n\n\n\n\n")
print("This is the data:")
print("\n\n\n\n\n\n\n")
print(df)
print("\n\n\n\n\n\n\n")


# Replace bad values
df = df.replace('?', np.nan)

# Drop missing rows
df = df.dropna()

# Convert columns to numeric
df = df.apply(pd.to_numeric)

# Remove duplicates
df = df.drop_duplicates()


### AGE ANALYSIS

young = (df['age'] < 40).sum()
middle = ((df['age'] >= 40) & (df['age'] < 60)).sum()
old = (df['age'] >= 60).sum()




total = young + middle + old
print("This is the the people broken down ")

print("Young (<40):", young / total * 100)
print("Middle (40-60):", middle / total * 100)
print("Old(>60):", old / total * 100)

print("\n\n\n\n\n\n\n")

#checking which people had heart disease

def young_people_with_heart_disease(dataframe):
    y = 0
    young_people = dataframe[dataframe['age'] < 40]
    young_hd = young_people[young_people['target'] >= 1]
    y+= len(young_hd)
    print(y/young *100, "% of young people have heart disease")


def middle_people_with_heart_disease(dataframe):
    m = 0
    middle_people = dataframe[(dataframe['age'] >= 40) & (dataframe['age'] < 60)]
    middle_hd = middle_people[middle_people['target'] >=1]
    m += len(middle_hd)
    print(m/middle *100, "% of middle-aged people have heart disease")


def old_people_with_heart_disease(dataframe):
    o = 0
    old_people = dataframe[dataframe['age'] >= 60]
    old_hd = old_people[old_people['target'] >= 1]
    o += len(old_hd)
    print(o/old *100, "% of old people have heart disease")


print('Heart diease analysis with age:')
old_people_with_heart_disease(df)
middle_people_with_heart_disease(df)
young_people_with_heart_disease(df)

#average age of heart disease patients

print("Average age of people with heart disease:", df.loc[df['target']>=1, 'age'].mean())

print("\n\n\n\n\n\n\n")
print("\n\n\n\n\n\n\n")
print("\n\n\n\n\n\n\n")



#Conclusions: As evident, the percentage of people with heart disease increases with age. This is consistent with the fact that heart disease is more common in older people. However, it is also important to note that there are still a significant number of young people with heart disease, which is concerning and highlights the importance of early detection and prevention.




#ANALYZING CHOLESTROL LEVELS 
print('Cholestrol DATA')
print(df[['chol', 'target']])

#people with high cholesterol levels (greater than 240) and how many of them have heart disease (target >= 1)

def cholestrol_anlysis ():
    
    high_chol = df.loc[df['chol'] > 240, 'target']

    high_chol_count = 0
    for row in high_chol:
        if row >= 1:
            high_chol_count += 1

    print(high_chol_count/len(high_chol) * 100, "% of people with high cholesterol have heart disease")

#people with medium cholesterol levels (between 200 and 239) and how many of them have heart disease (target >= 1)
    
    medium_chol = df.loc[(df['chol'] > 200) & (df['chol'] <= 239), 'target']
    medium_chol_count = 0
    for row in medium_chol:
        if row >= 1:
            medium_chol_count += 1

    print(medium_chol_count/len(medium_chol) * 100, "% of people with medium cholesterol have heart disease")
    
#people with low cholesterol levels (between 0 and 200) and how many of them have heart disease (target >= 1)
    
    low_chol = df.loc[(df['chol'] > 0) & (df['chol'] < 200), 'target']
    low_chol_count = 0
    for row in low_chol:
        if row >= 1:
            low_chol_count += 1

    print(low_chol_count/len(low_chol) * 100, "% of people with low cholesterol have heart disease")

    print(df.loc[df["target"] >=1, 'chol'].mean(), "is the average cholesterol level for people with heart disease")

### Conclusion: Cholesterol alone showed weak separation between healthy and diseased groups, suggesting it is not a strong independent predictor in this dataset. However, since this is a relatively small dataset, it is possible that the trend that higher cholesterol levels are associated with increased heart disease risk may become more apparent with a larger sample size. Additionally, cholesterol may still be an important factor when combined with other variables in a multivariate analysis. Also, average cholestral was high in people with heart disease. 
print("\n\n\n\n\n\n\n")
def max_heart_rate_analysis():

#Analyzing for maximum heart rate achieved (thalach)
    print(df.loc[:, ['thalach', 'target']])

    print(df.loc[df['target'] >= 1, 'thalach'])

    print("Mean maximum heart rate for people with heart disease:", df.loc[df['target'] >= 1, 'thalach'].mean())


#factoring for severity of heart disease (target = 1 or 2); low severity 

    print (df.loc[df['target'] >= 3, 'thalach'].mean(), "is the mean maximum heart rate for people with severe heart disease")

#factoring for severity of heart disease (target = 3 or 4)

    print (df.loc[df['target'].isin([1, 2]), 'thalach'].mean(), "is the mean maximum heart rate for people with less severe heart disease")



print("\n\n\n")
print("Cholestrol Analysis")
cholestrol_anlysis()
print("\n\n\n")
print("Max Heart Rate Analysis")
max_heart_rate_analysis()




 # did not make these by myself, just exploring options and learning



# =========================
# GRAPH 1: AGE DISTRIBUTION
# =========================

young = df[df['age'] < 40]
middle = df[(df['age'] >= 40) & (df['age'] < 60)]
old = df[df['age'] >= 60]

age_labels = ["Young (<40)", "Middle (40-60)", "Old (>60)"]
age_counts = [len(young), len(middle), len(old)]

plt.figure()
plt.bar(age_labels, [c / len(df) * 100 for c in age_counts])
plt.title("Age Distribution (%)")
plt.ylabel("Percentage")
plt.show()

# =========================
# GRAPH 2: HEART DISEASE BY AGE
# =========================

plt.figure()
plt.bar(age_labels, [
    (young['target'] >= 1).mean() * 100,
    (middle['target'] >= 1).mean() * 100,
    (old['target'] >= 1).mean() * 100
])
plt.title("Heart Disease % by Age Group")
plt.ylabel("% with Heart Disease")
plt.show()

# =========================
# GRAPH 3: CHOLESTEROL ANALYSIS
# =========================

low = df[df['chol'] < 200]
medium = df[(df['chol'] >= 200) & (df['chol'] <= 239)]
high = df[df['chol'] > 240]

plt.figure()
plt.bar(["Low", "Medium", "High"], [
    (low['target'] >= 1).mean() * 100,
    (medium['target'] >= 1).mean() * 100,
    (high['target'] >= 1).mean() * 100
])
plt.title("Heart Disease % by Cholesterol Level")
plt.ylabel("% with Heart Disease")
plt.show()

print("Average cholesterol (heart disease patients):",
      df[df['target'] >= 1]['chol'].mean())

# =========================
# GRAPH 4: MAX HEART RATE ANALYSIS
# =========================

plt.figure()
plt.bar(
    ["All HD", "Severe", "Less Severe"],
    [
        df[df['target'] >= 1]['thalach'].mean(),
        df[df['target'] >= 3]['thalach'].mean(),
        df[df['target'].isin([1, 2])]['thalach'].mean()
    ]
)
plt.title("Max Heart Rate vs Severity")
plt.ylabel("Average Thalach")
plt.show()

# =========================
# GRAPH 5: AGE VS CHOLESTEROL (SCATTER)
# =========================

plt.figure()
plt.scatter(df['age'], df['chol'], alpha=0.5)
plt.title("Age vs Cholesterol")
plt.xlabel("Age")
plt.ylabel("Cholesterol")
plt.show()

# =========================
# GRAPH 6: STACKED BAR (HD vs NO HD)
# =========================

age_groups = ["Young", "Middle", "Old"]

hd = [
    len(young[young['target'] >= 1]),
    len(middle[middle['target'] >= 1]),
    len(old[old['target'] >= 1])
]

no_hd = [
    len(young[young['target'] == 0]),
    len(middle[middle['target'] == 0]),
    len(old[old['target'] == 0])
]

plt.figure()
plt.bar(age_groups, hd, label="Heart Disease")
plt.bar(age_groups, no_hd, bottom=hd, label="No Heart Disease")
plt.title("Heart Disease Distribution by Age")
plt.legend()
plt.show()

# =========================
# GRAPH 7: BOX PLOT (CHOLESTEROL)
# =========================

plt.figure()
plt.boxplot([
    df[df['target'] == 0]['chol'],
    df[df['target'] >= 1]['chol']
], tick_labels=["No Disease", "Disease"])

plt.title("Cholesterol Distribution")
plt.show()

# =========================
# GRAPH 8: BOX PLOT (THALACH)
# =========================

plt.figure()
plt.boxplot([
    df[df['target'] == 0]['thalach'],
    df[df['target'].isin([1, 2])]['thalach'],
    df[df['target'] >= 3]['thalach']
], tick_labels=["None", "Mild", "Severe"])

plt.title("Max Heart Rate by Severity")
plt.show()

# =========================
# GRAPH 9: CORRELATION HEATMAP
# =========================

plt.figure(figsize=(10, 6))
sns.heatmap(df.corr(numeric_only=True), cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()


# =========================
# SIMULATION: HEART DISEASE RISK MODEL
# =========================

def heart_disease_risk(age, chol, thalach):

    score = 0

    # age contribution
    if age > 60:
        score += 2
    elif age > 40:
        score += 1
    elif age < 40:
        score += 0

    # cholesterol contribution
    if chol > 240:
        score += 2
    elif chol >=200:
        score += 1

    # heart rate contribution (lower is higher risk)
    if thalach < 130:
        score += 2
    elif thalach < 160:
        score += 1

    risk_percent = (score / 6) * 100

    print(risk_percent)


simulation_age = int(input('What is your age?'))
simulation_cholestrol = int(input("What is your cholestrol?"))
simulation_heart_rate = int(input("What is your heart rate?"))

heart_disease_risk(simulation_age, simulation_cholestrol, simulation_heart_rate)
