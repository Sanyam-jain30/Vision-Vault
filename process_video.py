import base64
import cv2
import numpy as np
import json
import os
from cryptography.fernet import Fernet
from retinaface import RetinaFace

# Directory Setup
OUTPUT_DIR = "./output"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Generate a unique encryption key
def generate_key():
    return Fernet.generate_key()

# Encrypt face data
def encrypt_face(face_region, key):
    cipher = Fernet(key)
    face_bytes = face_region.tobytes()
    encrypted_bytes = cipher.encrypt(face_bytes)
    return encrypted_bytes

# Decrypt face data
def decrypt_face(encrypted_face, key, shape):
    cipher = Fernet(key)
    decrypted_bytes = cipher.decrypt(encrypted_face)
    return np.frombuffer(decrypted_bytes, dtype=np.uint8).reshape(shape)

# Process video: Blur faces and encrypt face data
def process_video(video_path):
    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        print("Error: Could not open video.")
        return

    frame_width = int(video_capture.get(3))
    frame_height = int(video_capture.get(4))
    fps = video_capture.get(cv2.CAP_PROP_FPS)

    frame_interval = 1  # Process one frame every second
    output_fps = 1  # Output video frame rate (1 frame per second)

    output_path = os.path.join(OUTPUT_DIR, "blurred_video.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, output_fps, (frame_width, frame_height))

    encrypted_faces = {}

    frame_number = 0
    processed_frame_number = 0

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Process only one frame per second
        if frame_number % int(fps) == 0:  # Use actual FPS to process frames at a rate of 1 frame per second
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = RetinaFace.detect_faces(rgb_frame)
            frame_data = []

            if faces:
                for face in faces.values():
                    x1, y1, x2, y2 = face['facial_area']
                    landmarks = face['landmarks']

                    # Extract face region and generate key
                    face_region = frame[y1:y2, x1:x2]
                    key = generate_key()

                    # Encode key as base64 string for storage
                    encoded_key = base64.urlsafe_b64encode(key).decode()

                    # Encrypt face
                    encrypted_face = encrypt_face(face_region, key)

                    # Save encrypted data
                    frame_data.append({"x": str(x1), "y": str(y1), "w": str(x2 - x1), "h": str(y2 - y1), "data": encrypted_face.hex(), "key": encoded_key})

                    # Blur face
                    blurred_face = cv2.GaussianBlur(face_region, (31, 31), 50)
                    frame[y1:y2, x1:x2] = blurred_face

                    # Draw bounding box and landmarks
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    for key, value in landmarks.items():
                        if isinstance(value, tuple):
                            cv2.circle(frame, value, 3, (0, 0, 255), -1)

            # Save encrypted face info for this frame
            if frame_data:
                encrypted_faces[str(processed_frame_number)] = frame_data

            # Write the processed frame at the correct frame rate (1 frame per second)
            out.write(frame)
            processed_frame_number += 1  # Keep track of processed frames

        frame_number += 1

    video_capture.release()
    out.release()

    # Save encryption data
    with open(os.path.join(OUTPUT_DIR, "encrypted_faces.json"), "w") as f:
        json.dump(encrypted_faces, f, indent=4)

    print(f"Blurred video saved to {output_path}")
    print(f"Encryption data saved to {os.path.join(OUTPUT_DIR, 'encrypted_faces.json')}")


# Restore selected frames using correct keys
def restore_selected_frames(blurred_video_path, frame_keys):
    video_capture = cv2.VideoCapture(blurred_video_path)
    if not video_capture.isOpened():
        print("Error: Could not open blurred video.")
        return

    # Load encrypted face data
    encrypted_faces_path = os.path.join(OUTPUT_DIR, "encrypted_faces.json")
    if not os.path.exists(encrypted_faces_path):
        print("Error: Encrypted faces data not found.")
        return

    with open(encrypted_faces_path, "r") as f:
        encrypted_faces_data = json.load(f)

    frame_width = int(video_capture.get(3))
    frame_height = int(video_capture.get(4))
    fps = video_capture.get(cv2.CAP_PROP_FPS)

    output_path = os.path.join(OUTPUT_DIR, "restored_selected_frames.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    restored_frames = {}

    frame_number = 0
    processed_frame_number = 0

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        if frame_number % int(fps) == 0:  # Process only frames that were originally processed
            if str(processed_frame_number) in frame_keys:
                provided_keys = frame_keys[str(processed_frame_number)]
                frame_data = encrypted_faces_data.get(str(processed_frame_number), [])

                restored_faces = 0
                for face_data in frame_data:
                    try:
                        if face_data["key"] in provided_keys:
                            x, y, w, h = int(face_data["x"]), int(face_data["y"]), int(face_data["w"]), int(face_data["h"])
                            encrypted_face = bytes.fromhex(face_data["data"])
                            key = base64.urlsafe_b64decode(face_data["key"])  

                            decrypted_face = decrypt_face(encrypted_face, key, (h, w, 3))
                            frame[y:y+h, x:x+w] = decrypted_face
                            print(f"Decrypted face {restored_faces + 1} for frame {processed_frame_number} - restored successfully.")
                            restored_faces += 1
                    except Exception as e:
                        print(f"Decryption failed for face in frame {processed_frame_number}: {e}")
                        continue  # Continue to the next face instead of stopping

                # Store the restored frame
                restored_frames[processed_frame_number] = frame.copy()

            processed_frame_number += 1  # Ensure proper indexing

        frame_number += 1

    video_capture.release()

    if not restored_frames:
        print("No frames were restored.")
        return

    # Sort frames by frame number before writing to video
    sorted_frame_numbers = sorted(restored_frames.keys())
    for frame_no in sorted_frame_numbers:
        out.write(restored_frames[frame_no])

    out.release()
    print(f"Restored video with selected frames saved to {output_path}")

# Example usage
if __name__ == "__main__":
    video_path = "./data/sample.mp4"  # Path to your video file

    # Step 1: Process and encrypt the video
    process_video(video_path)

    # Step 2: Selective decryption example (matching the correct frames)
    frame_keys = {
        "0": [
            "YVdReE5McXhnMmtMUXk2SVhPejZzVzVvdHVkelBQNlZXcEY5cXhXV3JJST0=",
            "TmhMX21yc0JHOUtoU2t1Q1VPUFhNVDFQMEVhejJUSUJKS3dPMU1ZNFVPOD0="
        ],
        "3": [
            "VXJjSkt5TEFPQnY1WERBR1lJaHo3OEhlZkt5SWVpcWs0TUFPTGpVR283UT0=",
            "YWFsLXM3OUhYS1VtYkZJVFFqazNUNkZxcGVTV203NUFoSW9mOVF1UUQtcz0="
        ]
    }

    restore_selected_frames(os.path.join(OUTPUT_DIR, "blurred_video.mp4"), frame_keys)

