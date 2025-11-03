

// Improved version with loading indicator and better error handling --deepseek--
function handleKeyPress(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
}

async function sendMessage() {
  const input = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");
  const userMessage = input.value.trim();
  
  if (!userMessage) return;

  input.value = "";
  addMessageToChat(chatBox, userMessage, 'user-msg');
  
  let loadingId = null;
  
  try {
    // Show loading indicator
    loadingId = showLoadingMessage(chatBox);
    
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMessage })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    const aiReply = data.reply;

    // Remove loading FIRST
    removeLoadingMessage(loadingId);
    loadingId = null;
    
    // Then add AI response
    addMessageToChat(chatBox, aiReply, 'bot-msg');
    
  } catch (error) {
    console.error("Error:", error);
    
    // Always remove loading in case of error
    if (loadingId) {
      removeLoadingMessage(loadingId);
    }
    
    const errorMessage = error.message.includes('HTTP error') 
      ? "Service temporarily unavailable. Please try again later."
      : "Sorry, something went wrong. Please try again.";
    
    addMessageToChat(chatBox, errorMessage, 'bot-msg error');
  }
}

// Helper functions (unchanged)
function addMessageToChat(chatBox, message, className) {
  const messageDiv = document.createElement('div');
  messageDiv.className = className;
  messageDiv.textContent = message;
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function showLoadingMessage(chatBox) {
  const loadingDiv = document.createElement('div');
  loadingDiv.className = 'bot-msg loading';
  loadingDiv.id = 'loading-' + Date.now();
  loadingDiv.textContent = 'Thinking...';
  chatBox.appendChild(loadingDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
  return loadingDiv.id;
}

function removeLoadingMessage(loadingId) {
  const loadingElement = document.getElementById(loadingId);
  if (loadingElement) {
    loadingElement.remove();
  }
}

// Add restart button functionality
function addRestartButton() {
    const chatBox = document.getElementById("chat-box");
    const restartDiv = document.createElement('div');
    restartDiv.className = 'restart-option';
    restartDiv.innerHTML = '<button onclick="restartConversation()" class="restart-btn">🔄 Start New Conversation</button>';
    chatBox.appendChild(restartDiv);
}

async function restartConversation() {
    await fetch("/reset", { method: "POST" });
    document.getElementById("chat-box").innerHTML = '';
    addMessageToChat(document.getElementById("chat-box"), 
        "Hello! I'm your INEC CVR Assistant. How can I help you with voter registration today?", 'bot-msg');
}