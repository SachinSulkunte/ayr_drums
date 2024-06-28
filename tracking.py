import cv2
import numpy as np
import time
import json
import pyglet

import Instrument
import Kit

def audio_callback(drum):
    print('-- audio_callback: ' + drum.name)
    if 1:
        player = pyglet.media.Player()
        sound = pyglet.media.load(drum.file, streaming=False)
        player.queue(sound)
        player.play()
    else:
        music = pyglet.resource.media(drum.file)
        music.play()

def track_colored_object():
    # Open the webcam
    cap = cv2.VideoCapture(0)
    
    # Get the frame dimensions
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Define the lower and upper boundaries of the color in HSV
    lower_color = np.array([120, 40, 80])  # Example for lavender
    upper_color = np.array([160, 100, 255])
    
    # Initialize variables for velocity and hit detection
    prev_center = None
    prev_time = None
    interval = 0.1  # Time interval between velocity calculations in seconds
    last_velocity_update_time = time.time()
    max_velocity = 1000  # Define the maximum expected velocity (in pixels per second)
    hit_detected = False
    
    # Calculate the vertical center of the frame
    center_y_frame = frame_height // 2

    # Calculate the horizontal center of the frame
    center_x_frame = frame_width // 2
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # Get the current time
        curr_time = time.time()
        
        # Convert the frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create a mask for the specified color
        mask = cv2.inRange(hsv, lower_color, upper_color)
        
        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            # Calculate the area of the contour
            area = cv2.contourArea(contour)
            
            # Only proceed if the area meets a minimum size
            if area > 20000:
                # Compute the bounding box for the contour
                (x, y, w, h) = cv2.boundingRect(contour)
                
                # Calculate the center of the object
                center_x = int(x + w / 2)
                center_y = int(y + h / 2)
                
                # Highlight the object based on hit detection
                if hit_detected:
                    color = (0, 0, 255)  # Red color for hit
                    if center_x > center_x_frame:
                        audio_callback(SNARE)
                    elif center_x < center_x_frame:
                        audio_callback(HIHAT)
                else:
                    color = (0, 255, 0)  # Green color for normal tracking
                
                # Draw a rectangle around the object
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.circle(frame, (center_x, center_y), 5, (0, 255, 255), -1)
                
                # Check if the object passes through the vertical center of the frame
                if prev_center is not None and center_y_frame in range(prev_center[1], center_y):
                    hit_detected = True
                    # Temporary color change to red for hit
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                
                # Reset hit detection after showing the temporary color change
                if hit_detected and center_y_frame not in range(prev_center[1], center_y):
                    hit_detected = False
                
                # Estimate velocity if enough time has passed
                if prev_center is not None and prev_time is not None and (curr_time - last_velocity_update_time) >= interval:
                    dx = center_x - prev_center[0]
                    dy = center_y - prev_center[1]
                    dt = curr_time - prev_time + 1e-6  # Add a small epsilon to prevent division by zero
                    
                    # Calculate velocity components in pixels per second
                    velocity_x = dx / dt
                    velocity_y = dy / dt
                    velocity_magnitude = np.sqrt(velocity_x ** 2 + velocity_y ** 2)
                    
                    # Normalize the velocity
                    normalized_velocity = min((velocity_magnitude / max_velocity) * 100, 100)
                    
                    # Display normalized velocity on the frame
                    cv2.putText(frame, f"Velocity: {normalized_velocity:.2f} / 100", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    
                    # Update last velocity update time
                    last_velocity_update_time = curr_time
                
                # Update previous center and time
                prev_center = (center_x, center_y)
                prev_time = curr_time
        
        # Display the resulting frame
        cv2.imshow('Frame', frame)
        
        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    track_colored_object()
