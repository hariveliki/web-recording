let mediaRecorder;
let stream;
let recordedChunks = [];

async function startRecording() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = (event) => {
      recordedChunks.push(event.data);
    };
    mediaRecorder.start();
  } catch (error) {
    showError("Error while startRecording: " + error.message);
  }
}

async function stopRecording() {
  try {
    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(recordedChunks, { type: "audio/webm" });
      recordedChunks = [];
      stream.getTracks().forEach((track) => track.stop());
      const formData = new FormData();
      formData.append("file", audioBlob, "recording.webm");
      const response = await fetch("/upload_audio", {
        method: "POST",
        body: formData,
      });
      if (response.ok) {
        const data = await response.json();
        console.log(data)
        await getAudioText();
      } else {
        showError("Failed to upload audio: " + response.statusText);
      }
    };
    mediaRecorder.stop();
  } catch (error) {
    showError("Error while stopRecording: " + error.message);
  }
}

async function getAudioText() {
  try {
    const response = await fetch("/get_audio_text", {
      method: "GET",
    });
    const data = await response.json();
    if (response.ok) {
      $("#audioText").val(data.text);
    } else {
      showError("Failed to get audio text: " + response.statusText);
    }
  } catch (error) {
    showError("Error while getAudioText: " + error.message);
  }
}


function showError(message) {
  const errorDiv = document.getElementById("error");
  errorDiv.textContent = message;
  errorDiv.style.display = "block";
}

export { startRecording, stopRecording, getAudioText };
