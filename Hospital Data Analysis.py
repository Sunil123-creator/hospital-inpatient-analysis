#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt


# In[2]:


path = r"C:\Users\sunil\OneDrive\Desktop\MSIS415\Hospital_Inpatient_Discharges.csv" #loading the data


# In[3]:


df = pd.read_csv(path, low_memory=False) #reading the entire file


# In[4]:


df.head(10) #looking the first 10 rows of the table


# In[5]:


df.tail(10) #last 10 rows


# In[6]:


df.info() #information about the datatypes


# In[7]:


df["Length of Stay"] = df["Length of Stay"].astype(str).str.strip()
df["Length of Stay"] = df["Length of Stay"].str.replace("120 +", "120", regex=False)
df["Length of Stay"] = pd.to_numeric(df["Length of Stay"], errors="coerce") #change the legnth of stay from object to string and from string to numeric


# In[8]:


df["Length of Stay"].head(10) #Length of Stay


# In[9]:


df["Total Charges"].describe()


# In[10]:


df["Total Costs"].describe()


# **Insights:**
# 
# Total inpatient hospital stays: 2.13 million. Mean for the total charge is 72, 835 dollars and mean for the total cost is 21, 895 dollars. The standard deviation for total charge stands at 148, 598 dollars which means some patient cost very little amount whereas some patients costs huge amount i.e. more than a million. Similar situation exists in total costs. Median for the total charges is 38, 122 dollares which means 50 percent of the data falls under this value. Similarly, median for the total costs is 11, 530 dollars which implies 50 percent of the data falls under this value. Overall, inpatient hospital charges are 2-3 times higher than the associated costs, reflecting standard hospital pricing and reimbursement structures rather than actual resources consumption. The large gap between mean and median confirms a right-skewed distribution.
# 

# In[11]:


df.isna().any().any()


# In[12]:


df.isna().sum()


# *** Here, some columns have several null values which does not necessiliry means they are missing values but it also means maybe the fields were not relevant or not necessary

# In[13]:


(df.isna().mean() * 100).sort_values(ascending=False)


# In[14]:


(df["Gender"].value_counts(normalize=True) * 100).round(2).astype(str) + "%"


# In[15]:


(df["Ethnicity"].value_counts(normalize=True) * 100).round(2).astype(str) + "%"


# **Insights:**
# 
# Females outnumber males, representing 54.5% percent of patients versus 45 percent male patients. Interms of ethnicity, the majority of patients are not Spanish/Hispanic, followed by Spanish/Hispanic patients. Approximately 9.57% of patients have unknown ethnicity, while 0.22% identify as multi-ethnic. 
# 
# Resource planning should consider slightly higher female utilization. Services frequently used by female patients should be appropriately staffed. Communication resources should prioritize English, while ensuring Spanish-language support due to 15% representation (over 300,000 patients).

# In[16]:


df["CCSR Procedure Code"].notna()


# In[17]:


df["has_procedure"] = df["CCSR Procedure Code"].notna()


# In[18]:


df[["CCSR Procedure Code", "has_procedure"]].head(10)


# In[19]:


(df["has_procedure"].value_counts(normalize=True) * 100).round(2).astype(str) + "%"


# In[20]:


df[["has_procedure", "Total Costs", "Length of Stay"]].head(10)


# In[21]:


df.groupby("has_procedure")[["Total Costs", "Total Charges"]].median()


# In[22]:


df.groupby("has_procedure")["Length of Stay"].agg(["mean", "median"])


# **Insights:**
# 
# 73% of inpatient stays involved at least one recorded procedure, while 27% did not meaning majority of inpatient admissions require precedural intervention beyond just observation. Patients with procedures have higher median costs and charges. The median length of stay for both group is 3 days which indicates that typical hospitalization duration is similar regardless of procedure status. However, mean LOS is higher amnog patients undergoing prcedures. Planning for OR scheduling and post-procedure beds is important.  

# As we have multiple columns, lets categorise each column into different domains. 
# 
# Financial /Billing Information
# - Total Charges, Total Costs, Payment Typology 1, Payment Typology 2, Payment Tyypology 3
# 
# Facility /Hospital Information
# - Facility Name, Permanent Facility Id, Operating Certificate Number, Hospital Service Area, Hospital County
# 
# Patient Demographics
# - Age Group, Gender, Race, Ethnicity, Zip Code
# 
# Clinical Condition /Diagnosis
# - CCSR Diagnosis Code, CCSR Diagnosis Description, APR DRG Code, APR DRG Description, APR MDC Code, APR MDC Description
# 
# Clinical Procedures /Treatment
# - CCSR Procedure Code, CCSR Procedure Description, APR Medical Surgical Description, APR Medical Surgical Code, has_procedure
# 
# Severity and Risk Indicators
# - APR Severity of Illness Code, APR Severity of Illness Description, APR Risk of Morality
# 
# Utilization and Encounter Details
# - Length of Stay, Type of Admission, Emergency Department Indicator, Patient Disposition, Discharge Year
# 
# Neonatal /Special Population
# - Birth Weight

# ***PATIENTS DEMOGRAPHICS + UTILIZATION AND ENCOUNTER DETAILS*** 

# In[23]:


df["Length of Stay"].isna().sum()


# In[24]:


(df["Length of Stay"].describe()).round(2)


# In[25]:


los_counts = df["Length of Stay"].value_counts(normalize=True).sort_index().head(15) * 100

plt.figure(figsize=(10,5))
plt.bar(los_counts.index, los_counts.values)
plt.xlabel("Length of Stay (Days)")
plt.ylabel("Percent of Patients (%)")
plt.title("Distribution of Length Stay")
plt.grid(True)
plt.show()


# **Insights:**
# 
# The median length of stay is 3 days which means that half of all inpatient hospitalizations are short. Approximately 75% of data falls under 6 days indicating that 75% of patients are discharged within 6 days. However, the mean LOS is 5.75 days which is higher than the median, reflecting a right-skewed distribution. The maximum LOS of 120 days reflects rare but extremely prolonged hospitalizations, likely associated with complex medical conditions. About 27% of patients have LOS 2 days which is the highest, followed by 1 day and 3 days. 

# In[26]:


los_stats = df.groupby("Age Group")["Length of Stay"].agg(["mean","median"])
los_stats.plot(kind="bar", figsize=(8,5))
plt.title("Mean vs Median Length of Stay by Age Group")
plt.ylabel("Days")
plt.xticks(rotation=45)
plt.show()


# In[27]:


summary = df.groupby("Age Group").agg(Patient_Count=("Age Group", "count"), Mean_LOS=("Length of Stay", "mean"), Median_LOS=("Length of Stay", "median"))
summary["Percent_of_Total"] = (summary["Patient_Count"] / summary["Patient_Count"].sum() * 100).round(2)
print(summary)


# In[28]:


plt.figure(figsize=(12,7))

ax = summary["Percent_of_Total"].plot(kind="bar")
for i, v in enumerate(summary["Percent_of_Total"]):
    ax.text(i, v, f"{v:.1f}%", ha="center", va="bottom")

a2x = ax.twinx()
summary["Mean_LOS"].plot(ax=a2x, marker='o')
summary["Median_LOS"].plot(ax=a2x, marker='s')
ax.set_xlabel("Age Group")
ax.set_ylabel("Patients (% of total)")
a2x.set_ylabel("Length of Stay (Days)")
plt.title("Age Group vs Patient % and Length of Stay", pad=20)
ax.legend(["Patient Count"], loc="upper left")
a2x.legend(["Mean LOS", "Median LOS"], loc="upper center")
plt.show()


# **Insights:**
# 
# Young adults of age 18 to 29 have the lowest hospitalization share amnong all age group. In contrast, 55% of patients are of age 50 above. Their median length of stay is approximately 4 and average length of stay exceeds 6 days. Majority of patients are older people and they stay longer. It should be also noted that 50% of patient occupy hospital facilities and benefits from 4 to 6 days. Therefore while planning anything related to bed allocation, infrasturcture planning, staff scheduling, policy planning, service, etc. It important to keep older people in mind. 50% - 60% of any planning should focus on older people.  

# In[29]:


admission_percent = pd.crosstab(
    df["Age Group"],
    df["Type of Admission"],
    normalize="index"
) * 100

admission_percent = admission_percent.round(2)
admission_percent


# In[30]:


admission_percent.plot(kind="bar", stacked=True, figsize=(12,7))
plt.title("Type of Admission by Age Group (%)")
plt.ylabel("Percentage")
plt.xticks(rotation=45)
plt.show()


# **Insights:**
# 
# About 75% of patient of age over 50 are admitted through emergency service, emergency admissions increases with age. Around 60% of patient of age from 18 to 49 are admiited through emergency, followed by elective and urgent admissions. The 18-49 cohort exhibits the highest proportion of urgent admissions among adult age groups. Under 17, about 65% of patient are newborn.
# 
# From the previous graph, patients above age 50 represents 57% of total patients, with nearly three-quarters of these cases entering through emergency services. Therefore, more focus should be given to emergency department while staffing, bed allocation, and operatinal planning. 

# ***PATIENT DEMOGRAPICS + FINANACIAL/BILLING INFORMATION***

# In[31]:


plt.figure(figsize=(12,20))
df.boxplot(column="Total Charges", by="Age Group")
plt.title("Total Charges by Age Group")
plt.suptitle("")
plt.xlabel("Age Group")
plt.ylabel("Charges ($)")
plt.show()

plt.figure(figsize=(12,20))
df.boxplot(column="Total Charges", by="Age Group")
plt.ylim(0, 200000)
plt.title("Total Charges by Age Group")
plt.suptitle("")
plt.xlabel("Age Group")
plt.ylabel("Charges ($)")
plt.show()


# **Insights:**
# 
# We have outlier in all the age groups, confirming the highly right-skewed nature of hospital charge distributions. The median total charge increase with age which means more severe cases for older generation and greater financial burden among older patients. The 75th percentile rises substantially from 50,000 dollars in the 18-19 group to nearly 100,000 dollars among patients aged 70 and above, meaning increased resource utilization in elderly populations. 
# 
# To help elderly people, maybe specific program should be introduced to them to make them stay more healthy and early interventions programs may help reduce prolonged stays and high-cost complications among elderly patients.

# In[32]:


median_admission = df.groupby("Type of Admission")[["Total Charges", "Total Costs"]].median()
median_admission


# In[33]:


mean_admission = df.groupby("Type of Admission")[["Total Charges", "Total Costs"]].mean()
mean_admission


# In[34]:


trauma_percent = (pd.crosstab(df["Age Group"], df["Type of Admission"], normalize="index") * 100)
trauma_percent["Trauma"].round(2).astype(str) + "%"


# **Insights:**
# 
# Both mean and median suggests that trauma has the highest total charge and total cost. Elective admissions are more expensive than emergency which means planned hospital process contribute to hospital revenue more than emergency admissions. In all the type of admissions, mean is higher than median, which suggests that there are outliers or high-cost cases. 
# 
# Trauma admissions have high charge and high cost, therefore, hospital should ensure adequate infrastructure and facilities are present in the hospital to manage trauma cases efficiently. Also, elective admissions is good contributor to hospital revenue, so any strategies that make the elective admissions efficient and effective should be implemented.

# In[35]:


plt.figure(figsize=(12,7))
plt.scatter(df["Length of Stay"], df["Total Charges"], alpha=0.3)
plt.yscale("log")
plt.title("Length of Stay vs Total Charges")
plt.xlabel("Length of Stay (Days)")
plt.ylabel("Total Charges ($)")
plt.show()

plt.figure(figsize=(12,7))
plt.scatter(df["Length of Stay"], df["Total Costs"], alpha=0.3)
plt.yscale("log")
plt.title("Length of Stay vs Total Costs")
plt.xlabel("Length of Stay (Days)")
plt.ylabel("Total Costs ($)")
plt.show()


# In[36]:


df[["Length of Stay", "Total Charges"]].corr()


# In[37]:


df[["Length of Stay", "Total Costs"]].corr()


# **Insights:**
# 
# As the hospitalization day increases, so does the total charge and total cost that is confirmed by log-scale visualization. Also, the correlation data shows a strong positive relationship between length of saty and both total charges and total costs. 
# 
# Therefore, to decrease the financial burden on patients, hospital should plan on reducing avoiable length of stay withot compromising patient's satefy. They can have early discharge planning, post follow-up, etc.

# In[38]:


(df["Payment Typology 1"].value_counts(normalize=True) * 100).round(2).astype(str) + "%"


# In[39]:


revenue_percent = (
    df.groupby("Payment Typology 1")["Total Charges"]
    .sum()
    / df["Total Charges"].sum()
) * 100

plt.figure(figsize=(12,7))
revenue_percent.sort_values(ascending=False).plot(kind="bar")
plt.title("Revenue Contribution by Primary Payer")
plt.ylabel("Revenue Share (%)")
plt.xticks(rotation=20)
plt.show()


# **Insight**
# 
# Around 70% of the expenses are covered by Medicare and Medicaid which means dependence on government reimbursement structures. This matches with the data of about 57% of pataients are above age 50. Since there is fixed reimbursement from public programs, which means less profit margin, it's better to make the management and operation more efficient without compromising the patient's safety.

# ***PATIENTS DEMOGRPAHICS + CLINICAL CONDITION/DIAGNOSIS***

# In[40]:


# Top 5 diagnosis within each age group
top_n = 5
for age, g in df.groupby("Age Group"):
    top_diag = (g["CCSR Diagnosis Description"].value_counts(normalize=True).head(top_n) * 100).sort_values()
    
    plt.figure(figsize=(8,3))
    plt.barh(top_diag.index, top_diag.values, color="darkgreen")
    plt.title(f"Top {top_n} Diagnosis (%) - Age Group: {age}")
    plt.xlabel("Percent of Patients")
    plt.ylabel("Diagnosis")
    plt.show()


# In[41]:


# Top 5 diagnosis within each age group
top_n = 5
g = df[(df["Age Group"] == "0 to 17") & (df["CCSR Diagnosis Description"] != "Liveborn")]
top_diag = (g["CCSR Diagnosis Description"].value_counts(normalize=True).head(top_n) * 100).sort_values()
    
plt.figure(figsize=(8,3))
plt.barh(top_diag.index, top_diag.values, color="darkgreen")
plt.title(f"Top 5 Diagnosis (%) - Age Group: 0 to 17")
plt.xlabel("Percent of Patients")
plt.ylabel("Diagnosis")
plt.show()


# **Insights:**
# 
# The distribution of top CCSR diagnosis varies significantly by age group. Patients of age group 0 to 17 are mostly driven by live births, while young adults are predominantly admitted for pregnancy-related complications and behavioral health conditions. In the patient of age group 30 to 49, child birth complications still present followed by Septicemia and alcohol related disorders. Septicemia becomes dominant in 50 to 69 years age groups, followed by COVID19 and alcohol-related disorders. Septicemia is still dominant in the patients of age 70 or more, ollowed by heart failure and COVID-19. 

# In[42]:


#Top 5 APR MDC Category in each Age Group
top_n = 5
for age, g in df.groupby("Age Group"):
    top_mdc = (g["APR MDC Description"].value_counts(normalize=True).head(top_n) * 100).sort_values()
    
    plt.figure(figsize=(8,3))
    plt.barh(top_mdc.index, top_mdc.values, color="purple")
    plt.title(f"Top {top_n} MDC Categories (%) - Age Group: {age}")
    plt.xlabel("Percent of Patients")
    plt.ylabel("MDC Category")
    plt.show()


# **Insights:**
# 
# MDC category indicates a strong age-depended shift in inpatient utlization patterns. Early life/pediatric admissions are driven by neonatal/birth related conditions, while young adults are primarily admitted for pregnancy-related care, followed by mental health. As the age increases, diseases and disorders related to circulatory and respiratory system becomes more dominant.

# In[43]:


#Top 5 APR DRG Category in each Age Group
top_n = 5
for age, g in df.groupby("Age Group"):
    top_apr = (g["APR DRG Description"].value_counts(normalize=True).head(top_n) * 100).sort_values()
    
    plt.figure(figsize=(8,3))
    plt.barh(top_apr.index, top_apr.values, color="navy")
    plt.title(f"Top {top_n} APR Categories (%) - Age Group: {age}")
    plt.xlabel("Percent of Patients")
    plt.ylabel("APR Category")
    plt.show()


# **Insights:**
# 
# APR category indicates a clear life-stage progression in inpatient admissions. Pediatric hospitalizations are primarily driven by neonatal care, while young adults (18–29) are largely admitted for obstetric services such as vaginal delivery and cesarean section. In middle-aged adults (30–49), reproductive admissions remain important, but infectious and systemic conditions begin to increase.
# 
# Among patients aged 50 and older, admissions are increasingly dominated by septicemia, respiratory disease, heart failure, and other chronic multi-system conditions. This shift reflects the transition from event-driven care (birth and pregnancy) to chronic and infection-related disease management with age, highlighting the growing importance of chronic care and infection control in older populations.

# In[44]:


def financial_info(diagnosis_name):
    summary = (
        df.groupby(diagnosis_name)
        .agg(
            Mean_Charges=("Total Charges", "mean"),
            Median_Charges=("Total Charges", "median"),
            Mean_Costs=("Total Costs", "mean"),
            Median_Costs=("Total Costs", "median"),
            Mean_LOS=("Length of Stay", "mean"),
            Median_LOS=("Length of Stay", "median")
        )
    )
    return summary.sort_values("Median_Charges", ascending=False)


# In[45]:


apr_mdc_summary = financial_info("APR MDC Description")
apr_mdc_summary.head(10)


# **Insights:**
# 
# APR MDC category with highest financial intensity are Myeloproliferative diseases & neoplasms with mean charge 178,301 dollars and mean LOS 10.37 days and multiple significant trauma with mean charges 156,410  dollars and mean LOS 9.37 days. These are category with high cost and high LOS. Category with moderate cost and moderate LOS are circulatory, nervous, and musculosketal system.

# In[46]:


apr_drg_summary = financial_info("APR DRG Description")
apr_drg_summary.head(10)


# **Insights:**
# 
# APR DRG analysis indicates that transplant procedures and neonatal intensive care cases represent the highest financial and LOS. Extremely premature neonates and advanced cardiopulmonary interventions exhibit mean charges exceeding $1–2 million with average stays ranging from 40 to 90 days. These findings highlight the disproportionate resource consumption of high-acuity critical care services relative to the overall average inpatient stay of 5.75 days

# In[47]:


apr_mdc_summary = financial_info("CCSR Diagnosis Description")
apr_mdc_summary.head(10)


# **Insights:**
# 
# Diagnosis-level CCSR analysis indicates that leukemia, tuberculosis, and head and neck cancers represent the highest financial and length-of-stay burden within the inpatient population. These conditions demonstrate substantial right-skewed cost distributions, reflecting the presence of highly complex cases.

# In[48]:


top_n = 5

for age, g in df.groupby("Age Group"):
    rev = (g.groupby("APR MDC Description")["Total Charges"].sum()
           .sort_values(ascending=False)
           .head(top_n))
    
    # convert to millions
    rev_m = rev / 1_000_000

    plt.figure(figsize=(8,4))
    plt.barh(rev_m.index.astype(str), rev_m.values)
    plt.title(f"Top {top_n} MDC Codes by Revenue (Millions) — Age Group: {age}")
    plt.xlabel("Total Charges ($M)")
    plt.ylabel("APR MDC Code")
    plt.gca().invert_yaxis()
    plt.show()


# **Insights:**
# 
# Revenue analysis across age groups indicates that pediatric revenue is dominated by neonatal and perinatal conditions, while young adults are primarily driven by obstetric and mental health services. Middle-aged adults exhibit a transitional mix of reproductive, infectious, and cardiovascular conditions. In older populations, circulatory, respiratory, and systemic infectious diseases become the dominant financial drivers, reflecting a shift toward chronic multi-system disease management. 

# In[49]:


#Margin by MDC
mdc_margin = (
    df.groupby("APR MDC Description")
    .agg(
        Total_Charges=("Total Charges", "sum"),
        Total_Costs=("Total Costs", "sum")
    )
)

mdc_margin["Margin"] = (
    mdc_margin["Total_Charges"] - mdc_margin["Total_Costs"]
)

mdc_margin["Margin_Percent"] = (
    mdc_margin["Margin"] / mdc_margin["Total_Charges"] * 100
)

mdc_margin.sort_values("Margin", ascending=False).head()


# In[50]:


#Margin by Age Group
age_margin = (
    df.groupby("Age Group")
    .agg(
        Total_Charges=("Total Charges", "sum"),
        Total_Costs=("Total Costs", "sum")
    )
)

age_margin["Margin"] = (
    age_margin["Total_Charges"] - age_margin["Total_Costs"]
)

age_margin["Margin_Percent"] = (
    age_margin["Margin"] / age_margin["Total_Charges"] * 100
)

age_margin


# **Insights:**
# 
# Margin analysis reveals that circulatory, nervous, and infectious disease categories generate the highest financial contribution, with margin percentages consistently near or above 70%. Age-based margin patterns demonstrate strong profitability in pediatric and elderly populations, while young adult admissions-largely driven by obstetrics and mental health services-exhibit comparatively lower margins. These findings suggest that cardiology, infection management, and high-acuity care represent key financial drivers, whereas obstetric and behavioral health services operate with tighter margins.

# In[ ]:




