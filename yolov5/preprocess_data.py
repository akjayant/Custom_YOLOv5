import os
import ast
import pandas as pd
from sklearn import model_selection
from tqdm import tqdm
import numpy as np
import shutil


DATA_PATH = '/media/ashish-j/B/wheat_detection/global_wheat_detection'
OUTPUT_PATH = '/media/ashish-j/B/wheat_detection/yolo_wheat_data'

def process_data(data,data_split='train'):
	for _,row in tqdm(data.iterrows(),total=len(data)):
		image_name = row['image_id']
		bounding_boxes = row['bboxes']
		yolo_data = []
		for bbox in bounding_boxes:
			x=bbox[0]
			y=bbox[1]
			w=bbox[2]
			h=bbox[3]

			#normalizing data for yolo
			x_center = x + w /2
			y_center = y+h /2
			x_center /= 1024
			y_center /= 1024
			w /= 1024
			h /= 1024

			yolo_data.append([0,x_center,y_center,w,h])
		yolo_data = np.array(yolo_data)
		np.savetxt(
			os.path.join(OUTPUT_PATH,f"labels/{data_split}/{image_name}.txt"),
			yolo_data,
			fmt=["%d","%f","%f","%f","%f"]
			)
			
		shutil.copyfile(
			os.path.join(DATA_PATH,f"train/{image_name}.jpg"),
			os.path.join(OUTPUT_PATH,f"images/{data_split}/{image_name}.jpg")
			
			)






if __name__ == "__main__":
	df = pd.read_csv(os.path.join(DATA_PATH,"train.csv"))
	#-----convert string list to list
	df.bbox = df.bbox.apply(ast.literal_eval)
	df = df.groupby("image_id")['bbox'].apply(list).reset_index(name='bboxes')
	df_train, df_valid = model_selection.train_test_split(
		df,
		test_size=0.1,
		random_state=56,
		shuffle=True
		)
	df_train = df_train.reset_index(drop=True)
	df_valid = df_valid.reset_index(drop=True)

	process_data(df_train,data_split='train')

	process_data(df_valid,data_split='validation')