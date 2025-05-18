from PIL import Image
import os
import cv2
import numpy as np

# def frameDownscaler(frame, frame_id, userResolution, outputPath):
#     # Converting the numpy array to image
#     image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#     # image.save('frame.png')
#     # Specify new size (e.g., 50% of the original dimensions
#     new_size = (int(image.width*userResolution) , int(image.height * userResolution))
#     # Downscale with high-quality resampling
#     downscaled_image = image.resize(new_size, Image.Resampling.LANCZOS)
#     # Storing the frames in specific dir : reside-outdoor\test\hazy\frame_1.png
#     # print(f"Output Path: {outputPath}")
#     # print(f"Saving frame 1 to: {os.path.join(outputPath, f'frame_1.png')}")
#     downscaled_image.save(os.path.join(outputPath, f"frame_{frame_id:04d}.png"))
#     # Convert the downscaled image to numpy array
#     # downscaled_image = cv2.cvtColor(np.array(downscaled_image), cv2.COLOR_RGB2BGR)
#     # Save the downscaled image in the list
#     # downscaled_frames.append(downscaled_image)
#     # return downscaled_frames


def frameDownscaler(frame, frame_id, userResolution, userInterpolation, outputPath):
    new_width = int(frame.shape[1] * userResolution)
    new_height = int(frame.shape[0] * userResolution)
    new_size = (new_width, new_height)
    downscaled_frame = cv2.resize(frame, new_size, interpolation=getattr(cv2, userInterpolation))
    # cv2.imwrite(os.path.join(outputPath, f"frame_{frame_id:04d}.png"), downscaled_frame)
    cv2.imwrite(
        os.path.join(outputPath, f"frame_{frame_id:04d}.jpg"),
        downscaled_frame,
        [int(cv2.IMWRITE_JPEG_QUALITY), 95],
    )


def imageSharpner(inputPath):
    # Load the image
    # Define a sharpening kernel (3x3 matrix)
    sharpening_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    # if not os.path.exists(outputPath):
    #     os.makedirs(outputPath)
    for fileName in os.listdir(inputPath):
        if fileName.endswith(".jpg"):
            image_path = os.path.join(inputPath, fileName)
            image = cv2.imread(image_path)
            # Sharpening the image
            sharpened_image = cv2.filter2D(image, -1, sharpening_kernel)
            # outputdir = os.path.join(outputPath, fileName)
            # cv2.imwrite(outputdir, sharpened_image)
        else:
            break
    return sharpened_image
