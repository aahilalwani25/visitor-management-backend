import cv2
import numpy as np
from paddleocr import PaddleOCR
import os

class IDCardScanner:
    def __init__(self):
        # Initialize PaddleOCR with English language
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
        self.camera = None
        
    def start_camera(self):
        """Initialize the camera"""
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise Exception("Could not open camera")
            
    def detect_id_card(self, image):
        """Detect ID card region using contour detection"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection
        edges = cv2.Canny(blurred, 75, 200)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Find the largest contour by area
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Only return if the contour is large enough to be an ID card
            if w > image.shape[1] * 0.3 and h > image.shape[0] * 0.3:
                return image[y:y+h, x:x+w]
        
        return image  # Return original image if no card detected
    
    def process_image(self, image):
        """Process image with PaddleOCR and draw bounding boxes"""
        # Detect ID card region
        card_region = self.detect_id_card(image)
        
        # Run OCR
        result = self.ocr.ocr(card_region, cls=True)
        
        # Draw bounding boxes and text
        for line in result:
            for word_info in line:
                points = word_info[0]
                text = word_info[1][0]
                confidence = word_info[1][1]
                
                # Convert points to integer coordinates
                points = np.array(points, dtype=np.int32)
                
                # Draw bounding box
                cv2.polylines(card_region, [points], True, (0, 255, 0), 2)
                
                # Add text
                cv2.putText(card_region, text, tuple(points[0]), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        return card_region, result
    
    def scan_id_card(self):
        """Main function to scan ID card"""
        try:
            self.start_camera()
            print("Press 's' to capture image, 'q' to quit")
            
            while True:
                ret, frame = self.camera.read()
                if not ret:
                    print("Failed to grab frame")
                    break
                
                # Display the frame
                cv2.imshow('ID Card Scanner', frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    # Process the captured image
                    processed_image, ocr_result = self.process_image(frame)
                    
                    # Display processed image
                    cv2.imshow('Processed Image', processed_image)
                    
                    # Print extracted text
                    print("\nExtracted Text:")
                    for line in ocr_result:
                        for word_info in line:
                            text = word_info[1][0]
                            confidence = word_info[1][1]
                            print(f"Text: {text}, Confidence: {confidence:.2f}")
                    
                    # Wait for key press to continue
                    cv2.waitKey(0)
        
        finally:
            if self.camera:
                self.camera.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    scanner = IDCardScanner()
    scanner.scan_id_card() 