import supervision as sv
from PIL import Image
from rfdetr import RFDETRBase

classNames = ["Null", "Bystander", "Gun", "Man Holding Gun", "Robbery Using Gun"]

model = RFDETRBase(
    pretrain_weights="./Pipeline_Implementation/Detection_Models/RF_DETR_Models/checkpoint_best_ema.pth"
)

image = Image.open("./Extras/test/Screenshot 2025-04-22 000257.png")
image = image.convert("RGB")
detections = model.predict(image, threshold=0.4)

labels = [
    f"{classNames[class_id]} {confidence:.2f}"
    for class_id, confidence in zip(detections.class_id, detections.confidence)
]

annotated_image = image.copy()
annotated_image = sv.BoxAnnotator().annotate(annotated_image, detections)
annotated_image = sv.LabelAnnotator().annotate(annotated_image, detections, labels)

sv.plot_image(annotated_image)
