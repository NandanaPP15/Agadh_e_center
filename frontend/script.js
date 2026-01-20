
// ================= SIDEBAR TOGGLE =================
const toggleBtn = document.getElementById("toggleBtn");
const sidebar = document.getElementById("sidebar");

toggleBtn.onclick = () => {
    sidebar.classList.toggle("open");
};

// ================= LANGUAGE TOGGLE =================
const enBtn = document.getElementById("enBtn");
const malBtn = document.getElementById("malBtn");

enBtn.onclick = () => {
    enBtn.classList.add("active");
    malBtn.classList.remove("active");
};

malBtn.onclick = () => {
    malBtn.classList.add("active");
    enBtn.classList.remove("active");
};

// ================= CHAT ELEMENTS =================
const sendBtn = document.getElementById("sendBtn");
const input = document.getElementById("userInput");
const historyList = document.getElementById("historyList");
const chatBody = document.getElementById("chatBody");

// ================= ADD MESSAGE =================
function addMessage(text, sender) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender);
    msgDiv.textContent = text;
    chatBody.appendChild(msgDiv);
    chatBody.scrollTop = chatBody.scrollHeight;

    // Add to search history
    if (historyList.children[0] && historyList.children[0].textContent === "No history yet") {
        historyList.innerHTML = "";
    }
    historyList.innerHTML += `<li>${text}</li>`;
}

// ================= SEND MESSAGE TO RASA =================
async function sendToRasa(message) {
    try {
        const response = await fetch("http://127.0.0.1:5005/webhooks/rest/webhook", {

            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                sender: "web_user",
                message: message
            })
        });

        const data = await response.json();

        if (data.length === 0) {
            addMessage("Sorry, I didn't understand that.", "bot");
        } else {
            data.forEach(res => {
                if (res.text) {
                    addMessage(res.text, "bot");
                }
            });
        }

    } catch (error) {
        console.error("Rasa connection error:", error);
        addMessage("Unable to connect to chatbot server.", "bot");
    }
}

// ================= SEND BUTTON =================
sendBtn.onclick = () => {
    const message = input.value.trim();
    if (message !== "") {
        addMessage(message, "user");
        sendToRasa(message);
        input.value = "";
    }
};

// ================= FILE UPLOAD =================
const uploadBtn = document.getElementById("uploadBtn");
const fileInput = document.getElementById("fileInput");

uploadBtn.onclick = () => fileInput.click();

fileInput.onchange = () => {
    if (fileInput.files.length > 0) {
        const fileName = fileInput.files[0].name;
        addMessage(`Uploaded document: ${fileName}`, "user");
        fileInput.value = "";
    }
};

// ================= VOICE INPUT =================
const micBtn = document.getElementById("micBtn");

micBtn.onclick = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Speech Recognition not supported in this browser.");
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = enBtn.classList.contains("active") ? "en-US" : "ml-IN";
    recognition.start();

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        addMessage(transcript, "user");
        sendToRasa(transcript);
    };

    recognition.onerror = (err) => {
        console.error(err);
        alert("Error recognizing speech.");
    };
};
