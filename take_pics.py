import os
import sys
import cv2
import pickle
import face_recognition
from time import sleep

vsrc = 'rtsp://admin:spspsp01!!:@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0'
vcap = cv2.VideoCapture(vsrc)

downsample_scale = 0.5
assert 0. < downsample_scale < 1.

sampler = 0
sampling_cycle = 75
locs = []

ret, frame = vcap.read()
print (frame.shape)

person_name = input('What is your name? ')
img_dir = str(os.path.join(os.getcwd(), 'img'))
img_dir = str(os.path.join(img_dir, person_name))
pkl_dir = str(os.path.join(os.getcwd(), 'encodings'))

if not os.path.exists(img_dir):
    os.mkdir(img_dir)
if not os.path.exists(pkl_dir):
    os.mkdir(pkl_dir)

print ('Saving photos at {}'.format(img_dir))

frame_num = 0
max_frame_num = 20

small_frames = []
face_encodings_tosave = []
while frame_num < max_frame_num:
    
    ret, frame = vcap.read()
    if frame is None:
        print('Error: Reading a frame from camera failed.')
        sys.exit()
            
    sampler = (sampler + 1) % sampling_cycle
    if sampler != 1:
        continue

    frame = cv2.flip(frame, 0)
    frame_small = cv2.resize(frame, None, fx=downsample_scale, fy=downsample_scale)
    # Run detection model
    locs = face_recognition.face_locations(frame_small)
    if len(locs) != 1:
        print ('Failed to detect a face in the photo; trying again...')
        continue
    small_frames.append(frame_small)
    
    frame_num += 1
    print('Took photo #{}'.format(frame_num))

for sf in small_frames:
    new_face_encodings = face_recognition.face_encodings(sf)
    if len(new_face_encodings) != 1:
        print('photo #{} has bad encodings, discarded.')
    face_encodings_tosave.append(new_face_encodings[0])

encodings_path = os.path.join(pkl_dir, person_name+'.encodings')
print ('Writing pickled encodings at {}'.format(encodings_path))
with open(encodings_path, 'wb') as f:
    pickle.dump(face_encodings_tosave, f)

