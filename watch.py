import os
import sys
import cv2
import time
import datetime
import pickle
import face_recognition

vsrc = 'rtsp://admin:spspsp01!!:@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0'
vcap = cv2.VideoCapture(vsrc)

downsample_scale = 0.5
assert 0. < downsample_scale < 1.

sampler = 0
sampling_cycle = 12
locs = []

ret, frame = vcap.read()
print (frame.shape)

granted_encodings = []
with open('encodings/seungpyo.encodings', 'rb') as f:
    granted_encodings = pickle.load(f)

logs_dir = 'logs'
'''
granted_dir = 'img/seungpyo'
print ('Generating encodings from {}...'.format(granted_dir))
for granted_filename in os.listdir(granted_dir):
    granted_path = os.path.join(granted_dir, granted_filename)
    granted_pic = face_recognition.load_image_file(granted_path)
    h, w, _ = granted_pic.shape
    if granted_pic is None:
        print('load_image_file failed at {}'.foramt(granted_path))
    cv2.imshow(granted_path, granted_pic)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        sys.exit()
    granted_encodings.append(
        face_recognition.face_encodings(granted_pic, (0, w, h, 0))[0])
'''
print ('{} encodings were succesfully generated.'.format(len(granted_encodings)))

color_granted = (0, 255, 0) # Green
text_granted = 'Granted'
color_unknown = (0, 0, 255) # Red
text_unknown = 'Unknown'
match_threshold = 0.9

prev_count_unknown = 0

# The number of frames where unknowns(red boxes) were detected.
red_duration = 0
red_alert = 20

while True:
    ret, frame = vcap.read()
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.flip(frame, 0)
    frame_small = cv2.resize(frame, None, fx=downsample_scale, fy=downsample_scale)
    show_frame = frame

    sampler = (sampler + 1)%sampling_cycle
    if sampler == 0:
      # Run detection model
      t0 = time.time()
      locs = face_recognition.face_locations(frame_small)
      t1 = time.time()
      # new_face_encodings = face_recognition.face_encodings(frame_small)
      # Use recognized locations to avoid redundant works.
      new_face_encodings = face_recognition.face_encodings(frame_small, locs)
      t2 = time.time()
      # print ('face_locations: {}'.format(t1-t0))
      # print ('face_encodings: {}'.format(t2-t1))
    
    count_granted = 0
    count_unknown = 0
   
    for i, loc in enumerate(locs):
        # For each face
        t, r, b, l = loc
        face_blob = frame_small[t:b, l:r]

        results = face_recognition.compare_faces(
            granted_encodings, new_face_encodings[i])
        matched = [res for res in results if res]
        match_confidence = float(len(matched)) / len(results) 
        granted = match_confidence > match_threshold
        # print ('{}% match'.format(match_confidence*100))           
        if granted:
            rect_color = color_granted
            rect_text = '{} ({}%)'.format(text_granted, match_confidence*100)
            count_granted += 1
        else:
            rect_color = color_unknown
            rect_text = '{} ({}%)'.format(text_unknown, match_confidence*100)
            count_unknown += 1
        
        show_frame = cv2.rectangle(show_frame, 
          (int(l/downsample_scale), int(t/downsample_scale)), 
          (int(r/downsample_scale), int(b/downsample_scale)), 
          rect_color, 2)
        show_frame = cv2.putText(show_frame, 
          rect_text,
          (int(l/downsample_scale), int(t/downsample_scale)), 
          cv2.FONT_HERSHEY_SIMPLEX, 2, rect_color)

    if count_unknown == 0:
        red_duration = 0
    else:
        red_duration += 1

    if red_duration == red_alert:
        print ('Intruder detected!')
        now_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = 'alert_detections_{}.jpg'.format(now_str)
        cv2.imwrite(os.path.join(logs_dir, filename), show_frame)
        filename = 'alert_original_{}.jpg'.format(now_str)
        cv2.imwrite(os.path.join(logs_dir, filename), frame)
        # os.system('mpg123 alert.mp3')
        red_duration = 0

    cv2.imshow('VIDEO', frame)
    cv2.waitKey(10)
