import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(
    page_title="Heart Disease Simulator",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(180deg, #f7f9fc 0%, #eef3f9 100%);
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .app-title {
        font-size: 3rem;
        font-weight: 800;
        color: #b22234;
        text-align: center;
        margin-bottom: 0.15rem;
    }

    .app-subtitle {
        font-size: 1.05rem;
        color: #5a5a5a;
        text-align: center;
        margin-bottom: 1.3rem;
    }

    .card {
        background: white;
        padding: 1.1rem 1.2rem;
        border-radius: 18px;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
        border: 1px solid rgba(15, 23, 42, 0.06);
        margin-bottom: 1rem;
    }

    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.35rem;
    }

    .small-note {
        color: #6b7280;
        font-size: 0.92rem;
    }
    </style>

    <div class="app-title">Heart Disease Simulator</div>
    <div class="app-subtitle">Exploring age, cholesterol, and maximum heart rate with Streamlit</div>
    """,
    unsafe_allow_html=True
)

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
st.write("\n\n\n\n\n\n\n")
st.write("This is the data:")
st.write("\n\n\n\n\n\n\n")
st.write(df)
st.write("\n\n\n\n\n\n\n")


# Replace bad values
df = df.replace('?', np.nan)

# Drop missing rows
df = df.dropna()

# Convert columns to numeric
df = df.apply(pd.to_numeric)

# Remove duplicates
df = df.drop_duplicates()

st.sidebar.markdown("## Patient Inputs")
st.sidebar.write("This app explores three factors:")
st.sidebar.write("- Age")
st.sidebar.write("- Cholesterol")
st.sidebar.write("- Maximum heart rate")

### AGE ANALYSIS

# young = (df['age'] < 40).sum()
# middle = ((df['age'] >= 40) & (df['age'] < 60)).sum()
# old = (df['age'] >= 60).sum()




# total = young + middle + old
# st.write("This is the the people broken down ")

# st.write("Young (<40):", young / total * 100)
# st.write("Middle (40-60):", middle / total * 100)
# st.write("Old(>60):", old / total * 100)

# st.write("\n\n\n\n\n\n\n")

# #checking which people had heart disease

# def young_people_with_heart_disease(dataframe):
#     y = 0
#     young_people = dataframe[dataframe['age'] < 40]
#     young_hd = young_people[young_people['target'] >= 1]
#     y+= len(young_hd)
#     st.write(y/young *100, "% of young people have heart disease")


# def middle_people_with_heart_disease(dataframe):
#     m = 0
#     middle_people = dataframe[(dataframe['age'] >= 40) & (dataframe['age'] < 60)]
#     middle_hd = middle_people[middle_people['target'] >=1]
#     m += len(middle_hd)
#     st.write(m/middle *100, "% of middle-aged people have heart disease")


# def old_people_with_heart_disease(dataframe):
#     o = 0
#     old_people = dataframe[dataframe['age'] >= 60]
#     old_hd = old_people[old_people['target'] >= 1]
#     o += len(old_hd)
#     st.write(o/old *100, "% of old people have heart disease")


# st.write('Heart diease analysis with age:')
# old_people_with_heart_disease(df)
# middle_people_with_heart_disease(df)
# young_people_with_heart_disease(df)

# #average age of heart disease patients

# st.write("Average age of people with heart disease:", df.loc[df['target']>=1, 'age'].mean())

# st.write("\n\n\n\n\n\n\n")
# st.write("\n\n\n\n\n\n\n")
# st.write("\n\n\n\n\n\n\n")



# #Conclusions: As evident, the percentage of people with heart disease increases with age. This is consistent with the fact that heart disease is more common in older people. However, it is also important to note that there are still a significant number of young people with heart disease, which is concerning and highlights the importance of early detection and prevention.

### AGE ANALYSIS
age = df.loc[df["target"] >= 1, "age"]

age_with_heart_disease = len(age)

st.write("Mean age with Heart Disease: ", age.mean())

young = st.write("Percentage of people with heart disease under 40: ",
      (age < 40).sum() / age_with_heart_disease *100) 
y = age[age < 40]

middle = st.write("Percentage of people with heart disease between 40-60: ",
      ((age >= 40) & (age < 60)).sum() / age_with_heart_disease *100) 
m = age[(age >= 40) & (age < 60)]

old = st.write("Percentage of people with heart disease between >60: ",
      (age>60).sum() / age_with_heart_disease * 100) 
o = age[age >= 60]


#ANALYZING CHOLESTROL LEVELS 
st.write('Cholestrol DATA')
st.write(df[['chol', 'target']])

#people with high cholesterol levels (greater than 240) and how many of them have heart disease (target >= 1)

def cholestrol_anlysis ():
    
    high_chol = df.loc[df['chol'] > 240, 'target']

    high_chol_count = 0
    for row in high_chol:
        if row >= 1:
            high_chol_count += 1

    st.write(high_chol_count/len(high_chol) * 100, "% of people with high cholesterol have heart disease")

#people with medium cholesterol levels (between 200 and 239) and how many of them have heart disease (target >= 1)
    
    medium_chol = df.loc[(df['chol'] > 200) & (df['chol'] <= 239), 'target']
    medium_chol_count = 0
    for row in medium_chol:
        if row >= 1:
            medium_chol_count += 1

    st.write(medium_chol_count/len(medium_chol) * 100, "% of people with medium cholesterol have heart disease")
    
#people with low cholesterol levels (between 0 and 200) and how many of them have heart disease (target >= 1)
    
    low_chol = df.loc[(df['chol'] > 0) & (df['chol'] < 200), 'target']
    low_chol_count = 0
    for row in low_chol:
        if row >= 1:
            low_chol_count += 1

    st.write(low_chol_count/len(low_chol) * 100, "% of people with low cholesterol have heart disease")

    st.write(df.loc[df["target"] >=1, 'chol'].mean(), "is the average cholesterol level for people with heart disease")

### Conclusion: Cholesterol alone showed weak separation between healthy and diseased groups, suggesting it is not a strong independent predictor in this dataset. However, since this is a relatively small dataset, it is possible that the trend that higher cholesterol levels are associated with increased heart disease risk may become more apparent with a larger sample size. Additionally, cholesterol may still be an important factor when combined with other variables in a multivariate analysis. Also, average cholestral was high in people with heart disease. 
st.write("\n\n\n\n\n\n\n")
def max_heart_rate_analysis():

#Analyzing for maximum heart rate achieved (thalach)
    st.write(df.loc[:, ['thalach', 'target']])

    st.write(df.loc[df['target'] >= 1, 'thalach'])

    st.write("Mean maximum heart rate for people with heart disease:", df.loc[df['target'] >= 1, 'thalach'].mean())


#factoring for severity of heart disease (target = 1 or 2); low severity 

    st.write (df.loc[df['target'] >= 3, 'thalach'].mean(), "is the mean maximum heart rate for people with severe heart disease")

#factoring for severity of heart disease (target = 3 or 4)

    st.write (df.loc[df['target'].isin([1, 2]), 'thalach'].mean(), "is the mean maximum heart rate for people with less severe heart disease")



st.write("\n\n\n")
st.write("Cholestrol Analysis")
cholestrol_anlysis()
st.write("\n\n\n")
st.write("Max Heart Rate Analysis")
max_heart_rate_analysis()




 

tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Age", "Cholesterol", "Heart Rate"])

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
st.pyplot()

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
st.pyplot()

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
st.pyplot()

st.write("Average cholesterol (heart disease patients):",
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
st.pyplot()

# =========================
# GRAPH 5: AGE VS CHOLESTEROL (SCATTER)
# =========================

plt.figure()
plt.scatter(df['age'], df['chol'], alpha=0.5)
plt.title("Age vs Cholesterol")
plt.xlabel("Age")
plt.ylabel("Cholesterol")
st.pyplot()

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
st.pyplot()

# =========================
# GRAPH 7: BOX PLOT (CHOLESTEROL)
# =========================

plt.figure()
plt.boxplot([
    df[df['target'] == 0]['chol'],
    df[df['target'] >= 1]['chol']
], tick_labels=["No Disease", "Disease"])

plt.title("Cholesterol Distribution")
st.pyplot()

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
st.pyplot()

# =========================
# GRAPH 9: CORRELATION HEATMAP
# =========================

plt.figure(figsize=(10, 6))
sns.heatmap(df.corr(numeric_only=True), cmap="coolwarm")
plt.title("Correlation Heatmap")
st.pyplot()


# =========================
# SIMULATION: HEART DISEASE RISK MODEL
# =========================

def heart_disease_risk(age, chol, thalach):

    score = 0

    # age contribution (375)
    if age >= 60:
        score +=  200
    elif (age >= 40) and (age < 60) :
        score += 125
    elif age < 40:
        score += 50

    # cholesterol contribution (80)
    if chol >= 240:
        score += 50
    elif (chol >=200) and (chol<240):
        score += 25
    elif chol <200:
        score += 5

    # heart rate contribution (lower is higher risk) (1000pt)
    if thalach >= 170:
        score += 100
    elif (thalach >= 150) and (thalach <170) :
        score += 200
    elif (thalach >= 130) and (thalach < 150):
        score +=300
    elif thalach <130:
        score+=400
    

    risk_percent = (score / 1455) * 100

    st.write(risk_percent)


simulation_age = st.number_input('What is your age?', min_value=0, max_value=120, value=50)
simulation_cholestrol = st.number_input("What is your cholestrol?", min_value=0, max_value=1000, value=200)
simulation_heart_rate = st.number_input("What is your heart rate?", min_value=0, max_value=250, value=150)

heart_disease_risk(simulation_age, simulation_cholestrol, simulation_heart_rate)
