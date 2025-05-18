from Pipeline_Implementation.Dehazing_Models.main import main, Arguments
from Pipeline_Implementation.Image_Processing.liveFrameProcessing import frameDownscaler, imageSharpner
import os


def framePipeline(frame, frame_id, userResolution, userInterpolation):
    current_file_dir = os.path.dirname(__file__)
    frameDownscaler(
        frame,
        frame_id,
        userResolution,
        userInterpolation,
        os.path.join(
            current_file_dir, "Dehazing_Models", "reside-outdoor", "test", "hazy"
        ),
    )
    # This is the dehazing function which knows where to dehaze from
    args = Arguments()
    main(args)
    
    newFrame = imageSharpner(
        os.path.join(current_file_dir, "Dehazing_Models", "results"),
    )
    return newFrame
