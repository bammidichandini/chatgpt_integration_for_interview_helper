import os
import os
from openai import OpenAI
import json
from flask import Flask, render_template
from PIL import Image
import pytesseract
import os

app = Flask(__name__)

# Configure the OpenAI API key
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPEN_AI_API_KEY")
)
# # Model and settings
model_name = "gpt-4-1106-preview"  # or other GPT-3.5 models like text-davinci-002
# generation_config = {
#     "temperature": 0.9,
#     "max_tokens": 2048,
#     "top_p": 1,
#     "frequency_penalty": 0,
#     "presence_penalty": 0
# }
resultant_list = []
# # Folder containing the .txt files
folder_path = "/Users/chandinibammidi/Desktop/HackathonReqDocuments/"
ouput_path = "/Users/chandinibammidi/Desktop/HackathonReqDocuments/Triggerpoints/"
# # Iterate over each file in the directory

# Function to extract text from images
def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

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
            You are a student success mentor in a EdTech Company. Your task is to help students retain the topics taught in our course. Generate examples/triggerpoints that will help trigger the student and help him remember the topic. Give me the pure Json"""
            
            response = client.chat.completions.create(
 
            messages=[{"role": "system", "content": prompt + """Don't give anything else. Give me pure json with topic,trigger and explanation"""},
 
                {"role": "user", "content": content}], model="gpt-4-1106-preview")
            segregated_text = str(response.choices[0].message.content)
            # segregated_text = segregated_text.replace("```json", "").replace("```", "")
            start_index = segregated_text.find('[')
            end_index = segregated_text.rfind(']') + 1
            segregated_text = segregated_text[start_index:end_index]
            try:
                print(segregated_text)
                data_dict = json.loads(segregated_text)
                file_name, file_extension = os.path.splitext(filename)
                output_file_path = os.path.join(ouput_path, f"{file_name}.json")
                with open(output_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(data_dict, json_file, ensure_ascii=False, indent=4)
                print(f"Data saved to {output_file_path}")
                resultant_list.append(data_dict)
                # json_file.write(data_dict)
            except json.JSONDecodeError:
                print("Invalid JSON response.",filename)

print(resultant_list)
# @app.route('/')
# def index():
#     return render_template('index.html', qa_data=data_dict)
# if __name__ == '__main__':
#     app.run(port = 8082, debug=True)