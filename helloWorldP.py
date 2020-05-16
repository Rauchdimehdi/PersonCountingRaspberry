import json
import numpy as np 
import cv2
import re
import greengrasssdk
import time
import io
import picamera
from PIL import Image
from tflite_runtime.interpreter import Interpreter
from annotation import Annotator
import os




CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480


def load_labels(path):
  """Loads the labels file. Supports files with or without index numbers."""
  with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    labels = {}
    for row_number, content in enumerate(lines):
      pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
      if len(pair) == 2 and pair[0].strip().isdigit():
        labels[int(pair[0])] = pair[1].strip()
      else:
        labels[row_number] = pair[0].strip()
  return labels
def set_input_tensor(interpreter, image):
  """Sets the input tensor."""
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image


def get_output_tensor(interpreter, index):
  """Returns the output tensor at the given index."""
  output_details = interpreter.get_output_details()[index]
  tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
  return tensor


def detect_objects(interpreter, image, threshold):
  """Returns a list of detection results, each a dictionary of object info."""
  set_input_tensor(interpreter, image)
  interpreter.invoke()

  # Get all output details
  boxes = get_output_tensor(interpreter, 0)
  classes = get_output_tensor(interpreter, 1)
  scores = get_output_tensor(interpreter, 2)
  count = int(get_output_tensor(interpreter, 3))

  results = []
  for i in range(count):
    if scores[i] >= threshold:
      result = {
          'bounding_box': boxes[i],
          'class_id': classes[i],
          'score': scores[i]
      }
      results.append(result)
  return results


def annotate_objects(annotator, results, labels):
  """Draws the bounding box and label for each object in the results."""
  for obj in results:
    # Convert the bounding box figures from relative coordinates
    # to absolute coordinates based on the original resolution
    
    if labels[obj['class_id']] == 'person':
      
      ymin, xmin, ymax, xmax = obj['bounding_box']
      xmin = int(xmin * CAMERA_WIDTH)
      xmax = int(xmax * CAMERA_WIDTH)
      ymin = int(ymin * CAMERA_HEIGHT)
      ymax = int(ymax * CAMERA_HEIGHT)



      # Overlay the box, label, and score on the camera preview
      annotator.bounding_box([xmin, ymin, xmax, ymax])
      annotator.text([xmin, ymin],
                     '%s\n%.2f' % (labels[obj['class_id']], obj['score']))


# Initialize example model
model_resource_path = os.environ.get('MODEL_PATH', '/model')
# Read model & label file
model = os.path.join(model_resource_path, 'detect.tflite')
label = os.path.join(model_resource_path, 'coco_labels.txt')

#read labels & model & treshold
interpreter = Interpreter(model)
labels = load_labels(label)
threshold = 0.5
 

def greengrass_app():
    try:
        client = greengrasssdk.client('iot-data')
        iot_topic = 'raspberry/out'
        client.publish(topic=iot_topic, payload='Loading object detection model')
        
        #test = labels[0]
        
        
        #client.publish(topic=iot_topic, payload='first item :'+ test +'!!!')
        
        
        interpreter.allocate_tensors()
        _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']
        # Do inference until the lambda is killed.
        client.publish(topic=iot_topic, payload='object detection model loaded')
        while True:
          with picamera.PiCamera(resolution=(CAMERA_WIDTH, CAMERA_HEIGHT), framerate=30) as camera:
            camera.start_preview()
            try:
              stream = io.BytesIO()
              annotator = Annotator(camera)
              for _ in camera.capture_continuous(
                  stream, format='jpeg', use_video_port=True):
                stream.seek(0)
                
                image = Image.open(stream).convert('RGB').resize(
                    (input_width, input_height), Image.ANTIALIAS)
                start_time = time.monotonic()
                results = detect_objects(interpreter, image, threshold)
                #print (results, type(results))
                elapsed_ms = (time.monotonic() - start_time) * 1000
        
                annotator.clear()
                annotate_objects(annotator, results, labels)
                annotator.text([5, 0], '%.1fms' % (elapsed_ms))
                annotator.update()
        
                stream.seek(0)
                stream.truncate()
                nbr = len(results)
                #print(f" Prediction result : {nbr}")
                p = str(nbr)
                client.publish(topic=iot_topic, payload='Nombre de personne détecter :'+ p +'!!!')
            except Exception as e:
              client.publish(topic=iot_topic, payload='Error inside Pica ')
    except Exception as e:
      client.publish(topic=iot_topic, payload='Error inside lambda ')

    # Asynchronously schedule this function to be run again in 5 seconds
    #Timer(5, greengrass_app).start()


# Start executing the function above
greengrass_app()



def lambda_handler(event, context):
    return 
