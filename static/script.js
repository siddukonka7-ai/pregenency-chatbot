function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value.trim();

    if (!message) return;

    addUserMessage(message);
    input.value = "";
    sendToServer(message);
}

function quickSend(message) {
    addUserMessage(message);
    sendToServer(message);
}

function addUserMessage(message) {
    const chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `
        <div class="user-msg">
            <div class="msg-title">You</div>
            ${escapeHtml(message)}
        </div>
    `;
    scrollChatToBottom();
}

function addBotMessage(message, extraClass = "") {
    const chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `
        <div class="bot-msg ${extraClass}">
            <div class="msg-title">Assistant</div>
            ${escapeHtml(message)}
        </div>
    `;
    scrollChatToBottom();
}

function addTypingIndicator() {
    const chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `
        <div class="bot-msg typing" id="typingIndicator">
            <div class="msg-title">Assistant</div>
            Typing...
        </div>
    `;
    scrollChatToBottom();
}

function removeTypingIndicator() {
    const typing = document.getElementById("typingIndicator");
    if (typing) typing.remove();
}

function sendToServer(message) {
    addTypingIndicator();

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        removeTypingIndicator();
        addBotMessage(data.response);
    })
    .catch(error => {
        removeTypingIndicator();
        addBotMessage("Error connecting to server.");
        console.error(error);
    });
}

function loadHistory() {
    fetch("/history")
        .then(response => response.json())
        .then(data => {
            const chatbox = document.getElementById("chatbox");
            chatbox.innerHTML = "";
            data.forEach(item => {
                chatbox.innerHTML += `
                    <div class="user-msg">
                        <div class="msg-title">You</div>
                        ${escapeHtml(item.user)}
                    </div>
                    <div class="bot-msg">
                        <div class="msg-title">Assistant</div>
                        ${escapeHtml(item.bot)}
                    </div>
                `;
            });
            scrollChatToBottom();
        })
        .catch(error => {
            addBotMessage("Could not load chat history.");
            console.error(error);
        });
}

function openHospitalMap() {
    window.open("https://www.google.com/maps/search/hospitals+near+me", "_blank");
}

function openEmergencyMap() {
    window.open("https://www.google.com/maps/search/emergency+hospital+near+me", "_blank");
}

function triggerSOS() {
    document.getElementById("sosModal").classList.remove("hidden");
}

function closeSOS() {
    document.getElementById("sosModal").classList.add("hidden");
}

function scrollChatToBottom() {
    const chatbox = document.getElementById("chatbox");
    chatbox.scrollTop = chatbox.scrollHeight;
}

function escapeHtml(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}

document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("userInput");
    if (input) {
        input.addEventListener("keydown", function (event) {
            if (event.key === "Enter") {
                sendMessage();
            }
        });
    }
});
const toggleBtn = document.getElementById("darkModeToggle");

toggleBtn.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");

  // Save theme
  if (document.body.classList.contains("dark-mode")) {
    localStorage.setItem("theme", "dark");
  } else {
    localStorage.setItem("theme", "light");
  }
});

// Load saved theme
window.onload = () => {
  if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-mode");
  }
};
