# Face Blurring and Encryption in Video

This project uses computer vision and cryptography to blur faces in videos while securely encrypting and storing the face data. It allows for selective decryption of specific frames, ensuring privacy while keeping the face data encrypted.

## Features

- **Face Detection and Blurring**: Detects faces in each frame of a video and applies Gaussian blur to obscure them.
- **Encryption**: Encrypts the detected face regions and stores the encrypted data along with the key in a JSON file.
- **Selective Decryption**: Enables the restoration of specific faces in the video by decrypting encrypted face data.
- **Data Security**: All sensitive face data is encrypted and stored separately from the video, ensuring privacy and security.
- **Easy Integration**: The project can be used to process any video, blur faces, and selectively restore them using the keys.

## Technologies Used

- **OpenCV**: For video processing, face detection, and manipulation.
- **RetinaFace**: For accurate face detection in images.
- **Cryptography (Fernet)**: For encrypting and decrypting face data.
- **JSON**: For storing the encrypted face data and corresponding keys.

## Requirements

To run this project, you'll need the following Python packages:

- `opencv-python`
- `numpy`
- `cryptography`
- `retinaface`

You can install these dependencies using `pip`:

``` bash
pip install opencv-python numpy cryptography retinaface
```

## Setup
Clone this repository:

``` bash
git clone https://github.com/yourusername/face-blurring-encryption.git
cd face-blurring-encryption
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Make sure to place your video files in the ./data directory (or specify your video path in the script).

Run the script:
```bash
python process_video.py
```

This will generate a blurred video along with a JSON file containing the encrypted face data and keys.

## Usage
Process Video
To process a video, blur faces, and encrypt face data, call the process_video function with the video file path.

```bash
video_path = "./data/sample.mp4"  # Path to your video file
process_video(video_path)
```

Restore Selected Frames
You can restore specific frames by providing the frame number and corresponding encryption keys in the frame_keys dictionary.

```bash
frame_keys = {
    "0": [
        "encrypted_key_1",
        "encrypted_key_2"
    ],
    "3": [
        "encrypted_key_3",
        "encrypted_key_4"
    ]
}
restore_selected_frames("./output/blurred_video.mp4", frame_keys)
```

This will restore only the specified frames (in this case, frames 0 and 3).

## Output
blurred_video.mp4: The processed video with blurred faces.
encrypted_faces.json: A JSON file containing encrypted face data and the corresponding keys.
restored_selected_frames.mp4: A video containing the selected restored frames, based on the provided encryption keys.

## Workflow
Step 1: Process and Encrypt Video
Run `process_video(video_path)` to blur faces in the video and store the encrypted face data.

Step 2: Selective Decryption
Provide the frame numbers and the corresponding keys to `restore_selected_frames` to decrypt and restore specific faces.

### Team
Thanks to Bhavya Shah, Aryan Bhatt, and Akash for awesome team work.
