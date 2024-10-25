import cv2
import numpy as np
from pathlib import Path
import tensorflow as tf

# Load the trained model
model_filepath = Path(__file__).parent.joinpath('./models/banana_ripeness_classifier_finetuned.keras')
model = tf.keras.models.load_model(model_filepath)

# Define the labels
class_labels = ['unripe', 'partially_ripe', 'ripe', 'overripe']

def classify_banana():
    # Initialize the webcam (try with different indices if needed)
    cap = cv2.VideoCapture(1)  # Try 0, 1, or higher if this doesn't work
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None
    
    print("Camera successfully opened.")

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        # Preprocess the image
        img = cv2.resize(frame, (224, 224))  # Resize to match the input shape of the model
        img_array = np.expand_dims(img, axis=0)  # Add batch dimension
        img_array = img_array / 255.0  # Normalize the image to [0, 1] range

        # Make predictions
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]

        # Get the label
        label = class_labels[predicted_class]

        # Display the resulting frame
        cv2.putText(frame, f'Predicted: {label}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow('Banana Ripeness Classification', frame)

        # Break the loop and return the classification when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(f"Returning label: {label}")
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

    # Return the classification label
    return label

# Testing the function by running it directly
if __name__ == "__main__":
    label = classify_banana()
    if label:
        print(f"Final classification: {label}")
    else:
        print("No classification was made.")
