# 何の料理かを判定し、カロリーを返す
#import subprocess
import os

class JudgeYOLO():

    def __init__(self, img_path):
        self.img_path = img_path
        self.result_img_path = 'darknet/predictions.*'
        self.result_txt_path = 'darknet/out.txt'
        self.classnames = ['curry', 'gyudon', 'ramen', 'rice', 'miso soup', 'nikujaga', 'grilled fish', 'rolled omlet', 'hamburg steak']
        self.food = ['カレーライス', '牛丼', 'ラーメン', '白飯', '味噌汁', '肉じゃが', '焼き魚', '卵焼き', 'ハンバーグ']   # 判別する料理の種類、数によってここを変える
        self.calories = [750, 656, 540, 252, 56, 170, 203, 145, 494]   # 判別する料理の種類、数によってここを変える

    # 判定コマンドを実行
    def run_detect(self):
        cur_img_path = os.path.basename(self.img_path)    # アップロードした画像はdarknet直下に置くようにあとでwebを変更
        os.chdir('darknet')
        #cmd = 'chmod +x ./darknet'
        #subprocess.call(cmd.split())
        #subprocess.call(['./darknet', 'detector', 'test', 'cfg/obj.data', 'cfg/yolo-obj.cfg', 'backup/yolo-obj_10000.weights', cur_img_path, '-thresh', '0.1'], shell=True)
        os.system("./darknet detector test cfg/obj.data cfg/yolo-obj.cfg backup/yolo-obj_10000.weights " + cur_img_path + " -thresh 0.1")
        os.chdir('..')

    def get_class_id(self):
        id_list = []
        with open(self.result_txt_path, "r") as file:
            for line in file.read().splitlines():
                idx = self.classnames.index(line)
                id_list.append(idx)
        return id_list

    # 料理名を返す
    def get_food(self):
        idx_list = self.get_class_id()
        food_list = []
        for id in idx_list:
            food_list.append(self.food[id])
        return food_list

    # カロリーを返す
    def get_calories(self):
        idx_list = self.get_class_id()
        calories_list = []
        for id in idx_list:
            calories_list.append(self.calories[id])
        return sum(calories_list), calories_list


# テスト用

if __name__ == '__main__':
    img_path = 'darknet/test12.jpeg'
    judge = JudgeYOLO(img_path)
    judge.run_detect()
    food_list = judge.get_food()
    total_calories, calories_list = judge.get_calories()
    n = len(food_list)
    print('検出された料理とそのカロリー')
    for i in range(n):
        print(food_list[i] + ' : ' + str(calories_list[i]) + 'kcal')
    print('合計カロリーは、' + str(total_calories) + 'kcal')
