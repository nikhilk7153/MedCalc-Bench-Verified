# CALCULATORs

Reference calculations and sources for each calculator (ordered by Calculator ID from calculator_implementations/calc_path.json).

## 2 - Creatinine Clearance (Cockcroft-Gault Equation)
Reference calculation:
- CrCl (mL/min) = ((140 - age) * weight_kg) / (72 * serum_creatinine_mg_dL); multiply by 0.85 if female.
Notes:
- Cockcroft-Gault is not adjusted for body surface area and may be less accurate in obese patients; it can overestimate creatinine clearance in some settings.
Alternative (default): implementation weight-selection logic (BMI-based)
- Underweight (BMI < 18.5): use actual body weight.
- Normal (BMI 18.5-24.9): use min(IBW, actual body weight).
- Overweight/obese (BMI >= 25): use adjusted body weight (AdjBW = IBW + 0.4 * (ABW - IBW)).
Implementation note:
- This BMI-threshold approach is an implementation choice. Other institutional guidance selects weight based on ABW vs IBW (use ABW if ABW <= IBW, otherwise AdjBW), even though IBW/AdjBW formulas match.
Sources:
- https://www.kidney.org/professionals/kdoqi/gfr_calculatorCoc
- https://www.hiv.uw.edu/page/clinical-calculators/crcl
- https://handbook.ggcmedicines.org.uk/guidelines/infections/manual-calculation-of-creatinine-clearance/

## 3 - CKD-EPI Equations for Glomerular Filtration Rate
Reference calculation:
- 2021 CKD-EPI creatinine equation (race-free): eGFR = 142 * min(SCr/k,1)^a * max(SCr/k,1)^-1.200 * 0.9938^Age * 1.012 (if female).
- k = 0.7 (female) or 0.9 (male); a = -0.241 (female) or -0.302 (male); SCr in mg/dL.
Sources:
- https://www.niddk.nih.gov/health-information/professionals/clinical-tools-patient-management/glomerular-filtration-rate-ckd-epi-adults-conventional-units

## 4 - CHA2DS2-VASc Score for Atrial Fibrillation Stroke Risk
Reference calculation:
- Sum points across criteria.
Scoring details:
- Congestive heart failure: 1
- Hypertension: 1
- Age >= 75 years: 2
- Diabetes mellitus: 1
- Prior stroke/TIA: 2
- Vascular disease: 1
- Age 65-74 years: 1
- Female sex: 1
Sources:
- https://www.msdmanuals.com/professional/multimedia/table/cha2ds2-vasc-score

## 5 - Mean Arterial Pressure (MAP)
Reference calculation:
- MAP = (SBP + 2 * DBP) / 3 = DBP + (SBP - DBP) / 3.
Sources:
- https://www.ncbi.nlm.nih.gov/books/NBK538226/

## 6 - Body Mass Index (BMI)
Reference calculation:
- BMI = weight_kg / (height_m^2).
Sources:
- https://clincalc.com/weight/ibw.aspx

## 7 - Calcium Correction for Hypoalbuminemia
Reference calculation:
- Corrected calcium (mg/dL) = measured calcium + 0.8 * (4.0 - albumin_g_dL).
Sources:
- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9816933/

## 8 - Wells' Criteria for Pulmonary Embolism
Reference calculation:
- Sum points across criteria.
Scoring details:
- Clinical signs of DVT: 3
- Alternative diagnosis less likely than PE: 3
- Heart rate > 100 bpm: 1.5
- Immobilization >= 3 days or surgery within 4 weeks: 1.5
- Previous DVT/PE: 1.5
- Hemoptysis: 1
- Malignancy: 1
Interpretation:
- Traditional: low < 2, moderate 2-6, high > 6
- Modified: PE unlikely <= 4, PE likely > 4
Sources:
- https://www.ncbi.nlm.nih.gov/books/NBK585742/table/ch12.Tab4/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC11152639/

## 9 - MDRD GFR Equation
Reference calculation:
- eGFR = 175 * SCr^-1.154 * Age^-0.203 * 0.742 (if female) * 1.212 (if Black); SCr in mg/dL.
Sources:
- https://www.niddk.nih.gov/health-information/professionals/clinical-tools-patient-management/glomerular-filtration-rate/previous-egfr-equations

## 10 - Ideal Body Weight
Reference calculation:
- Male: IBW = 50 kg + 2.3 kg * (height_in - 60).
- Female: IBW = 45.5 kg + 2.3 kg * (height_in - 60).
Sources:
- https://clincalc.com/weight/ibw.aspx

## 11 - QTc Bazett Calculator
Reference calculation:
- QTc = QT / sqrt(RR).
Sources:
- https://www.qtcalculator.org/

## 13 - Estimated Due Date
Reference calculation:
- Naegele's rule: EDD = LMP + 280 days (40 weeks). Adjust by cycle length difference from 28 days.
Sources:
- https://www.hopkinsmedicine.org/health/wellness-and-prevention/calculating-a-due-date

## 15 - Child-Pugh Score for Cirrhosis Mortality
Reference calculation:
- Sum 1-3 points for each factor; total score 5-15.
Scoring details (1 / 2 / 3 points):
- Bilirubin (mg/dL): <2 / 2-3 / >3
- Albumin (g/dL): >3.5 / 2.8-3.5 / <2.8
- INR or PT: INR <1.7 (or PT <4 sec) / INR 1.7-2.3 (PT 4-6 sec) / INR >2.3 (PT >6 sec)
- Ascites: none / mild / moderate-severe
- Encephalopathy: none / grade 1-2 / grade 3-4
Class:
- A: 5-6
- B: 7-9
- C: 10-15
Sources:
- https://my.clevelandclinic.org/health/diagnostics/child-pugh-score

## 16 - Wells' Criteria for DVT
Reference calculation:
- Sum points across criteria.
Scoring details:
- Active cancer (treatment ongoing, within 6 months, or palliative): +1
- Paralysis, paresis, or recent plaster immobilization of lower extremities: +1
- Recently bedridden >= 3 days or major surgery within 12 weeks: +1
- Localized tenderness along the deep venous system: +1
- Entire leg swollen: +1
- Calf swelling > 3 cm compared with asymptomatic leg: +1
- Pitting edema (greater in symptomatic leg): +1
- Collateral superficial veins (nonvaricose): +1
- Previous DVT documented: +1
- Alternative diagnosis as likely as DVT: -2
Interpretation:
- 3-tier: <=0 low, 1-2 moderate, >=3 high
- 2-tier: >=2 DVT likely, <=1 DVT unlikely
Sources:
- https://emedicine.medscape.com/article/1918446-images
- https://pmc.ncbi.nlm.nih.gov/articles/PMC5045251/

## 17 - Revised Cardiac Risk Index for Pre-Operative Risk
Reference calculation:
- Sum 1 point for each risk factor.
Scoring details:
- High-risk surgery (intraperitoneal, intrathoracic, or suprainguinal vascular): 1
- Ischemic heart disease: 1
- Congestive heart failure: 1
- Cerebrovascular disease: 1
- Diabetes requiring insulin: 1
- Creatinine > 2.0 mg/dL: 1
Sources:
- https://www.aafp.org/pubs/afp/issues/2013/0315/p414.html

## 18 - HEART Score for Major Cardiac Events
Reference calculation:
- Sum 0-2 points per component (History, ECG, Age, Risk factors, Troponin).
Scoring details:
- History: highly suspicious (2), moderately suspicious (1), slightly suspicious (0)
- ECG: significant ST deviation (2), nonspecific repolarization disturbance (1), normal (0)
- Age: >65 (2), 45-65 (1), <45 (0)
- Risk factors: >=3 risk factors or known atherosclerotic disease (2), 1-2 risk factors (1), none (0)
- Troponin: >2x normal (2), 1-2x normal (1), <= normal (0)
Sources:
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9635776/

## 19 - Fibrosis-4 (FIB-4) Index for Liver Fibrosis
Reference calculation:
- FIB-4 = (Age * AST) / (Platelets * sqrt(ALT)), with AST/ALT in U/L and platelets in 10^9/L.
Sources:
- https://www.hepatitis.va.gov/hcv/patient/advanced/liver-fibrosis-4.asp

## 20 - Centor Score (Modified/McIsaac) for Strep Pharyngitis
Reference calculation:
- Sum 1 point for each clinical criterion, then apply age adjustment.
Scoring details:
- Fever (>38 C): +1
- Tonsillar exudate/swelling: +1
- Tender anterior cervical adenopathy: +1
- Absence of cough: +1
- Age 3-14: +1
- Age 15-44: 0
- Age >=45: -1
Sources:
- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7121545/
- https://www.aafp.org/pubs/afp/issues/2016/0701/p24.html

## 21 - Glasgow Coma Score (GCS)
Reference calculation:
- Eye opening (1-4) + verbal response (1-5) + motor response (1-6) = total 3-15.
Scoring details:
- Eye: spontaneous (4), to verbal command (3), to pain (2), none (1)
- Verbal: oriented (5), confused (4), inappropriate words (3), incomprehensible sounds (2), none (1)
- Motor: obeys commands (6), localizes pain (5), withdraws from pain (4), abnormal flexion (3), abnormal extension (2), none (1)
Implementation note:
- If a component is not testable, it is marked NT and excluded from the summed total.
Sources:
- https://www.merckmanuals.com/professional/multimedia/table/glasgow-coma-scale

## 22 - Maintenance Fluids Calculations
Reference calculation:
- Holliday-Segar: 100 mL/kg for first 10 kg + 50 mL/kg for next 10 kg + 20 mL/kg for each kg >20. Divide by 24 for mL/hr.
Sources:
- https://www.msdmanuals.com/professional/pediatrics/fluid-and-electrolyte-disorders-in-children/maintenance-fluid-requirements

## 23 - MELD Na (UNOS/OPTN)
Reference calculation:
- OPTN MELD 3.0 (candidates >=18 at registration):
  MELD = 1.33 * (female) + 4.56 * ln(bilirubin) + 0.82 * (137 - Na) - 0.24 * (137 - Na) * ln(bilirubin) + 9.09 * ln(INR) + 11.14 * ln(creatinine) + 1.85 * (3.5 - albumin) - 1.83 * (3.5 - albumin) * ln(creatinine) + 6.
- OPTN MELD 3.0 (candidates 12-17 at registration):
  MELD = 4.56 * ln(bilirubin) + 0.82 * (137 - Na) - 0.24 * (137 - Na) * ln(bilirubin) + 9.09 * ln(INR) + 11.14 * ln(creatinine) + 1.85 * (3.5 - albumin) - 1.83 * (3.5 - albumin) * ln(creatinine) + 7.33.
- Floors/caps: bilirubin, INR, creatinine min 1.0; creatinine max 3.0 and set to 3.0 if dialysis >=2x in prior 7 days or 24h CVVHD; sodium 125-137; albumin 1.5-3.5.
- Result rounded to nearest whole number; min 6, max 40.
Sources:
- https://optn.transplant.hrsa.gov/media/3idbp5vq/policy-guid-change_improving-liver-allocation-meld-peld-status-1a-1b.pdf
- https://optn.transplant.hrsa.gov/learn/professional-education/learn-about-meld-and-peld/

## 24 - Steroid Conversion Calculator
Reference calculation:
- Equivalent doses (approx): hydrocortisone 20 mg, cortisone 25 mg, prednisone/prednisolone 5 mg, methylprednisolone 4 mg, triamcinolone 4 mg, dexamethasone 0.75 mg, betamethasone 0.75 mg.
Sources:
- https://immunisationhandbook.health.gov.au/resources/tables/table-equivalent-corticosteroid-dose

## 25 - HAS-BLED Score for Major Bleeding Risk
Reference calculation:
- Sum 1 point for each criterion (renal and liver function counted separately; drugs and alcohol counted separately).
Scoring details:
- Hypertension: 1
- Abnormal kidney function: 1
- Abnormal liver function: 1
- Prior stroke: 1
- Prior bleeding: 1
- Labile INR: 1
- Age > 65: 1
- Concomitant NSAID or antiplatelet use: 1
- Alcohol > 8 units/week: 1
Sources:
- https://www.merckmanuals.com/professional/multimedia/table/has-bled-tool-for-predicting-risk-of-bleeding-in-patients-with-atrial-fibrillation

## 26 - Sodium Correction for Hyperglycemia
Reference calculation:
- Corrected Na = measured Na + 0.024 * (glucose_mg_dL - 100).
Sources:
- https://ebmcalc.com/SodiumCorrection.htm

## 27 - Glasgow-Blatchford Bleeding Score (GBS)
Reference calculation:
- Sum points for BUN, hemoglobin, systolic BP, and clinical markers.
Scoring details:
- BUN (mmol/L): <6.5 (0), 6.5-8.0 (2), 8.0-10.0 (3), 10.0-25 (4), >25 (6)
- Hemoglobin (g/dL), men: >=13.0 (0), 12.0-12.9 (1), 10.0-11.9 (3), <10.0 (6)
- Hemoglobin (g/dL), women: >=12.0 (0), 10.0-11.9 (1), <10.0 (6)
- Systolic BP (mm Hg): >109 (0), 100-109 (1), 90-99 (2), <90 (3)
- Other markers: pulse >=100 (1), melena (1), syncope (2), hepatic disease (2), cardiac failure (2)
Sources:
- https://globalrph.com/medcalcs/glasgow-blatchford-bleeding-score-gbs/

## 28 - APACHE II Score
Reference calculation:
- APACHE II = acute physiology score (12 variables, worst value in first 24h) + age points + chronic health points.
- Oxygenation: if FIO2 >= 0.5, score by A-a gradient; if FIO2 < 0.5, score by PaO2.
Scoring details (acute physiology points):
- Temperature C: >=41 (4), 39-40.9 (3), 38.5-38.9 (1), 36-38.4 (0), 34-35.9 (1), 32-33.9 (2), 30-31.9 (3), <=29.9 (4)
- MAP mm Hg: >=160 (4), 130-159 (3), 110-129 (2), 70-109 (0), 50-69 (2), <=49 (4)
- Heart rate: >=180 (4), 140-179 (3), 110-139 (2), 70-109 (0), 55-69 (2), 40-54 (3), <=39 (4)
- Respiratory rate: >=50 (4), 35-49 (3), 25-34 (1), 12-24 (0), 10-11 (1), 6-9 (2), <=5 (4)
- Oxygenation:
  - FIO2 >=0.5 (A-a gradient): >=500 (4), 350-499 (3), 200-349 (2), <200 (0)
  - FIO2 <0.5 (PaO2 mm Hg): >70 (0), 61-70 (1), 55-60 (3), <55 (4)
- Arterial pH: >=7.7 (4), 7.6-7.69 (3), 7.5-7.59 (1), 7.33-7.49 (0), 7.25-7.32 (2), 7.15-7.24 (3), <7.15 (4)
- Sodium (mEq/L): >=180 (4), 160-179 (3), 155-159 (2), 150-154 (1), 130-149 (0), 120-129 (2), 111-119 (3), <=110 (4)
- Potassium (mEq/L): >=7 (4), 6-6.9 (3), 5.5-5.9 (1), 3.5-5.4 (0), 3-3.4 (1), 2.5-2.9 (2), <2.5 (4)
- Creatinine (mg/dL): >=3.5 (4), 2-3.4 (3), 1.5-1.9 (2), 0.6-1.4 (0), <0.6 (2) (double points if acute renal failure)
- Hematocrit (%): >=60 (4), 50-59.9 (2), 46-49.9 (1), 30-45.9 (0), 20-29.9 (2), <20 (4)
- WBC (10^3/mm^3): >=40 (4), 20-39.9 (2), 15-19.9 (1), 3-14.9 (0), 1-2.9 (2), <1 (4)
- GCS: points = 15 - actual GCS
Age points:
- <44 (0), 45-54 (2), 55-64 (3), 65-74 (5), >=75 (6)
Chronic health points:
- 2 points if elective postop with severe organ insufficiency or immunocompromise
- 5 points if nonoperative/emergency postop with severe organ insufficiency or immunocompromise
Sources:
- https://www.merckmanuals.com/professional/multimedia/table/acute-physiologic-assessment-and-chronic-health-evaluation-apache-ii-scoring-system

## 29 - PSI Score: Pneumonia Severity Index for CAP
Reference calculation:
- Sum points across demographics, comorbidities, exam findings, labs, and radiographic findings.
Scoring details:
- Demographics: male = age in years; female = age in years - 10; nursing home resident +10
- Comorbidities: cancer +30, liver disease +20, heart failure +10, cerebrovascular disease +10, renal disease +10
- Physical exam: altered mental status +20; RR >=30 +20; SBP <90 +20; temperature >=40 or <35 +15; pulse >=125 +10
- Labs/radiograph: arterial pH <7.35 +30; BUN >=30 mg/dL +20; sodium <130 +20; glucose >=250 +10; hematocrit <30 +10; PaO2 <60 or O2 sat <90% +10; pleural effusion +10
Risk classes (points):
- <=70
- 71-90
- 91-130
- >130
Sources:
- https://www.merckmanuals.com/professional/multimedia/table/risk-stratification-for-community-acquired-pneumonia-the-pneumonia-severity-index

## 30 - Serum Osmolality
Reference calculation:
- Calculated serum osmolality = 2 * Na + (glucose/18) + (BUN/2.8); Na in mmol/L, glucose and BUN in mg/dL.
Sources:
- https://emedicine.medscape.com/article/2088259-overview

## 31 - HOMA-IR (Homeostatic Model Assessment for Insulin Resistance)
Reference calculation:
- HOMA-IR = (glucose_mg_dL * insulin_uIU_mL) / 405.
Sources:
- https://www.elsevier.es/en-revista-endocrinologia-diabetes-nutricion-13-articulo-finder-homa-index-S2530016417301445

## 32 - Charlson Comorbidity Index (CCI)
Reference calculation:
- Weighted sum of comorbidities (1, 2, 3, or 6 points). Total score is the sum of all weights.
Sources:
- https://www.ncbi.nlm.nih.gov/books/NBK557680/table/article-37703.table0/?report=objectonly

## 33 - FeverPAIN Score for Strep Pharyngitis
Reference calculation:
- 1 point each: fever in prior 24h, purulent tonsils, attend rapidly (<=3 days), severely inflamed tonsils, no cough/coryza. Sum points (0-5).
Implementation note:
- If cough/coryza status is missing, the implementation does not award a point for that criterion.
Sources:
- https://www.aafp.org/pubs/afp/issues/2014/0615/p976.html

## 36 - Caprini Score for Venous Thromboembolism (2005)
Reference calculation:
- Assign points (1, 2, 3, or 5) for risk factors defined in the Caprini RAM; sum points.
Scoring details:
- 2005 revision risk groups: low 0-1, moderate 2, high 3-4, highest >=5.
Implementation note:
- Current implementation covers a subset of Caprini RAM factors. Within that subset, immobilizing plaster cast is 2 points and BMI is scored when >25 kg/m^2.
Sources:
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9783939/
- https://www.ncbi.nlm.nih.gov/books/NBK616080/

## 38 - Free Water Deficit
Reference calculation:
- Free water deficit = TBW * (serum Na/140 - 1), with TBW = weight_kg * factor (adult male 0.6, adult female 0.5, elderly male 0.5, elderly female 0.45, child 0.6).
Sources:
- https://emedicine.medscape.com/article/241844-overview

## 39 - Anion Gap
Reference calculation:
- Anion gap = Na - (Cl + HCO3).
Sources:
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9816933/

## 40 - Fractional Excretion of Sodium (FENa)
Reference calculation:
- FENa (%) = (urine Na * serum creatinine) / (serum Na * urine creatinine) * 100.
Sources:
- https://www.mdcalc.com/calc/615/fractional-excretion-sodium-fena

## 43 - Sequential Organ Failure Assessment (SOFA) Score
Reference calculation:
- Score 0-4 for each organ system (respiratory, coagulation, liver, cardiovascular, CNS, renal) and sum points.
Scoring details:
- Respiratory (PaO2/FIO2 mm Hg): >=400 (0), <400 (1), <300 (2), <200 with respiratory support (3), <100 with respiratory support (4)
- Coagulation (platelets x10^3/uL): >=150 (0), <150 (1), <100 (2), <50 (3), <20 (4)
- Liver (bilirubin mg/dL): <1.2 (0), 1.2-1.9 (1), 2.0-5.9 (2), 6.0-11.9 (3), >12.0 (4)
- Cardiovascular: MAP >=70 (0), MAP <70 (1), dopamine <=5 or dobutamine any dose (2), dopamine >5 or epi <=0.1 or norepi <=0.1 (3), dopamine >15 or epi >0.1 or norepi >0.1 (4)
- CNS (GCS): 15 (0), 13-14 (1), 10-12 (2), 6-9 (3), <6 (4)
- Renal (creatinine mg/dL or urine output): <1.2 (0), 1.2-1.9 (1), 2.0-3.4 (2), 3.5-4.9 or urine <500 mL/day (3), >=5.0 or urine <200 mL/day (4)
Sources:
- https://www.merckmanuals.com/professional/multimedia/table/sequential-organ-failure-assessment-sofa-score

## 44 - LDL Calculated
Reference calculation:
- Friedewald formula: LDL = total cholesterol - HDL - (triglycerides/5), in mg/dL.
Sources:
- https://pathology.jhu.edu/build/assets/department/files/LDL-Calc-Friedewald.pdf

## 45 - CURB-65 Score for Pneumonia Severity
Reference calculation:
- 1 point each: Confusion, BUN >7 mmol/L (or >20 mg/dL), RR >=30, SBP <90 or DBP <=60, Age >=65.
Sources:
- https://bmcpulmmed.biomedcentral.com/articles/10.1186/1471-2466-14-149/tables/1

## 46 - Framingham Risk Score for Hard Coronary Heart Disease
Reference calculation:
- Use sex-specific point tables for age, total cholesterol, HDL, SBP (treated/untreated), smoking, and diabetes; sum points and map to 10-year risk.
Alternative (default): continuous ATP III hard CHD function (matches implementation)
- Men: risk_score = 52.00961*ln(age) + 20.014077*ln(total_cholesterol) - 0.905964*ln(HDL) + 1.305784*ln(SBP) + 0.241549*(bp_meds) + 12.096316*(smoker) - 4.605038*ln(age)*ln(total_cholesterol) - 2.84367*ln(age_smoke)*smoker - 2.93323*ln(age)^2 - 172.300168.
- Women: risk_score = 31.764001*ln(age) + 22.465206*ln(total_cholesterol) - 1.187731*ln(HDL) + 2.552905*ln(SBP) + 0.420251*(bp_meds) + 13.07543*(smoker) - 5.060998*ln(age)*ln(total_cholesterol) - 2.996945*ln(age_smoke)*smoker - 146.5933061.
- Age cap for ln(age_smoke): use ln(70) for men and ln(78) for women if age exceeds those values.
- 10-year risk (%) = (1 - S0^exp(risk_score)) * 100, where S0 = 0.9402 (men) or 0.98767 (women).
Sources:
- https://framinghamheartstudy.org/fhs-risk-functions/hard-coronary-heart-disease-10-year-risk/

## 48 - PERC Rule for Pulmonary Embolism
Reference calculation:
- PERC negative only if all criteria are met (all negative).
Scoring details:
- Age <50
- Pulse <100
- O2 saturation >94%
- No unilateral leg swelling
- No hemoptysis
- No recent trauma or surgery
- No history of VTE
- No oral hormone use
Implementation note:
- Dataset expects a count of criteria met (0-8). PERC negative corresponds to 0 and positive to >=1.
- Future dataset change planned: switch output to binary negative/positive instead of a count.
Sources:
- https://www.acc.org/Latest-in-Cardiology/Articles/2020/07/10/08/44/2019-ESC-Guidelines-for-the-Diagnosis-and-Management-of-Acute-PE

## 49 - Morphine Milligram Equivalents (MME) Calculator
Reference calculation:
- Daily MME = sum(daily opioid dose * conversion factor) across opioids.
- Use CDC MME conversion factors for each opioid formulation.
Implementation note:
- Methadone uses the CDC 2022 fixed factor (4.7) rather than dose-dependent factors from older guidance.
 - Fentanyl patch doses are expected in µg/hr; transmucosal/buccal fentanyl is not supported in this calculator.
Sources:
- https://stacks.cdc.gov/view/cdc/100433
- https://www.cdc.gov/opioids/providers/prescribing/opioid-oral-morphine-milligram-equivalent-mme-conversion-factors.html

## 51 - SIRS Criteria
Reference calculation:
- 1 point each: Temp >38C or <36C, HR >90, RR >20 or PaCO2 <32, WBC >12 or <4 or >10% bands. SIRS is >=2 criteria.
Implementation note:
- Bands criterion is applied only if a bands (%) input is supplied.
Sources:
- https://www.ncbi.nlm.nih.gov/books/NBK547669/

## 56 - QTc Fridericia Calculator
Reference calculation:
- QTc = QT / RR^(1/3).
Sources:
- https://www.qtcalculator.org/

## 57 - QTc Framingham Calculator
Reference calculation:
- QTc = QT + 0.154 * (1 - RR).
Implementation note:
- If QT is in milliseconds and RR in seconds, the coefficient is 154 ms (equivalent to 0.154 s).
Sources:
- https://www.qtcalculator.org/

## 58 - QTc Hodges Calculator
Reference calculation:
- QTc = QT + 1.75 * (HR - 60).
Sources:
- https://www.qtcalculator.org/

## 59 - QTc Rautaharju Calculator
Reference calculation:
- QTcRTH = QT * (120 + HR) / 180.
Sources:
- https://pubmed.ncbi.nlm.nih.gov/30260244/

## 60 - Body Surface Area Calculator
Reference calculation:
- Mosteller: BSA = sqrt((height_cm * weight_kg) / 3600).
Sources:
- https://clincalc.com/weight/ibw.aspx

## 61 - Target weight
Reference calculation:
- Target weight (kg) = target BMI * (height_m^2).
Sources:
- https://clincalc.com/weight/ibw.aspx

## 62 - Adjusted Body Weight
Reference calculation:
- ABW = IBW + 0.4 * (total body weight - IBW).
Sources:
- https://clincalc.com/weight/ibw.aspx

## 63 - Delta Gap
Reference calculation:
- Delta gap (delta anion gap) = anion gap - 12.
Sources:
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9816933/

## 64 - Delta Ratio
Reference calculation:
- Delta ratio = (anion gap - 12) / (24 - HCO3).
Sources:
- https://www.ncbi.nlm.nih.gov/books/NBK554570/

## 65 - Albumin Corrected Anion Gap
Reference calculation:
- Albumin-corrected AG = AG + 2.5 * (4 - albumin_g_dL).
Sources:
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9816933/

## 66 - Albumin Corrected Delta Gap
Reference calculation:
- Albumin-corrected delta gap = (AG + 2.5 * (4 - albumin_g_dL)) - 12.
Sources:
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9816933/

## 67 - Albumin Corrected Delta Ratio
Reference calculation:
- Albumin-corrected delta ratio = ((AG + 2.5 * (4 - albumin_g_dL)) - 12) / (24 - HCO3).
Sources:
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9816933/

## 68 - Estimated of Conception
Reference calculation:
- Estimated date of conception = LMP + 14 days (about 2 weeks after last menstrual period).
Sources:
- https://americanpregnancy.org/getting-pregnant/estimated-date-of-conception/

## 69 - Estimated Gestational Age
Reference calculation:
- Gestational age = difference between current date and LMP, expressed as weeks and days.
Sources:
- https://emedicine.medscape.com/article/260300-overview
