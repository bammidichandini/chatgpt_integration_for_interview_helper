"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""
import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get("OPEN_AI_API_KEY"))


# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
# Folder containing the .txt files
folder_path = "/Users/chandinibammidi/Desktop/HackathonReqDocuments"

# Iterate over each file in the directory
for filename in os.listdir(folder_path):
    # Check if the file is a .txt file
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        
        # Read the content of the .txt file
        with open(file_path, 'r') as file:
            content = file.read()
            # Concatenate the content with the specified phrase
            prompt = """
            Generate Flash cards content for the data provided in like Question and multiple choice Answers of 4 format. Each question should be the important ones which can be asked in interviews.
                    """
            # - Give real time examples.
            # - To read and understand the flash card, it should not take more than 30 secs to read and understand one flash card.
            transcript = content
            # "Generate Flash cards content for the data provided in like Question and Answer kind of format. Give me the description for each flash card in one sentence."
            response = model.generate_content(contents = [prompt ,  transcript])
            # print(concatenated_content)
            print(response.text)