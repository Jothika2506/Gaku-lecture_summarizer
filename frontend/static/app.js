// @ts-nocheck
// ==============================
// NAVIGATION
// ==============================

const buttons = document.querySelectorAll(".nav-btn");
const sections = document.querySelectorAll(".section");

buttons.forEach(btn => {
  btn.addEventListener("click", () => {
    const targetId = btn.getAttribute("data-target");

    buttons.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");

    sections.forEach(sec => {
      sec.classList.toggle("active", sec.id === targetId);
    });

    // Update chat status when switching to chat section
    if (targetId === "section-chat") {
      updateChatStatus();
    }
  });
});

// ==============================
// API BASE URL
// ==============================
const API = "http://127.0.0.1:5000";

// ==============================
// UTILITY: Show/Hide Loaders
// ==============================
function showLoader(loaderId) {
  console.log("Attempting to show loader:", loaderId);
  const loader = document.getElementById(loaderId);
  if (loader) {
    loader.style.display = "block";
    loader.style.visibility = "visible";
    console.log("✅ Loader shown:", loaderId);
  } else {
    console.error("❌ Loader NOT found:", loaderId);
  }
}

function hideLoader(loaderId) {
  const loader = document.getElementById(loaderId);
  if (loader) {
    loader.style.display = "none";
  }
}

// ==============================
// MARKDOWN RENDERING HELPER
// ==============================
function renderMarkdown(text) {
  if (typeof marked !== 'undefined') {
    // Configure marked for better rendering
    marked.setOptions({
      breaks: true,
      gfm: true
    });
    return marked.parse(text);
  }
  // Fallback if marked.js not loaded
  return text.replace(/\n/g, '<br>');
}

function disableButton(button, loadingText = "Loading...") {
  if (!button) return;
  button.dataset.originalText = button.textContent;
  button.textContent = loadingText;
  button.disabled = true;
  button.style.opacity = "0.6";
  button.style.pointerEvents = "none";
}

function enableButton(button) {
  if (!button) return;
  button.textContent = button.dataset.originalText || button.textContent;
  button.disabled = false;
  button.style.opacity = "1";
  button.style.pointerEvents = "auto";
}

// ==============================
// IMPROVED ERROR HANDLING
// ==============================
function getUserFriendlyError(error, context = '') {
  let errorMsg = "";
  const errorStr = error.message || error.toString();
  
  if (errorStr.includes("Failed to fetch") || errorStr.includes("NetworkError")) {
    errorMsg = "Cannot connect to server. Please check:\n• Is the Flask server running?\n• Check your internet connection";
  } else if (errorStr.includes("timeout")) {
    errorMsg = "Request timed out. The file might be too large or your connection is slow.";
  } else if (errorStr.includes("Invalid file type")) {
    errorMsg = errorStr;
  } else if (errorStr.includes("File too large")) {
    errorMsg = errorStr;
  } else if (context === 'transcribe') {
    errorMsg = "Transcription failed. Please try:\n• A different audio file\n• A smaller file size\n• Check audio quality";
  } else if (context === 'chat') {
    errorMsg = "Chat error. Please refresh the page and try again.";
  } else {
    errorMsg = errorStr;
  }
  
  return errorMsg;
}

// ==============================
// DOWNLOAD/EXPORT FEATURES
// ==============================
function downloadText(content, filename) {
  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// ==============================
// SESSION PERSISTENCE
// ==============================

// Store raw markdown for session persistence
let rawSummaryMarkdown = '';

function saveToLocalStorage() {
  const transcript = document.getElementById("transcriptBox").value;
  
  if (transcript.trim()) {
    localStorage.setItem('gaku_transcript', transcript);
    localStorage.setItem('gaku_timestamp', Date.now().toString());
  }
  
  // Save RAW MARKDOWN, not rendered HTML
  if (rawSummaryMarkdown.trim()) {
    localStorage.setItem('gaku_summary', rawSummaryMarkdown);
  }
}

function loadFromLocalStorage() {
  const transcript = localStorage.getItem('gaku_transcript');
  const summary = localStorage.getItem('gaku_summary');
  const timestamp = localStorage.getItem('gaku_timestamp');
  
  if (transcript && timestamp) {
    const hoursSince = (Date.now() - parseInt(timestamp)) / (1000 * 60 * 60);
    
    // Only load if less than 24 hours old
    if (hoursSince < 24) {
      if (confirm('📚 Found a saved transcript from earlier today. Would you like to restore it?')) {
        document.getElementById("transcriptBox").value = transcript;
        
        // Show download button
        const downloadTranscriptBtn = document.getElementById("downloadTranscriptBtn");
        if (downloadTranscriptBtn) downloadTranscriptBtn.style.display = "inline-block";
        
        if (summary) {
          // Store the raw markdown and render it
          rawSummaryMarkdown = summary;
          document.getElementById("summaryBox").innerHTML = renderMarkdown(summary);
          // Show download button
          const downloadBtn = document.getElementById("downloadSummaryBtn");
          if (downloadBtn) downloadBtn.style.display = "inline-block";
        }
        
        // Set context for chat
        fetch(`${API}/set_context`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ transcript })
        }).then(() => {
          updateChatStatus();
          alert("✅ Previous session restored!");
        });
      }
    } else {
      // Clear old data
      clearLocalStorage();
    }
  }
}

function clearLocalStorage() {
  localStorage.removeItem('gaku_transcript');
  localStorage.removeItem('gaku_summary');
  localStorage.removeItem('gaku_timestamp');
  rawSummaryMarkdown = '';
}

// Load on page load
window.addEventListener('DOMContentLoaded', () => {
  loadFromLocalStorage();
});

// Save whenever transcript or summary changes
window.addEventListener('load', () => {
  document.getElementById("transcriptBox").addEventListener('change', saveToLocalStorage);
});

// Auto-save every 30 seconds
setInterval(() => {
  const transcript = document.getElementById("transcriptBox").value;
  if (transcript.trim()) {
    saveToLocalStorage();
    console.log("📝 Auto-saved transcript");
  }
}, 30000);

// ==============================
// CHAT STATUS INDICATOR
// ==============================
function updateChatStatus() {
  const hasTranscript = document.getElementById("transcriptBox").value.trim();
  let statusDiv = document.getElementById("chatStatus");
  
  // Create status div if it doesn't exist
  if (!statusDiv) {
    statusDiv = document.createElement("div");
    statusDiv.id = "chatStatus";
    statusDiv.style.cssText = "padding: 12px; border-radius: 8px; margin-bottom: 16px; text-align: center; font-size: 0.9rem; font-weight: 500;";
    
    const chatSection = document.getElementById("section-chat");
    const chatMessages = document.getElementById("chatMessages");
    chatMessages.insertAdjacentElement("beforebegin", statusDiv);
  }
  
  // Update status based on transcript availability
  if (hasTranscript) {
    statusDiv.style.background = "#d1fae5";
    statusDiv.style.color = "#065f46";
    statusDiv.style.border = "1px solid #86efac";
    statusDiv.innerHTML = "✅ Lecture loaded - Ready to chat!";
  } else {
    statusDiv.style.background = "#fee2e2";
    statusDiv.style.color = "#991b1b";
    statusDiv.style.border = "1px solid #fca5a5";
    statusDiv.innerHTML = "⚠️ No lecture loaded. Please transcribe a lecture first.";
  }
}

// ==============================
// 1️⃣ FILE UPLOAD → /transcribe
// ==============================

let selectedFile = null;

const uploadBox = document.querySelector(".upload-box");
const browseButton = uploadBox.querySelector("button");

browseButton.addEventListener("click", () => {
  const input = document.createElement("input");
  input.type = "file";
  input.accept = ".mp3,.wav,.m4a,.webm";

  input.onchange = () => {
    selectedFile = input.files[0];
    uploadBox.querySelector(".upload-main").textContent = selectedFile.name;
  };

  input.click();
});

// actual upload → API
async function transcribeAudio() {
  if (!selectedFile) {
    alert("Please select an audio file first.");
    return;
  }

  // Client-side file size check
  const maxSize = 200 * 1024 * 1024; // 200MB
  if (selectedFile.size > maxSize) {
    alert(`❌ File too large (${(selectedFile.size / (1024*1024)).toFixed(1)}MB). Maximum size is 200MB.`);
    return;
  }

  const button = document.getElementById("transcribeBtn");
  disableButton(button, "🔄 Transcribing...");
  showLoader("uploadLoader");

  try {
    const formData = new FormData();
    formData.append("file", selectedFile);

    const res = await fetch(`${API}/transcribe`, {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (data.status === "success") {
      document.getElementById("transcriptBox").value = data.text;
      
      // Show download button
      const downloadBtn = document.getElementById("downloadTranscriptBtn");
      if (downloadBtn) downloadBtn.style.display = "inline-block";

      await fetch(`${API}/set_context`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transcript: data.text })
      });

      updateChatStatus();
      saveToLocalStorage();
      alert("✅ Transcription completed successfully!");
    } else {
      alert("❌ " + (data.error || "Transcription failed"));
    }
  } catch (error) {
    const friendlyError = getUserFriendlyError(error, 'transcribe');
    alert("❌ " + friendlyError);
  } finally {
    enableButton(button);
    hideLoader("uploadLoader");
  }
}

// Set up transcribe button
(function initTranscribeButton() {
  const transcribeBtn = document.getElementById("transcribeBtn");
  if (transcribeBtn) {
    transcribeBtn.onclick = transcribeAudio;
  }
  
  // Set up download transcript button handler
  const downloadTranscriptBtn = document.getElementById("downloadTranscriptBtn");
  if (downloadTranscriptBtn) {
    downloadTranscriptBtn.onclick = () => {
      const text = document.getElementById("transcriptBox").value;
      if (!text.trim()) {
        alert("⚠️ No transcript to download!");
        return;
      }
      downloadText(text, 'lecture-transcript.txt');
      alert("✅ Transcript downloaded!");
    };
  }
  
  console.log("✅ Transcribe button initialized");
})();

// ==============================
// 2️⃣ SUMMARY → /summary
// ==============================

async function generateSummary() {
  const text = document.getElementById("transcriptBox").value.trim();
  if (!text) return alert("Transcript is empty. Please transcribe audio first.");

  const button = document.getElementById("generateSummaryBtn");
  disableButton(button, "🔄 Generating...");
  showLoader("summaryLoader");

  try {
    const res = await fetch(`${API}/summary`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    const data = await res.json();

    if (data.status === "success") {
      const summaryBox = document.getElementById("summaryBox");
      // STORE RAW MARKDOWN FOR SESSION PERSISTENCE
      rawSummaryMarkdown = data.summary;
      summaryBox.innerHTML = renderMarkdown(data.summary);
      
      // Show download button
      const downloadBtn = document.getElementById("downloadSummaryBtn");
      if (downloadBtn) downloadBtn.style.display = "inline-block";
      
      saveToLocalStorage();
      alert("✅ Summary generated successfully!");
    } else {
      alert("Error: " + data.error);
    }
  } catch (error) {
    alert("❌ Error: " + error.message);
  } finally {
    enableButton(button);
    hideLoader("summaryLoader");
  }
}

// Set up summary button
(function initSummaryButton() {
  const generateSummaryBtn = document.getElementById("generateSummaryBtn");
  if (generateSummaryBtn) {
    generateSummaryBtn.onclick = generateSummary;
  }
  
  // Set up download button handler
  const downloadBtn = document.getElementById("downloadSummaryBtn");
  if (downloadBtn) {
    downloadBtn.onclick = () => {
      // Download the raw markdown, not the rendered HTML
      if (!rawSummaryMarkdown.trim()) {
        alert("⚠️ No summary to download! Generate a summary first.");
        return;
      }
      downloadText(rawSummaryMarkdown, 'lecture-summary.txt');
      alert("✅ Summary downloaded!");
    };
  }
  
  console.log("✅ Summary buttons initialized");
})();

// ==============================
// 3️⃣ CHAT → /chat
// ==============================

const chatInput = document.getElementById("chatInput");
const chatSendBtn = document.getElementById("chatSendBtn");
const chatMessages = document.getElementById("chatMessages");
const chatLoader = document.getElementById("chatLoader");

let isChatting = false;

function initChat() {
  chatMessages.innerHTML = '<p style="color: #9ca3af; text-align: center; font-size: 0.9rem;">Start a conversation with Gaku...</p>';
}

function addMessage(text, type) {
  if (chatMessages.querySelector('p[style*="color: #9ca3af"]')) {
    chatMessages.innerHTML = '';
  }

  const messageDiv = document.createElement('div');
  messageDiv.className = `chat-message ${type}`;
  
  // Create header with name and timestamp
  const headerDiv = document.createElement('div');
  headerDiv.style.cssText = 'display: flex; align-items: center; gap: 8px; padding: 0 12px 4px;';
  
  const label = document.createElement('div');
  label.className = 'message-label';
  label.textContent = type === 'user' ? 'You' : 'Gaku AI';
  
  const timestamp = document.createElement('span');
  timestamp.style.cssText = 'font-size: 0.7rem; color: #9ca3af; font-weight: 400;';
  timestamp.textContent = getTimestamp();
  
  headerDiv.appendChild(label);
  headerDiv.appendChild(timestamp);
  
  const bubble = document.createElement('div');
  bubble.className = `message-bubble ${type}`;
  
  // Render markdown for AI messages, plain text for user messages
  if (type === 'ai') {
    bubble.innerHTML = renderMarkdown(text);
  } else {
    bubble.textContent = text;
  }
  
  messageDiv.appendChild(headerDiv);
  messageDiv.appendChild(bubble);
  chatMessages.appendChild(messageDiv);
  
  chatMessages.scrollTo({
    top: chatMessages.scrollHeight,
    behavior: 'smooth'
  });
}

function getTimestamp() {
  const now = new Date();
  let hours = now.getHours();
  const minutes = now.getMinutes();
  const ampm = hours >= 12 ? 'PM' : 'AM';
  
  hours = hours % 12;
  hours = hours ? hours : 12; // 0 should be 12
  const minutesStr = minutes < 10 ? '0' + minutes : minutes;
  
  return `${hours}:${minutesStr} ${ampm}`;
}

function showTypingIndicator() {
  const typingDiv = document.createElement('div');
  typingDiv.className = 'chat-message ai';
  typingDiv.id = 'typingIndicator';
  
  const label = document.createElement('div');
  label.className = 'message-label';
  label.textContent = 'Gaku AI';
  
  const typingBubble = document.createElement('div');
  typingBubble.className = 'typing-indicator';
  typingBubble.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
  
  typingDiv.appendChild(label);
  typingDiv.appendChild(typingBubble);
  chatMessages.appendChild(typingDiv);
  
  chatMessages.scrollTo({
    top: chatMessages.scrollHeight,
    behavior: 'smooth'
  });
}

function removeTypingIndicator() {
  const indicator = document.getElementById('typingIndicator');
  if (indicator) {
    indicator.remove();
  }
}

async function sendChatMessage() {
  if (isChatting) return;
  
  const question = chatInput.value.trim();
  if (!question) {
    alert("⚠️ Please type a question first!");
    return;
  }

  // Check if transcript exists before allowing chat
  const transcriptBox = document.getElementById("transcriptBox");
  if (!transcriptBox.value.trim()) {
    alert("⚠️ Please upload and transcribe a lecture first before chatting!");
    // Switch to upload section
    const uploadBtn = document.querySelector('[data-target="section-upload"]');
    if (uploadBtn) uploadBtn.click();
    return;
  }

  addMessage(question, 'user');
  chatInput.value = '';
  chatInput.style.height = '70px';

  isChatting = true;
  disableButton(chatSendBtn, "⏳");
  chatInput.disabled = true;
  
  showTypingIndicator();

  try {
    const res = await fetch(`${API}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    const data = await res.json();

    removeTypingIndicator();

    if (data.status === "success") {
      addMessage(data.answer, 'ai');
    } else {
      // Handle "No context" error gracefully
      if (data.error && data.error.includes('No context')) {
        addMessage("⚠️ It looks like the lecture context wasn't set properly. Please transcribe your lecture again.", 'ai');
      } else {
        addMessage("❌ Error: " + data.error, 'ai');
      }
    }
  } catch (error) {
    removeTypingIndicator();
    const friendlyError = getUserFriendlyError(error, 'chat');
    addMessage("❌ " + friendlyError, 'ai');
  } finally {
    isChatting = false;
    enableButton(chatSendBtn);
    chatInput.disabled = false;
    chatInput.focus();
  }
}

chatSendBtn.addEventListener('click', sendChatMessage);

chatInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendChatMessage();
  }
});

chatInput.addEventListener('input', function() {
  this.style.height = '70px';
  this.style.height = Math.min(this.scrollHeight, 150) + 'px';
});

initChat();

// ==============================
// 4️⃣ STUDY TOOLS
// ==============================

async function generateQuiz() {
  const transcriptBox = document.getElementById("transcriptBox");
  if (!transcriptBox.value.trim()) {
    alert("⚠️ Please transcribe a lecture first before generating a quiz!");
    return;
  }

  
  const num = parseInt(document.getElementById("quizSlider").value);

  const button = document.getElementById("quizBtn");
  disableButton(button, "🔄 Generating Quiz...");

  function convertQuizToMarkdown(text) {
    if (!text) return "";

    // Convert all lines of underscores to markdown horizontal lines
    text = text.replace(/_{5,}/g, '---');

    // Add markdown headers for QUESTION X
    text = text.replace(/QUESTION (\d+)/g, '## QUESTION $1');

    // Bold the correct answer line
    text = text.replace(/CORRECT ANSWER:/g, '**CORRECT ANSWER:**');

    return text;
  }

  try {
    const res = await fetch(`${API}/quiz`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ num_questions: num })
    });

    const data = await res.json();
    
    if (data.questions) {
      document.getElementById("toolsBox").innerHTML = renderMarkdown(convertQuizToMarkdown(data.questions));

      alert("✅ Quiz generated successfully!");
    } else {
      document.getElementById("toolsBox").textContent = data.error || "Failed to generate quiz";
    }
  } catch (error) {
    document.getElementById("toolsBox").textContent = "❌ Error: " + error.message;
  } finally {
    enableButton(button);
  }
}

async function generateFlashcards() {
  const transcriptBox = document.getElementById("transcriptBox");
  if (!transcriptBox.value.trim()) {
    alert("⚠️ Please transcribe a lecture first before generating flashcards!");
    return;
  }

  // Read from slider (NOT prompt)
  const num = parseInt(document.getElementById("flashcardsSlider").value);

  const button = document.getElementById("flashcardsBtn");
  disableButton(button, "🔄 Creating...");

  try {
    const res = await fetch(`${API}/flashcards`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ num_questions: num })
    });

    const data = await res.json();
    
    if (data.status === "success" && data.flashcards) {
      document.getElementById("toolsBox").innerHTML = renderMarkdown(data.flashcards);
      alert("✅ Flashcards generated successfully!");
    } else {
      document.getElementById("toolsBox").textContent = data.error || "Failed to generate flashcards";
    }
  } catch (error) {
    document.getElementById("toolsBox").textContent = "❌ Error: " + error.message;
  } finally {
    enableButton(button);
  }
}

(function initToolsButtons() {
  // Quiz
  const quizSlider = document.getElementById("quizSlider");
  const quizValue = document.getElementById("quizValue");
  if (quizSlider && quizValue) {
    quizSlider.oninput = () => {
      quizValue.textContent = quizSlider.value;
    };
  }

  const quizBtn = document.getElementById("quizBtn");
  if (quizBtn) {
    quizBtn.onclick = generateQuiz;
  }

  // Flashcards
  const flashcardsSlider = document.getElementById("flashcardsSlider");
  const flashcardsValue = document.getElementById("flashcardsValue");
  if (flashcardsSlider && flashcardsValue) {
    flashcardsSlider.oninput = () => {
      flashcardsValue.textContent = flashcardsSlider.value;
    };
  }

  const flashcardsBtn = document.getElementById("flashcardsBtn");
  if (flashcardsBtn) {
    flashcardsBtn.onclick = generateFlashcards;
  }

  console.log("✅ Study tools buttons initialized");
})();
