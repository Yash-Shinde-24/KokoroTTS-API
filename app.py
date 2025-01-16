from flask import Flask, request, jsonify, send_file
from io import BytesIO
import wave
import numpy as np
from models import build_model
from kokoro import generate
import torch

app = Flask(__name__)

# Example model initialization (same as before)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
MODEL = build_model('model/kokoro-v0_19.pth', device)

# List of available speakers
AVAILABLE_SPEAKERS = ['af_bella', 'af_nicole', 'af_sarah', 'af_sky', 'af', 'am_adam', 'am_michael', 'bf_emma', 'bf_isabella', 'bm_george', 'bm_lewis']

@app.route('/tts', methods=['POST'])
def text_to_speech():
    try:
        # Parse the JSON request
        input_data = request.json
        if not input_data:
            return jsonify({"error": "Invalid JSON body"}), 400

        # Validate 'text' field
        text = input_data.get('text')
        if not text or not isinstance(text, str):
            return jsonify({"error": "'text' must be a non-empty string"}), 400

        # Validate 'speaker' field
        speaker = input_data.get('speaker')
        if not speaker or not isinstance(speaker, str):
            return jsonify({"error": "'speaker' must be a non-empty string"}), 400
        if speaker not in AVAILABLE_SPEAKERS:
            return jsonify({"error": f"Invalid speaker '{speaker}'. Available speakers are: {', '.join(AVAILABLE_SPEAKERS)}"}), 400

        # Load the voice pack for the selected speaker
        try:
            voicepack = torch.load(f'voices/{speaker}.pt', weights_only=True).to(device)
        except FileNotFoundError:
            return jsonify({"error": f"Voicepack for speaker '{speaker}' not found"}), 500

        # Process the text and generate audio
        audio = []
        for chunk in text.split("."):
            if len(chunk.strip()) < 2:
                continue
            snippet, _ = generate(MODEL, chunk.strip(), voicepack, lang=speaker[0])
            snippet = np.array(snippet, dtype=np.float32)
            snippet = (snippet * 32767).astype(np.int16)  # Convert to 16-bit PCM
            audio.extend(snippet.tolist())

        # Create a valid WAV file
        audio_data = BytesIO()
        with wave.open(audio_data, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(22050)  # Sampling rate
            wav_file.writeframes(np.array(audio, dtype=np.int16).tobytes())

        # Rewind the BytesIO buffer
        audio_data.seek(0)
        return send_file(
            audio_data,
            mimetype='audio/wav',
            as_attachment=False,
            download_name='output.wav'
        )

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)