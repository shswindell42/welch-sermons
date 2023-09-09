import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes, ComputerVisionOcrErrorException
from msrest.authentication import CognitiveServicesCredentials

from array import array
from PIL import Image
import sys
import time

# Auth
subscription_key = os.environ["VISION_KEY"]
endpoint = os.environ["VISION_ENDPOINT"]

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


# Read files 
img_path = "/home/spencer/Documents/welch-bible-lessons"
all_files = os.listdir(img_path)
img_files = [f for f in all_files if f.endswith(".png")]
processed_files = [f.replace(".txt", ".png") for f in all_files if f.endswith(".txt")]

files_to_process = list(set(img_files) - set(processed_files))

print(f"Found {len(files_to_process)} to process")

for file in files_to_process:
    file = os.path.join(img_path, file)
    print(file)
    text_file_name = file.replace(".png", ".txt")

    with open(file, 'rb') as img_data:
        response = computervision_client.read_in_stream(image=img_data, raw=True, )
    operation_id = response.headers["Operation-Location"].split("/")[-1]

    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    if read_result.status == OperationStatusCodes.succeeded:
        with open(text_file_name, 'w') as text_file:
            for text_result in read_result.analyze_result.read_results:
                for line in text_result.lines:
                    text_file.write(line.text)
                    text_file.write("\n")
