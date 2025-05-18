import cv2
import os
import numpy as np

def extract_frames(video_path, output_folder="frames"):
    """
    Extracts frames from a video and saves them as images.
    
    :param video_path: Path to the input video.
    :param output_folder: Folder to store extracted frames.
    """
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(output_folder, f"frame_{frame_count:04d}.png")
        cv2.imwrite(frame_path, frame)
        frame_count += 1

    cap.release()
    return output_folder, frame_count


def apply_synthetic_haze(image, haze_intensity=0.3):
    """
    Apply synthetic haze to an image.
    
    :param image: Input image (NumPy array).
    :param haze_intensity: Haze strength (0 to 1), where 1 is fully hazy.
    :return: Hazy image.
    """
    # Normalize image
    image = image.astype(np.float32) / 255.0

    # Generate a white haze layer
    haze_layer = np.ones_like(image) * 1.0  # White layer

    # Blend the image with the haze
    hazy_image = (1 - haze_intensity) * image + haze_intensity * haze_layer

    # Convert back to 8-bit format
    hazy_image = (hazy_image * 255).astype(np.uint8)

    return hazy_image


def process_frames(input_folder, output_folder, haze_intensity=0.3):
    """
    Apply synthetic haze to all frames in a folder.
    
    :param input_folder: Folder containing extracted frames.
    :param output_folder: Folder to save hazy frames.
    :param haze_intensity: Strength of haze effect.
    """
    os.makedirs(output_folder, exist_ok=True)
    frame_files = sorted(os.listdir(input_folder))

    for frame_file in frame_files:
        frame_path = os.path.join(input_folder, frame_file)
        image = cv2.imread(frame_path)
        
        if image is None:
            continue
        
        hazy_image = apply_synthetic_haze(image, haze_intensity)
        hazy_frame_path = os.path.join(output_folder, frame_file)
        cv2.imwrite(hazy_frame_path, hazy_image)


def create_video_from_frames(frame_folder, output_video, fps=20):
    """
    Combines frames into a video.
    
    :param frame_folder: Folder containing processed frames.
    :param output_video: Path to save the final video.
    :param fps: Frames per second.
    """
    frame_files = sorted(os.listdir(frame_folder))
    first_frame = cv2.imread(os.path.join(frame_folder, frame_files[0]))
    height, width, _ = first_frame.shape

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    for frame_file in frame_files:
        frame = cv2.imread(os.path.join(frame_folder, frame_file))
        video_writer.write(frame)

    video_writer.release()


def process_video(video_path, output_video, haze_intensity=0.3, fps=30):
    """
    Processes a video: extracts frames, applies haze, and reconstructs video.
    
    :param video_path: Path to input video.
    :param output_video: Path to output video.
    :param haze_intensity: Strength of haze effect.
    :param fps: Frames per second.
    """
    frame_folder, frame_count = extract_frames(video_path)
    process_frames(frame_folder, "hazy_frames", haze_intensity)
    create_video_from_frames("hazy_frames", output_video, fps)


# Run the function on your video
process_video("SampleVideo.mp4", "hazy_video.mp4", haze_intensity=0.3, fps=30)
