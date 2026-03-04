# Tools API Documentation

Machine-usable argument schemas for APIs in `tools/`.

## 2: Creatinine Clearance (Cockcroft-Gault Equation)
- Module: `tools/creatinine_clearance.py`
- Function: `generate_cockcroft_gault(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `weight` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'lbs', 'g' |
| `sex` | Yes |  | `categorical` | `string` | 'Male' |
| `age` | Yes |  | `numerical` | `['number', 'unit']` | 'years', 'months', 'weeks', 'days' |
| `creatinine` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `height` | Yes |  | `numerical` | `['number', 'unit']` | 'm', 'cm', 'ft', 'in', '[feet, "ft", inches, "in"]' |

## 3: CKD-EPI Equations for Glomerular Filtration Rate
- Module: `tools/ckd-epi_2021_creatinine.py`
- Function: `ckd_epi_2021(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `age` | Yes |  | `numerical` | `['number', 'unit']` | 'years', 'months', 'weeks', 'days' |
| `sex` | Yes |  | `categorical` | `string` | 'Male', 'Female' |
| `creatinine` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |

## 4: CHA2DS2-VASc Score for Atrial Fibrillation Stroke Risk
- Module: `tools/cha2ds2_vasc_score.py`
- Function: `generate_cha2ds2_vasc(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `age` | Yes |  | `numerical` | `['number', 'unit']` | 'years', 'months', 'weeks', 'days' |
| `sex` | Yes |  | `categorical` | `string` | 'female' |
| `chf` | Yes |  | `categorical` | `boolean` | True, False |
| `hypertension` | Yes |  | `categorical` | `boolean` | True, False |
| `stroke` | Yes |  | `categorical` | `string` | any string |
| `tia` | Yes |  | `categorical` | `string` | any string |
| `thromboembolism` | Yes |  | `categorical` | `string` | any string |
| `vascular_disease` | Yes |  | `categorical` | `boolean` | True, False |
| `diabetes` | Yes |  | `categorical` | `boolean` | True, False |

## 5: Mean Arterial Pressure (MAP)
- Module: `tools/mean_arterial_pressure.py`
- Function: `mean_arterial_pressure(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `sys_bp` | Yes |  | `numerical` | `['number', 'unit']` | 'mm Hg' |
| `dia_bp` | Yes |  | `numerical` | `['number', 'unit']` | 'mm Hg' |

## 6: Body Mass Index (BMI)
- Module: `tools/bmi_calculator.py`
- Function: `bmi_calculator(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `height` | Yes |  | `numerical` | `['number', 'unit']` | 'm', 'cm', 'ft', 'in', '[feet, "ft", inches, "in"]' |
| `weight` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'lbs', 'g' |

## 7: Calcium Correction for Hypoalbuminemia
- Module: `tools/calcium_correction.py`
- Function: `calculate_corrected_calcium(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `albumin` | No | None | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `calcium` | No | None | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |

## 8: Wells' Criteria for Pulmonary Embolism
- Module: `tools/wells_criteria_pe.py`
- Function: `calculate_pe_wells(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `clinical_dvt` | Yes |  | `categorical` | `boolean` | True, False |
| `pe_number_one` | Yes |  | `categorical` | `boolean` | True, False |
| `heart_rate` | Yes |  | `numerical` | `['number', 'unit']` | 'beats per minute' |
| `immobilization_for_3days` | Yes |  | `categorical` | `string` | any string |
| `surgery_in_past4weeks` | Yes |  | `categorical` | `string` | any string |
| `previous_pe` | Yes |  | `categorical` | `string` | any string |
| `previous_dvt` | Yes |  | `categorical` | `string` | any string |
| `hemoptysis` | Yes |  | `categorical` | `boolean` | True, False |
| `malignancy_with_treatment` | Yes |  | `categorical` | `boolean` | True, False |

## 9: MDRD GFR Equation
- Module: `tools/mdrd_gfr.py`
- Function: `mrdr_gfr(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `sex` | Yes |  | `categorical` | `string` | 'Female' |
| `age` | Yes |  | `numerical` | `['number', 'unit']` | 'years', 'months', 'weeks', 'days' |
| `creatinine` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `race` | Yes |  | `categorical` | `string/boolean` | 'Black' |

## 10: Ideal Body Weight
- Module: `tools/ideal_body_weight.py`
- Function: `ibw(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `height` | Yes |  | `numerical` | `['number', 'unit']` | 'm', 'cm', 'ft', 'in', '[feet, "ft", inches, "in"]' |
| `sex` | Yes |  | `categorical` | `string` | 'Male', 'Female' |

## 11: QTc Bazett Calculator
- Module: `tools/qt_calculator_bazett.py`
- Function: `bazett_calculator(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `heart_rate` | Yes |  | `numerical` | `['number', 'unit']` | 'beats per minute' |
| `qt_interval` | Yes |  | `numerical` | `['number', 'unit']` | 'msec', 'ms' |

## 13: Estimated Due Date
- Module: `tools/estimated_due_date.py`
- Function: `add_40_weeks(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `menstrual_date` | Yes |  | `categorical` | `MM/DD/YYYY string` | any string in MM/DD/YYYY |
| `cycle_length` | Yes |  | `numerical` | `['number', 'unit']` | 'days' |

## 15: Child-Pugh Score for Cirrhosis Mortality
- Module: `tools/child_pugh_score.py`
- Function: `compute_child_pugh_score(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `inr` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |
| `ascites` | Yes |  | `categorical` | `string/boolean` | 'absent' |
| `bilirubin` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `albumin` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `encephalopathy` | No | None | `categorical` | `string` | any string |

## 16: Wells' Criteria for DVT
- Module: `tools/wells_criteria_dvt.py`
- Function: `compute_wells_criteria_dvt(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `bedridden_for_atleast_3_days` | No | False | `categorical` | `boolean` | True, False |
| `major_surgery_in_last_12_weeks` | No | False | `categorical` | `boolean` | True, False |
| `active_cancer` | No | False | `categorical` | `boolean` | True, False |
| `calf_swelling_3cm` | No | False | `categorical` | `boolean` | True, False |
| `collateral_superficial_veins` | No | False | `categorical` | `boolean` | True, False |
| `leg_swollen` | No | False | `categorical` | `boolean` | True, False |
| `localized_tenderness_on_deep_venuous_system` | No | False | `categorical` | `boolean` | True, False |
| `pitting_edema_on_symptomatic_leg` | No | False | `categorical` | `boolean` | True, False |
| `paralysis_paresis_immobilization_in_lower_extreme` | No | False | `categorical` | `boolean` | True, False |
| `previous_dvt_documented` | No | False | `categorical` | `boolean` | True, False |
| `alternative_to_dvt_diagnosis` | No | False | `categorical` | `boolean` | True, False |

## 17: Revised Cardiac Risk Index for Pre-Operative Risk
- Module: `tools/cardiac_risk_index.py`
- Function: `compute_cardiac_index(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `pre_operative_creatinine` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `elevated_risk_surgery` | No | False | `categorical` | `boolean` | True, False |
| `ischemic_heart_disease` | No | False | `categorical` | `boolean` | True, False |
| `congestive_heart_failure` | No | False | `categorical` | `boolean` | True, False |
| `cerebrovascular_disease` | No | False | `categorical` | `boolean` | True, False |
| `pre_operative_insulin_treatment` | No | False | `categorical` | `boolean` | True, False |

## 18: HEART Score for Major Cardiac Events
- Module: `tools/heart_score.py`
- Function: `compute_heart_score(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `age` | Yes |  | `numerical` | `['number', 'unit']` | 'years', 'months', 'weeks', 'days' |
| `history` | No | 'Slightly suspicious' | `categorical` | `string/boolean` | 'Highly suspicious', 'Moderately suspicious', 'Slightly suspicious' |
| `electrocardiogram` | No | 'Normal' | `categorical` | `string/boolean` | 'Non-specific repolarization disturbance', 'Normal', 'Significant ST deviation' |
| `initial_troponin` | No | 'less than or equal to normal limit' | `categorical` | `string/boolean` | 'between the normal limit or up to three times the normal limit', 'greater than three times normal limit', 'less than or equal to normal limit' |
| `hypertension` | No | False | `categorical` | `boolean` | True, False |
| `hypercholesterolemia` | No | False | `categorical` | `boolean` | True, False |
| `diabetes_mellitus` | No | False | `categorical` | `boolean` | True, False |
| `obesity` | No | False | `categorical` | `boolean` | True, False |
| `smoking` | No | False | `categorical` | `boolean` | True, False |
| `family_with_cvd` | No | False | `categorical` | `boolean` | True, False |
| `atherosclerotic_disease` | No | False | `categorical` | `boolean` | True, False |

## 19: Fibrosis-4 (FIB-4) Index for Liver Fibrosis
- Module: `tools/fibrosis_4.py`
- Function: `compute_fib4(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `age` | Yes |  | `numerical` | `['number', 'unit']` | 'years', 'months', 'weeks', 'days' |
| `ast` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |
| `alt` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |
| `platelet_count` | Yes |  | `numerical` | `['number', 'unit']` | 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3' |

## 20: Centor Score (Modified/McIsaac) for Strep Pharyngitis
- Module: `tools/centor_score.py`
- Function: `compute_centor_score(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `age` | Yes |  | `numerical` | `['number', 'unit']` | 'years', 'months', 'weeks', 'days' |
| `temperature` | Yes |  | `numerical` | `['number', 'unit']` | 'degrees celsius', 'degrees fahrenheit' |
| `cough_absent` | No | None | `categorical` | `string` | any string |
| `tender_lymph_nodes` | No | False | `categorical` | `boolean` | True, False |
| `exudate_swelling_tonsils` | No | False | `categorical` | `boolean` | True, False |

## 21: Glasgow Coma Score (GCS)
- Module: `tools/glasgow_coma_score.py`
- Function: `compute_glasgow_coma_score(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `best_eye_response` | Yes |  | `categorical` | `string` | any string |
| `best_verbal_response` | Yes |  | `categorical` | `string` | any string |
| `best_motor_response` | Yes |  | `categorical` | `string` | any string |

## 22: Maintenance Fluids Calculations
- Module: `tools/maintenance_fluid_calc.py`
- Function: `maintenance_fluid(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `weight` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'lbs', 'g' |

## 23: MELD Na (UNOS/OPTN)
- Module: `tools/meldna.py`
- Function: `compute_meldna(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `creatinine` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `dialysis_twice` | Yes |  | `categorical` | `string` | any string |
| `cvvhd` | Yes |  | `categorical` | `string` | any string |
| `bilirubin` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `inr` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |
| `sodium` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |

## 24: Steroid Conversion Calculator
- Module: `tools/steroid_conversion_calculator.py`
- Function: `compute_steroid_conversion(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `input_steroid` | Yes |  | `numerical` | `['number']` | depends on calculator (likely unitless) |
| `target_steroid` | Yes |  | `categorical` | `string` | any string |

## 25: HAS-BLED Score for Major Bleeding Risk
- Module: `tools/has_bled_score.py`
- Function: `compute_has_bled_score(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `alcoholic_drinks` | Yes |  | `categorical` | `string` | any string |
| `age` | Yes |  | `numerical` | `['number', 'unit']` | 'years', 'months', 'weeks', 'days' |
| `hypertension` | No | False | `categorical` | `boolean` | True, False |
| `liver_disease_has_bled` | No | False | `categorical` | `boolean` | True, False |
| `renal_disease_has_bled` | No | False | `categorical` | `boolean` | True, False |
| `stroke` | No | False | `categorical` | `boolean` | True, False |
| `prior_bleeding` | No | False | `categorical` | `boolean` | True, False |
| `labile_inr` | No | False | `categorical` | `boolean` | True, False |
| `medications_for_bleeding` | No | False | `categorical` | `boolean` | True, False |

## 26: Sodium Correction for Hyperglycemia
- Module: `tools/sodium_correction_hyperglycemia.py`
- Function: `compute_sodium_correction_hyperglycemia(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `sodium` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `glucose` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |

## 27: Glasgow-Blatchford Bleeding Score (GBS)
- Module: `tools/glasgow_bleeding_score.py`
- Function: `glasgow_bleeding_score(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `hemoglobin` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `bun` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `sex` | Yes |  | `categorical` | `string` | 'Male' |
| `sys_bp` | Yes |  | `numerical` | `['number', 'unit']` | 'mm Hg' |
| `heart_rate` | Yes |  | `numerical` | `['number', 'unit']` | 'beats per minute' |
| `melena_present` | No | False | `categorical` | `boolean` | True, False |
| `syncope` | No | False | `categorical` | `boolean` | True, False |
| `hepatic_disease_history` | No | False | `categorical` | `boolean` | True, False |
| `cardiac_failure` | No | False | `categorical` | `boolean` | True, False |

## 28: APACHE II Score
- Module: `tools/apache_ii.py`
- Function: `apache_ii(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `sodium` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `pH` | Yes |  | `numerical` | `['number']` | unitless |
| `heart_rate` | Yes |  | `numerical` | `['number', 'unit']` | 'beats per minute' |
| `respiratory_rate` | Yes |  | `numerical` | `['number', 'unit']` | 'breaths per minute' |
| `potassium` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `creatinine` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `hematocrit` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |
| `wbc` | Yes |  | `numerical` | `['number', 'unit']` | 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3' |
| `fio2` | Yes |  | `numerical` | `['number']` | unitless (%) |
| `gcs` | Yes |  | `categorical` | `string` | any string |
| `a_a_gradient` | No | None | `numerical` | `['number', 'unit']` | 'mm Hg' |
| `pao2` | No | None | `numerical` | `['number', 'unit']` | 'mm Hg', 'kPa' |
| `age` | No | None | `numerical` | `['number', 'unit']` | 'years', 'months', 'weeks', 'days' |
| `organ_failure_or_immunocompromise` | No | False | `categorical` | `boolean` | True, False |
| `temperature` | No | None | `numerical` | `['number', 'unit']` | 'degrees celsius', 'degrees fahrenheit' |
| `acute_renal_failure` | No | None | `categorical` | `string` | any string |
| `chronic_renal_failure` | No | None | `categorical` | `string` | any string |
| `surgery_type` | No | None | `categorical` | `string/boolean` | 'Elective', 'Emergency', 'Nonoperative' |
| `sys_bp` | No | None | `numerical` | `['number', 'unit']` | 'mm Hg' |
| `dia_bp` | No | None | `numerical` | `['number', 'unit']` | 'mm Hg' |

## 29: PSI Score: Pneumonia Severity Index for CAP
- Module: `tools/psi_score.py`
- Function: `psi_score(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `age` | Yes |  | `numerical` | `['number', 'unit']` | 'years', 'months', 'weeks', 'days' |
| `sex` | Yes |  | `categorical` | `string` | 'Female' |
| `heart_rate` | Yes |  | `numerical` | `['number', 'unit']` | 'beats per minute' |
| `temperature` | Yes |  | `numerical` | `['number', 'unit']` | 'degrees celsius', 'degrees fahrenheit' |
| `pH` | Yes |  | `numerical` | `['number']` | unitless |
| `respiratory_rate` | Yes |  | `numerical` | `['number', 'unit']` | 'breaths per minute' |
| `sys_bp` | Yes |  | `numerical` | `['number', 'unit']` | 'mm Hg' |
| `bun` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `sodium` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `glucose` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `hematocrit` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |
| `partial_pressure_oxygen` | No | None | `numerical` | `['number', 'unit']` | 'kPa', 'mm Hg' |
| `nursing_home_resident` | No | False | `categorical` | `boolean` | True, False |
| `neoplastic_disease` | No | False | `categorical` | `boolean` | True, False |
| `liver_disease` | No | False | `categorical` | `boolean` | True, False |
| `chf` | No | False | `categorical` | `boolean` | True, False |
| `cerebrovascular_disease` | No | False | `categorical` | `boolean` | True, False |
| `renal_disease` | No | False | `categorical` | `boolean` | True, False |
| `altered_mental_status` | No | False | `categorical` | `boolean` | True, False |
| `pleural_effusion` | No | False | `categorical` | `boolean` | True, False |

## 30: Serum Osmolality
- Module: `tools/sOsm.py`
- Function: `compute_serum_osmolality(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `sodium` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `bun` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `glucose` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |

## 31: HOMA-IR (Homeostatic Model Assessment for Insulin Resistance)
- Module: `tools/homa_ir.py`
- Function: `compute_homa_ir(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `insulin` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |
| `glucose` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |

## 32: Charlson Comorbidity Index (CCI)
- Module: `tools/cci.py`
- Function: `compute_cci(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `age` | Yes |  | `numerical` | `['number', 'unit']` | 'years', 'months', 'weeks', 'days' |
| `mi` | No | False | `categorical` | `boolean` | True, False |
| `chf` | No | False | `categorical` | `boolean` | True, False |
| `peripheral_vascular_disease` | No | False | `categorical` | `boolean` | True, False |
| `cva` | No | False | `categorical` | `boolean` | True, False |
| `tia` | No | False | `categorical` | `boolean` | True, False |
| `connective_tissue_disease` | No | False | `categorical` | `boolean` | True, False |
| `dementia` | No | False | `categorical` | `boolean` | True, False |
| `copd` | No | False | `categorical` | `boolean` | True, False |
| `hemiplegia` | No | False | `categorical` | `boolean` | True, False |
| `peptic_ucler_disease` | No | False | `categorical` | `boolean` | True, False |
| `liver_disease` | No | 'none' | `categorical` | `string/boolean` | 'mild', 'moderate to severe', 'none' |
| `diabetes_mellitus` | No | 'none or diet-controlled' | `categorical` | `string/boolean` | 'end-organ damage', 'uncomplicated', 'none or diet-controlled' |
| `moderate_to_severe_ckd` | No | False | `categorical` | `boolean` | True, False |
| `solid_tumor` | No | 'none' | `categorical` | `string/boolean` | 'localized', 'metastatic', 'none' |
| `leukemia` | No | False | `categorical` | `boolean` | True, False |
| `lymphoma` | No | False | `categorical` | `boolean` | True, False |
| `aids` | No | False | `categorical` | `boolean` | True, False |

## 33: FeverPAIN Score for Strep Pharyngitis
- Module: `tools/feverpain.py`
- Function: `compute_fever_pain(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `fever_24_hours` | No | False | `categorical` | `boolean` | True, False |
| `cough_coryza_absent` | No | None | `categorical` | `string` | any string |
| `symptom_onset` | No | False | `categorical` | `boolean` | True, False |
| `purulent_tonsils` | No | False | `categorical` | `boolean` | True, False |
| `severe_tonsil_inflammation` | No | False | `categorical` | `boolean` | True, False |

## 36: Caprini Score for Venous Thromboembolism (2005)
- Module: `tools/caprini_score.py`
- Function: `caprini_score(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `sex` | Yes |  | `categorical` | `string` | 'Male', 'Female' |
| `age` | Yes |  | `numerical` | `['number', 'unit']` | 'years', 'months', 'weeks', 'days' |
| `bmi` | No | None | `numerical` | `['number']` | unitless |
| `surgery_type_value` | No | None | `categorical` | `string/boolean` | 'arthroscopic', 'elective major lower extremity arthroplasty', 'laparoscopic', 'major', 'minor', 'none' |
| `mobility_value` | No | None | `categorical` | `string/boolean` | 'confined to bed >72 hours', 'normal', 'on bed rest' |
| `major_surgery_last_month` | No | False | `categorical` | `boolean` | True, False |
| `chf_last_month` | No | False | `categorical` | `boolean` | True, False |
| `sepsis` | No | False | `categorical` | `boolean` | True, False |
| `pneumonia` | No | False | `categorical` | `boolean` | True, False |
| `immobilizing_plaster_cast` | No | False | `categorical` | `boolean` | True, False |
| `hip_pelvis_leg_fracture` | No | False | `categorical` | `boolean` | True, False |
| `stroke_last_month` | No | False | `categorical` | `boolean` | True, False |
| `multiple_trauma` | No | False | `categorical` | `boolean` | True, False |
| `acute_spinal_chord_injury` | No | False | `categorical` | `boolean` | True, False |
| `varicose_veins` | No | False | `categorical` | `boolean` | True, False |
| `current_swollen_legs` | No | False | `categorical` | `boolean` | True, False |
| `current_central_venuous` | No | False | `categorical` | `boolean` | True, False |
| `previous_dvt` | No | False | `categorical` | `boolean` | True, False |
| `previous_pe` | No | False | `categorical` | `boolean` | True, False |
| `family_history_thrombosis` | No | False | `categorical` | `boolean` | True, False |
| `positive_factor_v` | No | False | `categorical` | `boolean` | True, False |
| `positive_prothrombin` | No | False | `categorical` | `boolean` | True, False |
| `serum_homocysteine` | No | False | `categorical` | `boolean` | True, False |
| `positive_lupus_anticoagulant` | No | False | `categorical` | `boolean` | True, False |
| `elevated_anticardiolipin_antibody` | No | False | `categorical` | `boolean` | True, False |
| `heparin_induced_thrombocytopenia` | No | False | `categorical` | `boolean` | True, False |
| `congenital_acquired_thrombophilia` | No | False | `categorical` | `boolean` | True, False |
| `inflammatory_bowel_disease` | No | False | `categorical` | `boolean` | True, False |
| `acute_myocardial_infarction` | No | False | `categorical` | `boolean` | True, False |
| `copd` | No | False | `categorical` | `boolean` | True, False |
| `malignancy` | No | False | `categorical` | `boolean` | True, False |

## 38: Free Water Deficit
- Module: `tools/free_water_deficit.py`
- Function: `free_water_deficit(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `age` | Yes |  | `numerical` | `['number', 'unit']` | 'years', 'months', 'weeks', 'days' |
| `sex` | Yes |  | `categorical` | `string` | 'Male', 'Female' |
| `weight` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'lbs', 'g' |
| `sodium` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |

## 39: Anion Gap
- Module: `tools/anion_gap.py`
- Function: `compute_anion_gap(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `sodium` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `chloride` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `bicarbonate` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |

## 40: Fractional Excretion of Sodium (FENa)
- Module: `tools/compute_fena.py`
- Function: `compute_fena(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `sodium` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `creatinine` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `urine_sodium` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `urine_creatinine` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |

## 43: Sequential Organ Failure Assessment (SOFA) Score
- Module: `tools/sofa.py`
- Function: `compute_sofa(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `pao2` | Yes |  | `numerical` | `['number', 'unit']` | 'mm Hg', 'kPa' |
| `fio2` | Yes |  | `numerical` | `['number']` | unitless (%) |
| `mechanical_ventilation` | Yes |  | `categorical` | `boolean` | True, False |
| `cpap` | Yes |  | `categorical` | `string` | any string |
| `sys_bp` | Yes |  | `numerical` | `['number', 'unit']` | 'mm Hg' |
| `dia_bp` | Yes |  | `numerical` | `['number', 'unit']` | 'mm Hg' |
| `gcs` | Yes |  | `numerical` | `['number']` | unitless |
| `bilirubin` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `platelet_count` | Yes |  | `numerical` | `['number', 'unit']` | 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3' |
| `creatinine` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `urine_output` | Yes |  | `numerical` | `['number', 'unit']` | 'mL/day' |
| `dopamine` | No | None | `numerical` | `['number']` | depends on calculator (likely unitless) |
| `dobutamine` | No | None | `numerical` | `['number']` | depends on calculator (likely unitless) |
| `epinephrine` | No | None | `numerical` | `['number']` | depends on calculator (likely unitless) |
| `norepinephrine` | No | None | `numerical` | `['number']` | depends on calculator (likely unitless) |
| `mechanical_ventillation` | No | None | `categorical` | `string` | any string |

## 44: LDL Calculated
- Module: `tools/ldl_calculated.py`
- Function: `compute_ldl(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `total_cholesterol` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `hdl_cholesterol` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `triglycerides` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |

## 45: CURB-65 Score for Pneumonia Severity
- Module: `tools/curb_65.py`
- Function: `curb_65(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `bun` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `respiratory_rate` | Yes |  | `numerical` | `['number', 'unit']` | 'breaths per minute' |
| `sys_bp` | Yes |  | `numerical` | `['number', 'unit']` | 'mm Hg' |
| `dia_bp` | Yes |  | `numerical` | `['number', 'unit']` | 'mm Hg' |
| `age` | Yes |  | `numerical` | `['number', 'unit']` | 'years', 'months', 'weeks', 'days' |
| `confusion` | Yes |  | `categorical` | `boolean` | True, False |

## 46: Framingham Risk Score for Hard Coronary Heart Disease
- Module: `tools/framingham_risk_score.py`
- Function: `framingham_risk_score(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `age` | Yes |  | `numerical` | `['number', 'unit']` | 'years', 'months', 'weeks', 'days' |
| `sex` | Yes |  | `categorical` | `string` | 'Male', 'Female' |
| `smoker` | Yes |  | `categorical` | `string` | any string |
| `bp_medicine` | Yes |  | `categorical` | `string` | any string |
| `total_cholesterol` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `hdl_cholesterol` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `sys_bp` | Yes |  | `numerical` | `['number', 'unit']` | 'mm Hg' |

## 48: PERC Rule for Pulmonary Embolism
- Module: `tools/perc_rule.py`
- Function: `compute_perc_rule(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `age` | Yes |  | `numerical` | `['number', 'unit']` | 'years', 'months', 'weeks', 'days' |
| `heart_rate` | Yes |  | `numerical` | `['number', 'unit']` | 'beats per minute' |
| `oxygen_sat` | Yes |  | `numerical` | `['number']` | unitless (%) |
| `previous_dvt` | No | None | `categorical` | `string/boolean` | True |
| `previous_pe` | No | None | `categorical` | `string/boolean` | True |
| `unilateral_leg_swelling` | No | False | `categorical` | `boolean` | True, False |
| `hemoptysis` | No | False | `categorical` | `boolean` | True, False |
| `recent_surgery_or_trauma` | No | False | `categorical` | `boolean` | True, False |
| `hormonal_use` | No | False | `categorical` | `boolean` | True, False |

## 49: Morphine Milligram Equivalents (MME) Calculator
- Module: `tools/mme.py`
- Function: `mme(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `codeine_dose` | No | None | `categorical` | `string` | any string |
| `codeine_dose_per_day` | No | None | `categorical` | `string` | any string |
| `fentanyl_buccal_dose` | No | None | `categorical` | `string` | any string |
| `fentanyl_buccal_dose_per_day` | No | None | `categorical` | `string` | any string |
| `fentanyl_patch_dose` | No | None | `categorical` | `string` | any string |
| `fentanyl_patch_dose_per_day` | No | None | `categorical` | `string` | any string |
| `hydrocodone_dose` | No | None | `categorical` | `string` | any string |
| `hydrocodone_dose_per_day` | No | None | `categorical` | `string` | any string |
| `hydromorphone_dose` | No | None | `categorical` | `string` | any string |
| `hydromorphone_dose_per_day` | No | None | `categorical` | `string` | any string |
| `methadone_dose` | No | None | `categorical` | `string` | any string |
| `methadone_dose_per_day` | No | None | `categorical` | `string` | any string |
| `morphine_dose` | No | None | `categorical` | `string` | any string |
| `morphine_dose_per_day` | No | None | `categorical` | `string` | any string |
| `oxycodone_dose` | No | None | `categorical` | `string` | any string |
| `oxycodone_dose_per_day` | No | None | `categorical` | `string` | any string |
| `oxymorphone_dose` | No | None | `categorical` | `string` | any string |
| `oxymorphone_dose_per_day` | No | None | `categorical` | `string` | any string |
| `tapentadol_dose` | No | None | `categorical` | `string` | any string |
| `tapentadol_dose_per_day` | No | None | `categorical` | `string` | any string |
| `tramadol_dose` | No | None | `categorical` | `string` | any string |
| `tramadol_dose_per_day` | No | None | `categorical` | `string` | any string |
| `buprenorphine_dose` | No | None | `categorical` | `string` | any string |
| `buprenorphine_dose_per_day` | No | None | `categorical` | `string` | any string |

## 51: SIRS Criteria
- Module: `tools/sirs_criteria.py`
- Function: `sirs_criteria(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `temperature` | Yes |  | `numerical` | `['number', 'unit']` | 'degrees celsius', 'degrees fahrenheit' |
| `heart_rate` | Yes |  | `numerical` | `['number', 'unit']` | 'beats per minute' |
| `wbc` | Yes |  | `numerical` | `['number', 'unit']` | 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3' |
| `respiratory_rate` | Yes |  | `numerical` | `['number', 'unit']` | 'breaths per minute' |
| `paco2` | No | None | `numerical` | `['number', 'unit']` | 'mm Hg', 'kPa' |

## 56: QTc Fridericia Calculator
- Module: `tools/qt_calculator_fredericia.py`
- Function: `fredericia_calculator(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `heart_rate` | Yes |  | `numerical` | `['number', 'unit']` | 'beats per minute' |
| `qt_interval` | Yes |  | `numerical` | `['number', 'unit']` | 'msec', 'ms' |

## 57: QTc Framingham Calculator
- Module: `tools/qt_calculator_framingham.py`
- Function: `framingham_calculator(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `heart_rate` | Yes |  | `numerical` | `['number', 'unit']` | 'beats per minute' |
| `qt_interval` | Yes |  | `numerical` | `['number', 'unit']` | 'msec', 'ms' |

## 58: QTc Hodges Calculator
- Module: `tools/qt_calculator_hodges.py`
- Function: `hodges_calculator(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `heart_rate` | Yes |  | `numerical` | `['number', 'unit']` | 'beats per minute' |
| `qt_interval` | Yes |  | `numerical` | `['number', 'unit']` | 'msec', 'ms' |

## 59: QTc Rautaharju Calculator
- Module: `tools/qt_calculator_rautaharju.py`
- Function: `rautaharju_calculator(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `heart_rate` | Yes |  | `numerical` | `['number', 'unit']` | 'beats per minute' |
| `qt_interval` | Yes |  | `numerical` | `['number', 'unit']` | 'msec', 'ms' |

## 60: Body Surface Area Calculator
- Module: `tools/bsa_calculator.py`
- Function: `bsa_calculator(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `height` | Yes |  | `numerical` | `['number', 'unit']` | 'm', 'cm', 'ft', 'in', '[feet, "ft", inches, "in"]' |
| `weight` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'lbs', 'g' |

## 61: Target weight
- Module: `tools/target_weight.py`
- Function: `targetweight(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `body_mass_index` | Yes |  | `numerical` | `['number']` | unitless |
| `height` | Yes |  | `numerical` | `['number', 'unit']` | 'm', 'cm', 'ft', 'in', '[feet, "ft", inches, "in"]' |

## 62: Adjusted Body Weight
- Module: `tools/adjusted_body_weight.py`
- Function: `abw(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `weight` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'lbs', 'g' |
| `height` | Yes |  | `numerical` | `['number', 'unit']` | 'm', 'cm', 'ft', 'in', '[feet, "ft", inches, "in"]' |
| `sex` | Yes |  | `categorical` | `string` | 'Male', 'Female' |

## 63: Delta Gap
- Module: `tools/delta_gap.py`
- Function: `compute_delta_gap(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `sodium` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |
| `chloride` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |
| `bicarbonate` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |

## 64: Delta Ratio
- Module: `tools/delta_ratio.py`
- Function: `compute_delta_ratio(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `bicarbonate` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `sodium` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |
| `chloride` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |

## 65: Albumin Corrected Anion Gap
- Module: `tools/albumin_corrected_anion.py`
- Function: `compute_albumin_corrected_anion(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `albumin` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `sodium` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |
| `chloride` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |
| `bicarbonate` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |

## 66: Albumin Corrected Delta Gap
- Module: `tools/albumin_corrected_delta_gap.py`
- Function: `compute_albumin_corrected_delta_gap(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `albumin` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |
| `sodium` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |
| `chloride` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |
| `bicarbonate` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |

## 67: Albumin Corrected Delta Ratio
- Module: `tools/albumin_delta_ratio.py`
- Function: `compute_albumin_delta_ratio(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `bicarbonate` | Yes |  | `numerical` | `['number', 'unit']` | 'kg', 'g', 'mg', 'µg', 'mol', 'mmol', 'µmol', 'pmol', 'mEq', 'L', 'dL', 'mL', 'µL', 'mm^3', 'cm^3', 'm^3', 'kg/L', 'kg/dL', 'kg/mL', 'kg/µL', 'kg/mm^3', 'kg/cm^3', 'kg/m^3', 'g/L', 'g/dL', 'g/mL', 'g/µL', 'g/mm^3', 'g/cm^3', 'g/m^3', 'mg/L', 'mg/dL', 'mg/mL', 'mg/µL', 'mg/mm^3', 'mg/cm^3', 'mg/m^3', 'µg/L', 'µg/dL', 'µg/mL', 'µg/µL', 'µg/mm^3', 'µg/cm^3', 'µg/m^3', 'mol/L', 'mol/dL', 'mol/mL', 'mol/µL', 'mol/mm^3', 'mol/cm^3', 'mol/m^3', 'mmol/L', 'mmol/dL', 'mmol/mL', 'mmol/µL', 'mmol/mm^3', 'mmol/cm^3', 'mmol/m^3', 'µmol/L', 'µmol/dL', 'µmol/mL', 'µmol/µL', 'µmol/mm^3', 'µmol/cm^3', 'µmol/m^3', 'pmol/L', 'pmol/dL', 'pmol/mL', 'pmol/µL', 'pmol/mm^3', 'pmol/cm^3', 'pmol/m^3', 'mEq/L', 'mEq/dL', 'mEq/mL', 'mEq/µL', 'mEq/mm^3', 'mEq/cm^3', 'mEq/m^3' |
| `albumin` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |
| `sodium` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |
| `chloride` | Yes |  | `numerical` | `['number', 'unit']` | not explicitly constrained in function |

## 68: Estimated Date of Conception
- Module: `tools/estimated_conception_date.py`
- Function: `add_2_weeks(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `menstrual_date` | Yes |  | `categorical` | `MM/DD/YYYY string` | any string in MM/DD/YYYY |

## 69: Estimated Gestational Age
- Module: `tools/estimated_gestational_age.py`
- Function: `compute_gestational_age(...)`

| Argument | Required | Default | Kind | Format | Values/Units |
|---|---:|---|---|---|---|
| `current_date` | Yes |  | `categorical` | `MM/DD/YYYY string` | any string in MM/DD/YYYY |
| `menstrual_date` | Yes |  | `categorical` | `MM/DD/YYYY string` | any string in MM/DD/YYYY |

