import shutil
import os

class SaveImg():
    def __init__(self):
        self.uploaded_file = 'uploads/temp.jpg'
        self.save_upload_file = 'darknet/test.jpg'
        self.judged_file = 'darknet/predictions.jpg'
        self.result_file = 'static/images/result.jpg'

    def save_uploads(self):
        shutil.copy(self.uploaded_file, self.save_upload_file)

    def save_results(self):
        shutil.copy(self.judged_file, self.result_file)
