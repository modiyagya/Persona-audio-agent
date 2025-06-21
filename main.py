import os

from flask import Flask, send_file
from tts import tts  # Import the tts function
import wave
from flask import render_template, request, Response

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
  """Renders the index page."""
  if request.method == "POST":
    text_input_value = request.form.get("text_input")
    print("User input text:", text_input_value)
    if text_input_value:
        audio_data = tts(text_input_value)  # Call your tts function
        return Response(audio_data, mimetype="audio/wav")  # Assuming tts returns WAV data
    return Response("No text provided", status=400)
  return render_template("index.html", submitted_text="")



@app.route("/tts", methods=["POST"])
def generate_tts():
 """Generates and returns text_input data from text input."""
 text = request.form.get("text_input")
 if text:
    audio_data = tts(text)  # Call your tts function
    with open(audio_data, "rb") as f:
       audio_content = send_file(audio_data, mimetype="audio/wav", as_attachment=True, download_name="output.wav")
       return audio_content
 return Response("No text provided", status=400)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))