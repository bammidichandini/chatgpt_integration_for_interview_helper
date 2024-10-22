import os
import os
from openai import OpenAI
import json
from flask import Flask, render_template

app = Flask(__name__)

resultant_list = []
# # Folder containing the .txt files
folder_path = "/Users/chandinibammidi/Desktop/HackathonReqDocuments/Triggerpoints/"
# # Iterate over each file in the directory
resultant_list = []
# Iterate over each file in the directory
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)

        # Read the content of the .txt file
        with open(file_path, 'r') as file:
            content = file.read()
            # print(content)
            resultant_list.append(content)

qa_data = [json.loads(data_string) for data_string in resultant_list]
print(qa_data)
@app.route('/')
def byteindex():
    return render_template('byteindex.html', qa_data=qa_data)
if __name__ == '__main__':
    app.run(port = 8084, debug=True)