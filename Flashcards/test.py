import os
import os
from openai import OpenAI
import json
from flask import Flask, render_template

app = Flask(__name__)

# # Folder containing the .txt files
ouput_path = "/Users/chandinibammidi/Desktop/HackathonReqDocuments/Output/"
# # Iterate over each file in the directory
for filename in os.listdir(ouput_path):
    if filename.endswith('.json'):
        file_path = os.path.join(ouput_path, filename)

        # Read the content of the .txt file
        with open(file_path, 'r') as file:
            content = file.read()
            # print(file_path)
            segregated_text = str(content)
            # segregated_text = segregated_text.replace("```json", "").replace("```", "")
            start_index = segregated_text.find('[')
            end_index = segregated_text.rfind(']') + 1
            segregated_text = json_part = segregated_text[start_index:end_index]
            try:    
                data_dict = json.loads(segregated_text)
                file_name, file_extension = os.path.splitext(filename)
                output_file_path = os.path.join(ouput_path, f"{file_name}.json")
                with open(output_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(data_dict, json_file, ensure_ascii=False, indent=4)
                print(f"Data saved to {output_file_path}")
                # json_file.write(data_dict)
            except json.JSONDecodeError:
                print("Invalid JSON response.")
                print(segregated_text)


@app.route('/')
def index():
    return render_template('index.html', qa_data=data_dict)
if __name__ == '__main__':
    app.run(port = 8082, debug=True)






