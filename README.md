## Using YOLOV5 Object Detection for a Custom Dataset

1. Change DATA_PATH in yolov5/preprocess_data.py to be the folder of training data.

2. OUTPUT PATH  should be a directory with tree structure as- 
```
         dir/images/train
         dir/labels/train
         dir/images/validation
         dir/labels/validation
```
3. Run to populate data in train and validation folders
```
cd yolov5
python preprocess_data.py
```
4. Change wheat.yaml config accordingly

```
train : 'dir/images/train'
val :   'dir/images/validation'
nc : <no of classes>
names: [<names of classes>]
```
5. Train the model
```
python train.py --img 1025 --batch 8 --epochs 100 --data wheat.yaml--cfg models/yolov5s.yaml --name wmdl
```
6. Test/Inference
<p>Best weights (.pt) file is in yolov5/runs.</p>
```
python detect.py <dir with images/ or a single image> --weights <model.pt file>
```
Credits - [Ultralytics](https://github.com/ultralytics/yolov5) , Abhishek Thakur
