# Inpatient Hospital Utilization and Financial Analysis (NY SPARCS 2021)

## Project Overview

This data contains patient details based on characteristics, diagnosis, treatments, services, and charges. This data was provided by New Yrok State Department of Health. This project explores about **2.13 million inpatient hospital stays** to understand:

- Patient demographics and utilization patterns
- Length of stay (LOS) distribution
- Clinical drivers of admission (CCSR, APR MDC, and APR DRG)
- Revenue and cost structure based on age, and clinical category
- Margin performance based on age group and clinical category

## Dataset

- Source: Hospital Inpatient Discharges (SPARCS De-Identified): 2021
- Link: https://health.data.ny.gov/Health/Hospital-Inpatient-Discharges-SPARCS-De-Identified/tg3i-cinn/about_data
- Dataset Owner: Open Data NY-DOH
- Size: 2.13 million inpatient stays
- Total rows: 2.13M
- Total columns: 33
- Key Variables:
    - Age Group
    - Gender
    - Race
    - Ethnicity
    - Length of Stay (LOS)
    - Total Charges: Total charges for the discharge
    - Total Costs: Total estimated cost for the discharge
    - CCSR Diagnosis Description: AHRQ Clinical Classification Software Refined (CCSR) diagnosis category description
    - APR MDC Description: All patient refined major diagnostic category description
    - APR DRG Description: Description of the DRG group (heart failure, pneumonia)
    - Payment Typology 1: Primary insurance or payment source
    - Payment Typology 2: Secondary insurance payer
    - Payment Typology 3: Third insurance payer
    
*Note: Data is de-identified and used for analytical purposes only.*

## Tools and Skills Demonstrated

- Python
- Data Cleaning and Transformation
- Financial Analysis (Charge, Cost, Revenue, Margin)
- Statistical Analysis
- Data Visualization
- Healthcare Classification Systems (CCSR, APR MDC, APR DRG)

## Analysis Roadmap

1. Thorough understanding the data
2. Data Cleaning and Feature Engineering
3. Length of Stay Distribution and Skewness
4. Diagnosis Level Analysis (CCSR)
5. Clinical System Analysis (APR MDC)
6. SeveritY Level Analysis (APR DRG)
7. Revenue and Cost Aggregation
8. Margin Analysis by Age Group and Clinical Category (APR MDC)

## Key Insights

### Utilization and Length of Stay
- Median length of stay is **3 days**, while mean LOS is **5.75 days**, indicating a right-skewed distribution.
- 75% of patients are discharged within **6 days**.
- Tiny percentage of high-acuity cases drive very long stays (up to 120 days).

### Age-Based Clinical Patterns
- **0-17**: Revenue dominated by neonatal and perinatal care.
- **18-29**: Admissions driven vy obstetrics and mental health.
- **30-49**: Transition stage with reproductive and infection-related admissions.
- **50+**: Cardiovascular, respiratory, and systemic infections dominate utilization.

### Clinical Drivers of Revenue
- Circulatory, infectious, respiratory, and musculoskeletal systems generate the highest total revenue.
- Oncology and severe infection cases drive high cost and longer length of stay.

### Financial Structure
- Mean total charge: **72,835 dollars**
- Mean total cost: **21,895 dollars**
- Hospital charges are approximately **2-3x higher than costs**.
- Cost distribution is highly right-skewed.

### Margin Analysis
- Overall margin remain strong across most clinical categories.
- Highest-margin age groups are pediatrics and elderly (70+).
- Circulatory and nervous system ctaegories are major financial drivers.

*Note: For detail information, kindly open the .ipynb file in Jupyter Notebook.*

### Visualizations

![distribution%20of%20length%20stay.png](attachment:distribution%20of%20length%20stay.png)

![Age%20group%20vs%20Patient%20%25%20and%20Length%20of%20Stay.png](attachment:Age%20group%20vs%20Patient%20%25%20and%20Length%20of%20Stay.png)

![Top%205%20MDC%20Categories%20in%20each%20group.png](attachment:Top%205%20MDC%20Categories%20in%20each%20group.png)

![Top%205%20MDC%20Codes%20by%20Revenue.png](attachment:Top%205%20MDC%20Codes%20by%20Revenue.png)

## Author
Sunil Sundas
