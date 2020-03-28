import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
#from judge import *
from judge_yolo import *
from save_img import *

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])  # gifではなくjpegに変更

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_name = 'temp.jpg'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], save_name))
            return redirect(url_for('result'))  # resultのページに遷移
    return render_template('./index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/result', methods=['GET', 'POST'])
def result():
    save_img = SaveImg()
    save_img.save_uploads()
    filepath = 'darknet/test.jpg'
    '''
    judge = Judge(filepath)
    result_food = judge.get_food()
    result_calories = str(judge.get_calories()) + 'kcal'

    # render_template('./result.html')
    return render_template('./result.html', title='予想カロリー', predict_food=result_food, predict_calories=result_calories)'''
    judge_yolo = JudgeYOLO(filepath)
    judge_yolo.run_detect()
    food_list = judge_yolo.get_food()
    total_calories, calories_list = judge_yolo.get_calories()
    nutrients_list = judge_yolo.get_nutrients()
    num = len(food_list)
    result_list = []
    for i in range(num):
        result_list.append([i, food_list[i], calories_list[i], nutrients_list[i]])
    save_img.save_results()
    img_path = 'static/images/result.jpg'
    return render_template('./result.html', title='予想カロリー', result_list=result_list, total_calories=total_calories, img_path=img_path)

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
