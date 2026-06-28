import os
import tempfile
from flask import Flask, request, jsonify
from faster_whisper import WhisperModel

app = Flask(__name__)

MODEL_SIZE = os.getenv("WHISPER_MODEL", "base")
model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")

@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "sagewire-stt-service",
        "version": "1.0"
    })

@app.post("/transcribe")
def transcribe():
    if "audio" not in request.files:
        return jsonify({"error": "Missing audio file field named audio"}), 400

    audio_file = request.files["audio"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp:
        audio_path = temp.name
        audio_file.save(audio_path)

    try:
        segments, info = model.transcribe(audio_path)
        text = " ".join(segment.text.strip() for segment in segments).strip()

        return jsonify({
            "text": text,
            "language": info.language,
            "duration": info.duration
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        try:
            os.remove(audio_path)
        except Exception:
            pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
