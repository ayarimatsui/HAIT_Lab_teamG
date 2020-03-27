# 何の料理かを判定し、カロリーを返す
import keras
from keras.models import load_model
from keras.preprocessing.image import load_img
import numpy as np

class Judge():

    def __init__(self, img_path):
        self.model = keras.models.load_model('VGG16/food_recognition_9.h5')   # 使うモデルによってここも変える
        self.img_path = img_path
        self.food = ['カレーライス', '牛丼', 'ラーメン', '白飯', '味噌汁', '肉じゃが', '焼き魚', '卵焼き', 'ハンバーグ']   # 判別する料理の種類、数によってここを変える
        self.calories = [750, 656, 540, 252, 56, 170, 203, 145, 494]   # 判別する料理の種類、数によってここを変える

    # 学習したモデルに基づいて何の料理なのかを判定
    def judge(self):
        img = keras.preprocessing.image.load_img(self.img_path, target_size=(224, 224))
        x = keras.preprocessing.image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = x / 255.0

        pred = self.model.predict(x)[0]

        category = np.argmax(pred)

        return category

    # 料理名を返す
    def get_food(self):
        cat = self.judge()
        return self.food[cat]

    # カロリーを返す
    def get_calories(self):
        cat = self.judge()
        return self.calories[cat]


# テスト用
'''
if __name__ == '__main__':
    img_path = 'test_images/ramen_test.jpg'
    judge = Judge(img_path)
    result_food = judge.get_food()
    result_calories = judge.get_calories()
    print('この食べ物は、' + result_food)
    print('カロリーは、' + str(result_calories) + 'kcal')
'''
