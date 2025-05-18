import os
from Pipeline_Implementation.Image_Processing.preProcessing import (
    videoToFrames,
    frameDownscaler,
)
from Pipeline_Implementation.Dehazing_Models.main import main, Arguments
from Pipeline_Implementation.Image_Processing.postProcessing import (
    imageSharpner,
    create_video_from_frames,
)
from Pipeline_Implementation.Detection_Models.videoObjectDetection import (
    processingVideo,
)


def pipeLinemain(videoPath, progressCallback=None):

    if progressCallback:
        progressCallback(10, "Converting video to frames")

    # Converting Video Into Frames
    frames = videoToFrames(videoPath)

    if progressCallback:
        progressCallback(30, "Downscaling frames")


    # Downscaling the frames to get better performance
    frames = frameDownscaler(
        frames,
        os.path.join(
            os.path.dirname(__file__),
            "Dehazing_Models",
            "reside-outdoor",
            "test",
            "hazy",
        ),
    )

    # This is the dehazing function
    if progressCallback:
        progressCallback(75, "Dehazing frames")

    args = Arguments()
    main(args)

    if progressCallback:
        progressCallback(85, "Sharpening frames")

    # Sharpening the dehazed frames and storing them in the sharpenedImage folder
    imageSharpner(
        os.path.join(
            os.path.dirname(__file__), "Dehazing_Models", "results", "FSNet", "test"
        ),
        os.path.join(os.path.dirname(__file__), "Dehazing_Models", "sharpenedImage"),
    )

    if progressCallback:
        progressCallback(90, "Creating video from frames")

    # Creating a video from the sharpened frames
    create_video_from_frames(
        os.path.join(os.path.dirname(__file__), "Dehazing_Models", "sharpenedImage"),
        os.path.join(
            os.path.dirname(__file__), "Input_Output_Videos", "outputVideo.mp4"
        ),
    )

    if progressCallback:
        progressCallback(100, "Processing video with YOLO")

    # Applying Object Detection To The Dehazed Video.
    processingVideo(
        os.path.join(
            os.path.dirname(__file__), "Input_Output_Videos", "outputVideo.mp4"
        ),
        os.path.join(
            os.path.dirname(__file__), "Input_Output_Videos", "outputVideoAnnotated.mp4"
        ),
    )

    # Returning the path of the output video.
    return os.path.join(
        os.path.dirname(__file__), "Input_Output_Videos", "outputVideoAnnotated.mp4"
    )


if __name__ == "__main__":
    pipeLinemain()
