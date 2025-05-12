import cv2
import numpy as np

class IdCardController:
    
    def detect_id_card(self, frame: np.ndarray) -> str:
        # Convert to grayscale and enhance contrast
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(gray, 255, 
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY, 11, 2)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        # Sort contours by area (descending)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        
        for cnt in contours:
            # Approximate the contour
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            
            # We're looking for a quadrilateral (4-sided polygon)
            if len(approx) == 4:
                # Check aspect ratio (typical ID card is ~1.6:1)
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = float(w)/h
                
                # ID card typically has aspect ratio between 1.4 and 1.8
                if 1.4 < aspect_ratio < 1.8:
                    # Check area (should be significant portion of image)
                    area = cv2.contourArea(cnt)
                    if area < (frame.shape[0] * frame.shape[1] * 0.25):  # At least 10% of image
                        return True
        
        return False