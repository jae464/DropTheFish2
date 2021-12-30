from flask import Flask, render_template, request, Response, redirect, url_for
from camera import *
from detect import *
from detect2 import *
from keras.models import load_model
from keras.preprocessing import image
from detect2 import *
app = Flask(__name__)

class_list = [["bangeo"],["jeon"],["yeolgi"]]
# model = load_model('model.h5')

# model.make_predict_function()

# dic = {0: 'Cat', 1: 'Dog'}
# def predict_label(img_path):
#   print(img_path)
#   i = image.load_img(img_path, target_size=(100,100))
#   i = image.img_to_array(i) / 255.0
#   i = i.reshape(1, 100, 100, 3)
#   p = model.predict_classes(i)
#   return dic[p[0]]

@app.route('/')
def index():
  return render_template('index.html')
  
@app.route('/fish')
def fish():
  return render_template('fish.html')
def gen(camera, type):
  if type == 'video':
    print('녹화를 시작합니다.')
    while True:
      frame = camera.get_frame()
      if frame == 'done':
        break
      yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
      
  elif type == 'capture':
    print('capture를 시작합니다.')
    frame = camera.get_frame()
    yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/sushi')
def sushi():
  return render_template('sushi.html')
def gen(camera, type):
  if type == 'video':
    print('녹화를 시작합니다.')
    while True:
      frame = camera.get_frame()
      if frame == 'done':
        break
      yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
      
  elif type == 'capture':
    print('capture를 시작합니다.')
    frame = camera.get_frame()
    yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  
@app.route('/video')
def video():
  return Response(gen(Video(type='video'), 'video'),
  mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def capture():
  return get_now_frame()

@app.route('/result')
def result():
  # img_path = './static/images/' + get_now_jpg()
  # print(img_path)
  # p = predict_label(img_path)
  # print('분류 결과는 ' + p + '입니다.')
  result = detectAllModels()
  print(len(result))
  for i in range(len(result)):
    ret, jpg = cv2.imencode('.jpg', i)
    cv2.imwrite('./static/images/' + class_list[i][0] + '_result_pic' + '.jpg', result[i])
  # ret, jpg = cv2.imencode('.jpg', result)
  # cv2.imwrite('./static/images/' + 'result_pic' + '.jpg', result)
  # return render_template('result.html', prediction = jpg)
  temp = get_final_result()
  if len(temp) == 0:
    final_result = ""
  else:
    final_result = get_final_result()[0]
  print('final_result : ', final_result)
  final_result_path = final_result[0] + '_result_pic' + '.jpg'
  clear_final_result()
  return render_template('result.html', path = final_result_path)

if __name__ == '__main__':
  app.run(debug=True)