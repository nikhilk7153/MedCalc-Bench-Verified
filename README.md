
# Updates

Updates to MedCalc-Bench Verified will be made on this page going forward. Here is the HuggingFace link to the dataset: https://huggingface.co/datasets/nsk7153/MedCalc-Bench-Verified. 

This is an updated version that is modified from MedCalc-Bench-v1.2

# MedCalc-Bench Verified

MedCalc-Bench Verified is a re-verified version of MedCalc-Bench used to benchmark LLMs ability to serve as clinical calculators. Each instance in the dataset consists of a patient note, a question asking to compute a specific clinical value, a final answer value, and a step-by-step solution explaining how the final answer was obtained. Our dataset covers 55 different calculation tasks which are either rule-based calculations or are equation-based calculations. This dataset contains a training dataset of 10,538 instances and a testing dataset of 1,100 instances.
 <br>

In all, we hope that our dataset and benchmark serves as a call to improve the computational reasoning skills of LLMs in medical settings. 

## Dataset Details


In addition to the 1,100 evaluation instances, there is a training dataset of 10,538 instances which can be used for fine-tuning open-source LLMs. The training data can be found in ```train_data.csv```. This training dataset can also be found in the train split of the HuggingFace link. 

Each Instance in the dataset contains the following information: 

- **Row Number**: Specifies the index of the instance.
- **Calculator ID**: Specifies the integer ID of the calculator.
- **Calculator Name**: Specifies the name of the clinical calculation task.
- **Category**: Specifies the sub-category of the calculator. For equation-based calculators, the options are lab test, dosage, date, or physical and for rule-based calculators, the options are risk, severity, and diagnosis.
- **Output Type**: Specifies the format type that the calculator will return. The options are decimal, integer, date (MM/DD/YY), or time in terms of weeks and days (i.e. (17 weeks, 4 days)).
- **Note ID**: Specifies the ID of the patient note. The ID of the note will either be the ID given by Open-Patients or it will be an integer value if the patient note was handwritten by clinicians or synthesized by a template.
- **Note Type**: Specifies whether the patient note was LLM generated and then edited/approved by a clinician (Synthetic), produced from a python template (Template), or was extracted from PMC-Patients (Extracted).
- **Patient Note**: Specifies the patient note which provides the information needed to compute the final answer.
- **Question**: Specifies the question that is asked to the model to compute a specific medical value based on a particular calculator.
- **Relevant Entities**: Provides a dictionary of the parameters and their extracted values based on the patient note.
- **Ground Truth Answer**: Specifies the ground truth value without any units for the medical value that needs to be calculated.
- **Lower Limit**: For equation-based calculators whose output is a decimal, this value is 95% of the ground truth answer value. For all other cases, the lower limit is the same as the ground-truth value.
- **Upper Limit**: For equation-based calculators whose output is a decimal, this value is 105% of the ground truth answer value. For all other cases, the upper limit is the same as the ground-truth value.
- **Ground Truth Explanation**: The ground truth explanation for the data instance providing a step-by-step explanation for how the final answer was obtained.

## Reproducing Main Results 

To install all the packages needed for this project, please run the following command: ```conda env create -f environment.yml```. This command will create the ```medcalc-bench``` conda environment. For running OpenAI models, you will need to provide your OpenAI key in this conda environment. You can do this by executing the following command in the ```medcalc-bench``` environment: ```export OPENAI_API_KEY = YOUR_API_KEY```, where YOUR_API_KEY is your OpenAI API key. You will also need to provide your HuggingFace token in this environment by running the following command: ```export HUGGINGFACE_TOKEN=your_hugging_face_token```, where ```your_hugging_face_token``` is your huggingface token. 


For reproducing the Table 2 from the original paper, first `cd` into the `evaluation` folder. Then, please run the following command: ```python run.py --model <model_name> and --prompt <prompt_style>```.

The options for `--model` are below:

- Mistral-7B: mistralai/Mistral-7B-Instruct-v0.2
- Mixtral-8x7B: mistralai/Mixtral-8x7B-Instruct-v0.1
- Llama3-8B: meta-llama/Meta-Llama-3-8B-Instruct
- Llama3-70B: meta-llama/Meta-Llama-3-70B-Instruct
- Meditron-70B: epfl-llm/meditron-70b
- GPT-3.5: OpenAI/gpt-3.5-turbo
- GPT-4: OpenAI/gpt-4
- PMC-Llama-13B: axiong/PMC_LLaMA_13B

The options for `--prompt` are below:

- Direct Answer: direct_answer 
- Zero Shot Chain of Thought: zero_shot
- One Shot Chain of Though: one_shot_cot

From this, you will get one jsonl file outputting the status of every question: Upon executing `run.py`, the results will be saved in a file called ```<model>_<prompt>.jsonl```. This file can be found in the ```outputs``` folder. 

Each instance in the jsonl will have the following meta-data associated with them:

<br>

```
{
  "Row Number": Row index of the item,
  "Calculator Name": Name of calculation task,
  "Calculator ID": ID of the calculator,
  "Category": type of calculation (risk, severity, diagnosis for rule-based calculators and lab, risk, physical, date, dosage for equation-based calculators),
  "Note ID": ID of the note taken directly from MedCalc-Bench,
  "Patient Note": Paragraph which is the patient note taken directly from MedCalc-Bench,
  "Question": Question asking for a specific medical value to be computed,
  "LLM Answer": Final Answer Value from LLM, 
  "LLM Explanation": Step-by-Step explanation by LLM,
  "Ground Truth Answer": Ground truth answer value,
  "Ground Truth Explanation": Step-by-step ground truth explanation,
  "Result": "Correct" or "Incorrect"
}
```

Additionally, we provide the mean accuracy and standard deviation percentage for each sub-category in a json titled ```results_<model>_<prompt_style>.json```. The cumulative accuracy and standard deviation among all 1,100 instances can be found under "overall" key of the JSON. This file can be found in the ```results``` folder. 

## Reproducing Code Interpreter Results

In addition to the results for Table 2 in the original MedCalc-Bench paper, we also prompted LLMs to write code to perform arithmetic instead of having the LLM do this itself. The results for this can be found in Appendix D. Due to limited compute, we only ran the results for GPT-3.5 and GPT-4. To examine the prompts and run under this setting, please examine the ```generate_code_prompt.py``` file in the ```evaluation``` folder. 

To run this code, simply `cd` into the ```evaluations``` folder and run the following: ```python generate_code_prompt.py --gpt <gpt_model>```. The options for ```<gpt_model>``` are either `4` for running GPT-4 or `35` to run GPT-3.5-turbo-16k. The results will then get saved in a jsonl file named: ```code_exec_{model_name}.jsonl``` in the  ```outputs``` folder. Note that in this case, ```model_name``` will be ```gpt_4``` if you chose to run using GPT-4. Otherwise, ```model_name``` will be ```gpt_35_16k``` if you selected to run with GPT-3.5-turbo. 

The metadata for each instance in the jsonl file for the code interprepter results is the same instance info provided in the section above. The only difference is that we store the LLM chat history between the user and the assistant and have a "LLM Chat History" key instead of the "LLM Explanation" key. Additionally, the sub-category and overall accuracy are stored in a JSON file named 
```results_<model_name>_code_augmented.json```. This JSON is located in the ```results``` folder. 


## Maintenance and Responsibility 

For any changes to this dataset, (i.e. adding new notes, calculators, modifying existing ones), we will update the README instructions, test_set.csv, and train_set.csv. We will still keep older versions of these datasets as separate branches and update the versions on Github for new releases. We will also update train and test sets for HuggingFace as well. 

## License 

MedCalc-Bench-Verified is released under the CC-BY-SA 4.0 license. 


