import cv2
import numpy as np
import os

def imageSharpner(inputPath, outputPath):
    # Load the image
    # Define a sharpening kernel (3x3 matrix)
    sharpening_kernel = np.array(
        [
            [0, -1, 0],
            [-1,  5,-1],
            [0, -1, 0]
        ]
    )
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    for fileName in os.listdir(inputPath):
        if fileName.endswith(".png"):
            image_path = os.path.join(inputPath, fileName)
            image = cv2.imread(image_path)
            # Sharpening the image
            sharpened_image = cv2.filter2D(image, -1, sharpening_kernel)
            outputdir = os.path.join(outputPath, fileName)
            cv2.imwrite(outputdir, sharpened_image)
        else:
            break



def create_video_from_frames(frames_dir, output_video_path, fps=30):
    # Get list of frame files
    frame_files = []
    for file in os.listdir(frames_dir):
        if file.endswith(".png"):
            frame_files.append(file)
                
    # Read the first frame to get the frame size
    first_frame_path = os.path.join(frames_dir, frame_files[0])
    first_frame = cv2.imread(first_frame_path)
    height, width, layers = first_frame.shape
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    for frame_file in frame_files:
        frame_path = os.path.join(frames_dir, frame_file)
        frame = cv2.imread(frame_path)
        video_writer.write(frame)
    
    video_writer.release()
    print(f"Video created at {output_video_path}")

