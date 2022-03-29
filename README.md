# Welcome to MediaControl!

Hi! With **MediaControl** you can use hand gestures to control videos and music that are playing on your computer.
- Control the volume;
- Pause and play the videos;
- Next media;
- Previous media.

<img src="https://i.imgur.com/ZLBRTPf.png" width="10%"></img> <img src="https://i.imgur.com/1OIod8o.png" width="10%"></img> <img src="https://i.imgur.com/6TpzAhc.png" width="10%"></img> <img src="https://i.imgur.com/4ZRItTk.png" width="10%"></img>

### Contributors

- [Mateus da Cruz da Silva](https://github.com/MateusOFCZ)

# Installation and Configuration

### PyCharm
Download [**PyCharm**](https://www.jetbrains.com/pt-br/pycharm) and open the project.

### Packages
Install the packages being imported at the beginning of the code, other packages will be automatically installed, but the following package needs to be manually installed by the project settings:
- HandDetector

### Fix Package Error
If the following error occurs when compiling the application and executing the pause and/or play gestures:

```sh
Traceback (most recent call last):
  File "...\PycharmProjects\MediaControl\MediaControl.py", line 77, in <module>
    length, info, img = hand.findDistance(lmList[8], lmList[12], img)
  File "...\PycharmProjects\MediaControl\venv\lib\site-packages\cvzone\HandTrackingModule.py", line 143, in findDistance
    x1, y1 = p1
ValueError: too many values to unpack (expected 2)
[ WARN:0@2.641] global D:\a\opencv-python\opencv-python\opencv\modules\videoio\src\cap_msmf.cpp (539) `anonymous-namespace'::SourceReaderCB::~SourceReaderCB terminating async callback
```

Click on the file that appears in the error, that is, on this line:
```sh
...\PycharmProjects\MediaControl\venv\lib\site-packages\cvzone\HandTrackingModule.py
```

You will find on lines 143 and 144, respectively, the following code:
```py
x1, y1 = p1  
x2, y2 = p2
```

Replace to:
```py
x1, y1, z1 = p1  
x2, y2, z2 = p2
```
