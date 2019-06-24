# Deep Home Security

![my_id_with_me.png](https://user-images.githubusercontent.com/7239579/59995464-2912cb80-9692-11e9-98cf-127f936a259a.png)
*As you can see, face_recognition even recognizes me wearing a hat and me in the Korean ID card!*

## What is this system for?
This system puts face recognition and IP camera together, thus enabling the surveilence of your place.
Personally, I've wondered what happens in my room when I go out, and that was the direct motivation of this project.

## Installation
First, you need Python 3 to run this system. I strongly recommend you to make a virtual environment for this system.
To install the dependencies, just run
`$ pip install -r requirements.txt`

For now, there are a number of hard coded values in codes. To run the system, you should;
* In `watch.py` and `take_pics.py`, fix `vsrc` value. Details are explained in **Ip Camera** section.
* In `watch.py`, fix `encodings/seungpyo.encodings` to the path where you store your face encodings. It is highly recommended to store the encodings in  `encodings/` directory.

## IP Camera
I used dahua's IP camera, and its model name is `DH-SD29204T-GN`.
Although dahua provides a number of cool features like PTZ control or face detection through its web-based controller, 
I just read frames from the camera using OpenCV's VideoCapture().
If you want to reproduce my results using your own IP camera, you should be careful about the issues below:
* You should fix the `vsrc`, the video source URI by putting **your** ID and password.
* If you are just using a webcam on your laptop or a USB webcam, just set `vsrc` to `0`. 
* I put camera upside down to put it on my table and used `cv2.flip()`. If you installed it upright, you should remove the `cv2.flip()`.
* Dahua IP Camera has a default IP address of `192.168.1.108`. Beware of subnet mask settings so that your PC can access IP camera.


## Face Recognition
I used Python's `face_recognition` library. 
This library provides face recognition, encoding, comparision, and so on.

## `take_pics.py`
By running 

`$ python take_pics.py`

you can register your face to the system.

Although the system compares every photos you registered, the latency doesn't change even though you increase the number of photos.
It seems like face_recognition library performs batch operation.

## `watch.py`

This is the main program that actually *watches* your place. For now, there are a number of hardcoded values in this code, so you should fix some of them.
* granted_encodings - You should modify the encoding file path.

## To do
Since I wrote the first version of this one in a rush, there are too many hard-coded values. I am going to gather them to a single `config.py` file so that user can manipulate them easily.
After this process, I can write more detailed install guide here.

Currently, only a single person's face can be registered as "Granted". I should make a generic version of this code so that users can register multiple faces (e.g. family members, friends)
