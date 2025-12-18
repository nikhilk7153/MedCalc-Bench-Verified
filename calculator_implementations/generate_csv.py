import pandas as pd
import json 
import os 
from rounding import round_number
import json
import importlib.util
import ast 

with open("/Users/nikhilkhandekar/Documents/MedCalc-Bench-Verified/calculator_implementations/name_to_python.json") as file:
    calc_info = json.load(file)

df_test = pd.read_csv("datasets/test_data_12_18_2025.csv")


csv_props = {"Row Number": [], "Calculator ID": [], "Calculator Name": [], "Category": [], "Output Type": [], "Note ID": [], "Note Type": [], 
             "Patient Note": [], "Question": [], "Relevant Entities": [], "Ground Truth Answer": [], "Lower Limit": [], "Upper Limit": [], "Ground Truth Explanation": []}


#synthesized_calc_id = [17, 25, 32, 29, 15, 21, 27, 28, 43, 36]

synthesized_calc_id = [21, 29, 28, 43, 36]

for index, row in df_test.iterrows():
    calculator_id = int(float(row["Calculator ID"]))  # Convert to float first in case of decimal format, then to int

    # Skip specific calculator IDs
    
    print(calculator_id, index + 1)

    note_type = row["Note Type"]

    if calculator_id == 68:
        row["Calculator Name"] = "Estimated Date of Conception"

    if calculator_id == 23:
        row["Question"] = "What is the patient's MeldNa (UNOS/OPTN) score?"

    csv_props["Row Number"].append(str(index + 1))
    csv_props["Calculator ID"].append(str(calculator_id))  # Convert to string when adding to csv_props
    csv_props["Calculator Name"].append(row["Calculator Name"])
    csv_props["Category"].append(row["Category"])
    csv_props["Output Type"].append(row["Output Type"])
    csv_props["Note Type"].append(note_type)
    csv_props["Patient Note"].append(row["Patient Note"])
    csv_props["Note ID"].append(row["Note ID"])

    
    try:
        relevant_entities = ast.literal_eval(row["Relevant Entities"])
    except Exception as e:
        print(f"Error in row {index}")
        print(f"Relevant Entities content: {row['Relevant Entities']}")
        print(f"Error: {e}")
        raise

    if row["Note Type"] == "Template":

        if row["Calculator ID"] != 24:
            question = calc_info[str(calculator_id)]["question"]
            csv_props["Question"].append(question)
        if row["Calculator ID"] == 24:
            question = f"Based on the patient's dose of {relevant_entities['input steroid'][0]}, what is the equivalent dosage in mg of {relevant_entities['target steroid']}?"
            csv_props["Question"].append(question)

    else:

        question = calc_info[str(calculator_id)]["question"]
        if str(calculator_id) not in ["43", "28"]:
            question = question + " " + "You should use the patient's medical values and health status when they were first admitted to the hospital prior to any treatment."

        csv_props["Question"].append(question)
    
    input_parameters = {}

    patient_note = row["Patient Note"]
    note_id = row["Note ID"]

    if row["Calculator ID"] == 49:   
        input_parameters = relevant_entities
    else:
        print(f"\nProcessing calculator_id: {calculator_id}")

     
        for entity in relevant_entities:
           
            calc_map = calc_info[str(calculator_id)]
            python_name = calc_map[entity]

            if relevant_entities[entity] == "False":
                relevant_entities[entity] = False
                input_parameters[python_name] = relevant_entities[entity]

            elif relevant_entities[entity] == "True":
                relevant_entities[entity] = True
                input_parameters[python_name] = relevant_entities[entity]

            else:
                input_parameters[python_name] = relevant_entities[entity]


        print(f"Relevant entities: {relevant_entities}")
        print(f"calc_info entry: {input_parameters}")


    # Get the file path and explanation function name
    file_path = calc_info[str(calculator_id)]["file path"]
    explanation_func_name = calc_info[str(calculator_id)]["explanation function"]
    
    # If file_path is relative, make it absolute by joining with calculator_implementations directory
    if not os.path.isabs(file_path):
        file_path = os.path.join(os.path.dirname(__file__), file_path)
    
    # Get just the filename without path and extension
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Import the module dynamically
    spec = importlib.util.spec_from_file_location(file_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Get the explanation function
    explanation_func = getattr(module, explanation_func_name)
    
    # Call the explanation function with input parameters
    func_output = explanation_func(input_parameters)
  
    csv_props["Relevant Entities"].append(relevant_entities)
    csv_props["Ground Truth Explanation"].append(func_output["Explanation"])

  
    if row["Note Type"] == "Synthetic" and row["Ground Truth Answer"] != func_output["Answer"]:
        print(row["Ground Truth Answer"], func_output["Answer"])

    if row["Category"] in ["lab test", "physical", "dosage"]:
        csv_props["Ground Truth Answer"].append(str(round_number(float(func_output["Answer"]))))
    else:
        csv_props["Ground Truth Answer"].append(func_output["Answer"])


    if row["Category"] in ["lab test", "physical", "dosage"]:
        # Calculate 5% margin for upper and lower limits properly handling negative values
        answer_value = float(func_output["Answer"])
    

        if answer_value < 0:

            print(answer_value)
            print("Lower Limit: ", round_number(answer_value * 1.05))
            print("Upper Limit: ", round_number(answer_value * 0.95))

            csv_props["Lower Limit"].append(str(round_number(answer_value * 1.05)))
            csv_props["Upper Limit"].append(str(round_number(answer_value * 0.95)))

        else:
            csv_props["Lower Limit"].append(str(round_number(answer_value * 0.95)))
            csv_props["Upper Limit"].append(str(round_number(answer_value * 1.05)))



    else:
        csv_props["Lower Limit"].append(func_output["Answer"])
        csv_props["Upper Limit"].append(func_output["Answer"])
  

df_output = pd.DataFrame(csv_props)
df_output.to_csv("datasets/test_data.csv", index=False)



 