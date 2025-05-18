import cv2
import numpy as np
from PIL import Image
import os

# Open the video file for reading


# This function will be used to load the video and than convert it into frames
def videoToFrames(filename):
    framesList = []
    cam = cv2.VideoCapture(filename)
    frameno = 0
    while(True):
        # Read the next frame from the video
        frameRead, frame = cam.read()
        # frameRead ---> True if the frame is read correctly, False otherwise
        # frame ---> the frame itself

        if frameRead:
            # if video is still left continue creating images
            framesList.append(frame)    
            # print(framesList)
            #   cv2.imwrite(name, frame)
            frameno += 1
        else:
            break
    cam.release()
    return framesList

# print("The number of frames in the list are: ", len(frames))



def frameDownscaler(framesList, outputPath):
    downscaled_frames = []
    for frameNo, frame in enumerate(framesList):
        # Converting the numpy array to image
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        # image.save('frame.png')
        # Specify new size (e.g., 50% of the original dimensions
        new_size = (image.width // 2, image.height // 2)
        # Downscale with high-quality resampling
        downscaled_image = image.resize(new_size, Image.Resampling.LANCZOS)
        # Storing the frames in specific dir : reside-outdoor\test\hazy\frame_1.png
        
        print(f"Output Path: {outputPath}")
        print(f"Saving frame {frameNo} to: {os.path.join(outputPath, f'frame_{frameNo:03d}.png')}")

        downscaled_image.save(os.path.join(outputPath,f"frame_{frameNo:03d}.png"))
        # Convert the downscaled image to numpy array
        # downscaled_image = cv2.cvtColor(np.array(downscaled_image), cv2.COLOR_RGB2BGR)
        # Save the downscaled image in the list
        # downscaled_frames.append(downscaled_image)
    # return downscaled_frames