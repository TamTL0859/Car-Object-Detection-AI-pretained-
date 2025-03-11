import cv2
import torch
import numpy as np
from torchvision.models.detection import fasterrcnn_resnet50_fpn, FasterRCNN_ResNet50_FPN_Weights
from torchvision.transforms import functional as F

# This class processes the video sent from the web page
class VideoProcessor:
    def __init__(self, uploaded_video):
        self.uploaded_video = uploaded_video
        self.output_video = r'' #INSERT PATH TO OUTPUT VIDEO e.g C:\\Users\\XXXXX\\Documents\\Projects\\Python\\ComputerVisionProject\\ComputerVision\\Backend\Data\\output.mp4
        
        #Checks if it can run on GPU
        self.graphics_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        #print(f"Using device: {self.graphics_device}") check if cuda works

        # Load AI Model på GPU/CPU
        self.model = fasterrcnn_resnet50_fpn(weights="DEFAULT").to(self.graphics_device)
        self.model.eval()

        # Load COCO labels (labels the pretrained model is trained on)
        self.LABEL_MAP = FasterRCNN_ResNet50_FPN_Weights.DEFAULT.meta["categories"]
        self.threshold = 0.8
        
        self.FRAME_RATE_LIMIT = 10 # Limit the amount of seconds the video can be (10 = 10 seconds)
        
         #filter
        self.FILTERED_LABEL_ID = [1,2,3,4,6,8]
        self.FILTERED_LABEL_NAMES = ["person,", "bicycle", "car", "motorcycle", "bus", "truck"] #choose objects to detect

    def process_video(self):
            
        video = cv2.VideoCapture(self.uploaded_video)

        if not video.isOpened():
            print("Error: Couldn't open video.")
            exit()

        #video properties
        frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Frame rate and processing limit
        frame_rate = video.get(cv2.CAP_PROP_FPS)
        frame_limit = frame_rate * self.FRAME_RATE_LIMIT  # Process 10 seconds worth of frames
        #print(frame_rate)

        frame_count = 0

        #output video setup (*'mp4v') doesnt work for me
        fourcc = cv2.VideoWriter.fourcc(*'H264')
        video_output = cv2.VideoWriter(self.output_video, fourcc, frame_rate, (frame_width, frame_height))
        #print(frame_limit)
        #print(self.threshold)
        

        while video.isOpened() and frame_count < frame_limit:
            ret, frame = video.read()
            if not ret:
                break
        
            processed_frame = self.detect_objects(frame)
            
            video_output.write(processed_frame)

            frame_count += 1

            # garbage   
        video.release()
        video_output.release()
        cv2.destroyAllWindows()
        return self.output_video

    def detect_objects(self, frame):
        modified_frame = frame.copy()
        # Convert frame from BGR TO RGB
        frame_rgb = cv2.cvtColor(modified_frame, cv2.COLOR_BGR2RGB)
        frame_tensor = F.to_tensor(frame_rgb).unsqueeze(0)
        frame_tensor = frame_tensor.to(self.graphics_device)
       
       
        with torch.no_grad():
            predictions = self.model(frame_tensor)

        # Extract detection results
        boxes = predictions[0]['boxes']
        labels = predictions[0]['labels']
        scores = predictions[0]['scores']
        
        # Filter by confidence threshold
        high_confidence_indices = scores > self.threshold

        high_confidence_boxes = boxes[high_confidence_indices].cpu().numpy()
        high_confidence_labels = labels[high_confidence_indices].cpu().numpy()
        high_confidence_scores = scores[high_confidence_indices].cpu().numpy()
        
        
        #using filter
        valid_result = np.isin(high_confidence_labels, self.FILTERED_LABEL_ID)
        
        high_confidence_boxes = high_confidence_boxes[valid_result]
        high_confidence_labels = high_confidence_labels[valid_result]
        high_confidence_scores = high_confidence_scores[valid_result]
        
        
        #draws boxes around selected objects (line 28)
        for box, label, score in zip(high_confidence_boxes, high_confidence_labels, high_confidence_scores):
            x1, y1, x2, y2 = map(int, box)
            label_text = f'{self.LABEL_MAP[label]}: {score:.2f}'
            cv2.rectangle(modified_frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
            cv2.putText(modified_frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1)


        return modified_frame
