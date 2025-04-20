
# 🛡️ VisionVault: Privacy-Preserving Face Blurring and Selective Decryption in Video

**VisionVault** is a computer vision + cryptography pipeline that blurs faces in videos and securely encrypts the facial regions for selective restoration.  
Designed to ensure privacy, security, and compliance, this project enables face anonymization while preserving encrypted identity data in a controllable and auditable manner.

---

## 📌 Project Overview

VisionVault combines **state-of-the-art face detection** with **secure encryption mechanisms** to create a robust, end-to-end solution for **privacy-preserving video processing**.

- 🔍 Automatically detects and blurs faces in video streams using RetinaFace.
- 🔐 Encrypts and stores cropped face data securely in a JSON format using Fernet symmetric encryption.
- 🧩 Allows **selective restoration** of encrypted faces via frame/key matching.
- 🗃️ Ensures encrypted data is stored **separately** from the processed video to maintain confidentiality.

---

## 🛠️ Technologies Used

| Category           | Stack                                      |
|-------------------|---------------------------------------------|
| Face Detection     | `RetinaFace`, `OpenCV`                     |
| Video Processing   | `OpenCV`, `NumPy`                          |
| Cryptography       | `Fernet (cryptography package)`            |
| Data Storage       | `JSON` (encrypted face data & keys)        |
| Language           | Python 3.x                                 |

---

## 🔐 Key Features

- **Face Detection + Gaussian Blurring**  
  Accurate face detection with RetinaFace, followed by Gaussian masking.

- **Per-frame Face Encryption**  
  Cropped face regions are encrypted using Fernet and saved securely.

- **Selective Face Restoration**  
  Allows authorized restoration of specified faces in specific frames via decryption keys.

- **Secure, Modular Architecture**  
  All facial data is kept encrypted outside of the main video stream, enabling compliance and audit control.

- **Plug-and-Play Design**  
  Easily integrate into any video pipeline — supports any video input.

---

## 🧠 Skills Demonstrated

- **Computer Vision** with OpenCV & RetinaFace for real-time face tracking
- **Data Privacy & Cryptography** using Fernet encryption
- **Secure Data Engineering** via JSON-based key-value storage and modular decryption
- **Automation & AI Workflow Integration**
- **Collaborative Team Engineering** on vision-driven research and development

---

## 📦 Installation & Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/visionvault.git
cd visionvault

# Install requirements
pip install opencv-python numpy cryptography retinaface
```

> ✅ Make sure to place your video files inside `./data/` or update the path in the script.

---

## ⚙️ Usage

### 🔧 1. Process and Encrypt Video

```python
video_path = "./data/sample.mp4"
process_video(video_path)
```

- Output:
  - `blurred_video.mp4` — anonymized video
  - `encrypted_faces.json` — per-frame encrypted face data + keys

---

### 🔓 2. Restore Selected Frames

```python
frame_keys = {
    "0": ["encrypted_key_1", "encrypted_key_2"],
    "3": ["encrypted_key_3", "encrypted_key_4"]
}

restore_selected_frames("./output/blurred_video.mp4", frame_keys)
```

- Output:
  - `restored_selected_frames.mp4` — only selected faces are decrypted and visible

---

## 📂 Output Summary

| File                          | Description                                     |
|-------------------------------|-------------------------------------------------|
| `blurred_video.mp4`           | Video with all faces blurred                   |
| `encrypted_faces.json`        | Encrypted face crops + keys                    |
| `restored_selected_frames.mp4`| Video with selected faces decrypted            |

---

## 👥 Team

Created with collaboration between:
- **Bhavya Shah**  
- **Aryan Bhatt**  
- **Akash**  

