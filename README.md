# KokoroTTS-API

KokoroTTS-API is a project that extends the functionality of the **Kokoro-82M** Text-to-Speech (TTS) model by providing an easy-to-use API endpoint for generating high-quality speech. By building on top of Kokoro-82M, this project offers a simple RESTful interface, enabling seamless integration of the model into various applications.

You can explore the original Kokoro-82M repository [here](https://huggingface.co/hexgrad/Kokoro-82M).

---

## **Features**
- 🎙️ **Multiple Speaker Support**: Generate speech using pre-trained speaker models.
- 🌍 **Language Flexibility**: Supports multiple accents.
- ⚡ **Fast and Lightweight**: Optimized for performance and scalability.
- 🚀 **Dockerized Deployment**: Run the application in isolated and portable containers.

---

## **Prerequisites**

Before running the application, ensure you have the following installed:

- Python 3.11+
- Docker (optional, for containerized deployment)
- `pip` (Python package manager)

---

## **Setup Instructions**

### 1. Clone the Repository
```bash
git clone https://github.com/Yash-Shinde-24/KokoroTTS-API.git
cd KokoroTTS-API
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Prepare the Environment
- **Voice Packs**: Download the voice packs from [here](https://huggingface.co/hexgrad/Kokoro-82M/tree/main/voices) and place the `.pt` files in the `voices/` folder.
- **Voice Model Files**: Download the voice model from [here](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/kokoro-v0_19.pth) and place the `.pth` file in the `model/` folder.

### 4. Run the Application
Start the Flask server locally:
```bash
python app.py
```

Access the application at: `http://localhost:5000`

---

## **API Usage**

The application exposes a REST API for generating TTS audio.

### **POST /tts**

#### Request
```json
{
    "text": "Hello, this is a test message.",
    "speaker": "am_adam"
}
```

#### Response
- Returns a `200 OK` with a `.wav` audio file.

#### Error Handling
- `400 Bad Request`: Invalid input (e.g., missing `text` or `speaker`).
- `500 Internal Server Error`: Issues with the model or system.

---

## **Folder Structure**
```plaintext
project/
├── app.py                 # Main application entry point
├── model/                 # Directory for .pth model files
│   └── KEEP_MODELS_HERE.txt
├── voices/                # Directory for .pt voice files
│   └── KEEP_VOICE_PACKS_HERE.txt
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── .gitignore             # Git ignore rules
└── README.md              # Project documentation
```

---

## **Running with Docker**

### Build the Docker Image
```bash
docker build -t kokoro-tts .
```

### Run the Docker Container
```bash
docker run -v $(pwd)/voices:/app/voices -v $(pwd)/model:/app/model -p 5000:5000 kokoro-tts
```

Access the application at: `http://localhost:5000`

---

## **Adding New Voice Models**

1. Save the new `.pt` voice pack in the `voices/` folder.
2. Add the speaker name to your `AVAILABLE_SPEAKERS` list in `app.py`.
3. Restart the application.

---

## **License**
This project is licensed under the [Apache License](LICENSE).

---

## **Contact**

For support or inquiries:
- **Email**: yashreya999@gmail.com

---
