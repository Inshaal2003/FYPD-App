import supervision as sv
from rfdetr import RFDETRBase

model = RFDETRBase(
    pretrain_weights="./Pipeline_Implementation/Detection_Models/RF_DETR_Models/checkpoint_best_ema.pth"
)
classNames = ["Null", "Bystander", "Gun", "Man Holding Gun", "Robbery Using Gun"]


# Callback function that takes a video path as an argument
def callback(frame, index, video_path):
    frame_copy = frame[:, :, ::-1].copy()

    detections = model.predict(frame_copy, threshold=0.5)

    # Create labels for the detections
    labels = [
        f"{classNames[class_id]} {confidence:.2f}"
        for class_id, confidence in zip(detections.class_id, detections.confidence)
    ]

    # Annotate frame with boxes and labels
    annotated_frame = frame.copy()
    annotated_frame = sv.BoxAnnotator().annotate(annotated_frame, detections)
    annotated_frame = sv.LabelAnnotator().annotate(annotated_frame, detections, labels)

    return annotated_frame


# Function to process video and pass the path dynamically
def processingVideo(source_path, target_path):
    sv.process_video(
        source_path=source_path,
        target_path=target_path,
        callback=lambda frame, index: callback(
            frame, index, source_path
        ),  # Pass video path to callback
    )