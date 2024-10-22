import os
import os
from openai import OpenAI
import json
from PIL import Image
import pytesseract

# Configure the OpenAI API key
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPEN_AI_API_KEY")
)
data = []
# Model and settings
model_name = "gpt-4-1106-preview"  # or other GPT-3.5 models like text-davinci-002
# generation_config = {
#     "temperature": 0.9,
#     "max_tokens": 2048,
#     "top_p": 1,
#     "frequency_penalty": 0,
#     "presence_penalty": 0
# }

# Folder containing the .txt files
folder_path = "/Users/chandinibammidi/Desktop/HackathonReqDocuments"
ouput_path = "/Users/chandinibammidi/Desktop/HackathonReqDocuments/MCQs/"
resultant_list = []

# Function to extract text from images
def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text
# Iterate over each file in the directory
for filename in os.listdir(folder_path):
    if filename.endswith('.md'):
        file_path = os.path.join(folder_path, filename)
        content = ""

        # Read the content of the .txt file
        with open(file_path, 'r') as file:
            content += file.read()

            for line in content.splitlines():
                if line.strip().lower().endswith('.png'):
                    image_path = os.path.join(folder_path, line.strip())
                    if os.path.exists(image_path):
                        image_text = extract_text_from_image(image_path)
                        content += "\n" + image_text
            prompt = """
    You are a student success mentor in a EdTech Company. Your task is to prepare different questions (could be question and answer, multiple choice) for the topics mentioned in the text file which we are providing.
	While preparing the questions follow the steps below :
		1. Don’t add unnecessary topics not mentioned in the text file
		2. Questions language should be in layman terms i.e should be even understood by a non-technical student.
		3. Ensure the answers that you are providing are correct and accurate. Cross check this before providing the response.
		4. Give the answers with proper examples along with definitions i.e try to real life examples so that users can correlate the concepts/topics easily.
		5. Questions and answers should be in a manner that we can use them as a flashcards of the topic so that user can revise entire topic using these flashcards.
        6. Try to give different type of questions like questions and answers type, multiple-choice questions.
        7. If a there is a chance to use coding snippets or images to explain the topic include at neccessry places without increasing complexity
        """
            
            response = client.chat.completions.create(
 
            messages=[{"role": "system", "content": prompt + "Dont give anything else, Just pure json with topic, subtopic, question and answer. Give pure json object"},
 
                  {"role": "user", "content": content}], model="gpt-4-1106-preview")
            # Print the generated response
            segregated_text = str(response.choices[0].message.content)
 
            segregated_text = segregated_text.replace("```json", "").replace("```", "")
 
            # segregated_text = segregated_text.replace("```json", "").replace("```", "")
            # start_index = segregated_text.find('[')
            # end_index = segregated_text.rfind(']') + 1
            # print(start_index,end_index)
            # print(segregated_text)
            # if start_index > 0 and end_index > 0:
            #     segregated_text = segregated_text[start_index:end_index]
            try:
                # data_dict = json.loads(segregated_text)
                data_dict = []
                data_dict.append(segregated_text)
                file_name, file_extension = os.path.splitext(filename)
                output_file_path = os.path.join(ouput_path, f"{file_name}.json")
                with open(output_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(data_dict, json_file, ensure_ascii=False, indent=4)
                print(f"Data saved to {output_file_path}")
                data.append(data_dict)
                # json_file.write(data_dict)
            except json.JSONDecodeError:
                print("Invalid JSON response.")
                
print(data)    

