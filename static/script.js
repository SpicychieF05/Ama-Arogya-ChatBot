// Configuration
const API_BASE_URL = 'http://localhost:8001';
let chatHistory = [];
let isConnected = false;

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const languageSelect = document.getElementById('languageSelect');
const statusIndicator = document.getElementById('statusIndicator');
const statusText = document.getElementById('statusText');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    checkServerStatus();
    setupEventListeners();
    addWelcomeMessage();
    setupMobileMenu();
});

// Mobile Menu Setup
function setupMobileMenu() {
    const menuToggle = document.getElementById('menuToggle');
    const nav = document.getElementById('nav');
    
    if (menuToggle && nav) {
        // Simple responsive menu toggle
        menuToggle.onclick = () => {
            menuToggle.classList.toggle('active');
            nav.classList.toggle('active');
        };
        
        // Close menu when clicking on a link
        nav.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', function() {
                menuToggle.classList.remove('active');
                nav.classList.remove('active');
            });
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!menuToggle.contains(e.target) && !nav.contains(e.target)) {
                menuToggle.classList.remove('active');
                nav.classList.remove('active');
            }
        });
    }
}

// Event Listeners
function setupEventListeners() {
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    sendButton.addEventListener('click', sendMessage);

    languageSelect.addEventListener('change', function() {
        addSystemMessage(`Language changed to ${this.options[this.selectedIndex].text}`);
    });

    // Smooth scrolling for navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Update active navigation link on scroll
    window.addEventListener('scroll', updateActiveNavLink);
}

// Check if the backend server is running
async function checkServerStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/docs`);
        if (response.ok) {
            updateConnectionStatus(true);
        } else {
            updateConnectionStatus(false);
        }
    } catch (error) {
        updateConnectionStatus(false);
    }
}

// Update connection status
function updateConnectionStatus(connected) {
    isConnected = connected;
    
    if (connected) {
        statusIndicator.className = 'status-indicator';
        statusText.textContent = 'Connected';
        sendButton.disabled = false;
        messageInput.disabled = false;
    } else {
        statusIndicator.className = 'status-indicator connecting';
        statusText.textContent = 'Demo Mode (Server Offline)';
        sendButton.disabled = false;
        messageInput.disabled = false;
        addSystemMessage('Note: Backend server is offline. Demo responses will be simulated.');
    }
}

// Add welcome message
function addWelcomeMessage() {
    const welcomeMessages = {
        'en': 'Hello! I\'m Ama Arogya, your health assistant. How can I help you today?',
        'hi': 'नमस्ते! मैं अमा आरोग्य हूँ, आपका स्वास्थ्य सहायक। मैं आपकी कैसे सहायता कर सकता हूँ?',
        'or': 'ନମସ୍କାର! ମୁଁ ଅମା ଆରୋଗ୍ୟ, ଆପଣଙ୍କର ସ୍ୱାସ୍ଥ୍ୟ ସହାୟକ। ମୁଁ ଆପଣଙ୍କୁ କିପରି ସାହାଯ୍ୟ କରିପାରେ?'
    };
    
    setTimeout(() => {
        const language = languageSelect.value;
        addBotMessage(welcomeMessages[language] || welcomeMessages['en']);
    }, 1000);
}

// Send message
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    // Add user message to chat
    addUserMessage(message);
    messageInput.value = '';

    // Show typing indicator
    const typingId = addTypingIndicator();

    try {
        let response;
        
        if (isConnected) {
            // Try to send to real API
            const apiResponse = await fetch(`${API_BASE_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    sender_id: `demo_user_${Date.now()}`,
                    language: languageSelect.value
                }),
            });

            if (apiResponse.ok) {
                const data = await apiResponse.json();
                response = data.response;
            } else {
                throw new Error('API request failed');
            }
        } else {
            // Use demo responses
            response = getDemoResponse(message, languageSelect.value);
        }

        // Remove typing indicator and add response
        setTimeout(() => {
            removeTypingIndicator(typingId);
            addBotMessage(response);
        }, 1500); // Simulate typing delay

    } catch (error) {
        console.error('Error sending message:', error);
        setTimeout(() => {
            removeTypingIndicator(typingId);
            addBotMessage('Sorry, I encountered an error. Please try again.');
        }, 1000);
    }
}

// Send quick message
function sendQuickMessage(message) {
    messageInput.value = message;
    sendMessage();
}

// Add user message to chat
function addUserMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.className = 'message user-message';
    messageElement.innerHTML = `
        <div class="message-content">
            <span>${escapeHtml(message)}</span>
            <div class="message-time">${getCurrentTime()}</div>
        </div>
        <div class="message-avatar">
            <i class="fas fa-user"></i>
        </div>
    `;
    chatMessages.appendChild(messageElement);
    scrollToBottom();
}

// Add bot message to chat
function addBotMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.className = 'message bot-message';
    messageElement.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <span>${escapeHtml(message)}</span>
            <div class="message-time">${getCurrentTime()}</div>
        </div>
    `;
    chatMessages.appendChild(messageElement);
    scrollToBottom();
}

// Add system message
function addSystemMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.className = 'message system-message';
    messageElement.innerHTML = `
        <div class="message-content" style="background: #fef3c7; color: #92400e; text-align: center; font-style: italic;">
            <span>${escapeHtml(message)}</span>
        </div>
    `;
    chatMessages.appendChild(messageElement);
    scrollToBottom();
}

// Add typing indicator
function addTypingIndicator() {
    const typingId = `typing_${Date.now()}`;
    const typingElement = document.createElement('div');
    typingElement.id = typingId;
    typingElement.className = 'message bot-message';
    typingElement.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    
    // Add typing animation styles
    const style = document.createElement('style');
    style.textContent = `
        .typing-indicator {
            display: flex;
            gap: 4px;
            align-items: center;
        }
        .typing-indicator span {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #94a3b8;
            animation: typing 1.4s infinite ease-in-out;
        }
        .typing-indicator span:nth-child(2) {
            animation-delay: 0.2s;
        }
        .typing-indicator span:nth-child(3) {
            animation-delay: 0.4s;
        }
        @keyframes typing {
            0%, 60%, 100% {
                transform: scale(1);
                opacity: 0.5;
            }
            30% {
                transform: scale(1.2);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(style);
    
    chatMessages.appendChild(typingElement);
    scrollToBottom();
    return typingId;
}

// Remove typing indicator
function removeTypingIndicator(typingId) {
    const typingElement = document.getElementById(typingId);
    if (typingElement) {
        typingElement.remove();
    }
}

// Get demo response (when server is offline)
function getDemoResponse(message, language) {
    const lowerMessage = message.toLowerCase();
    
    const responses = {
        'en': {
            fever: "For fever, take adequate rest and stay hydrated. If fever persists for more than 3 days, consult a doctor.",
            vaccination: "Children should receive vaccines at: Birth (BCG, Hepatitis B), 6 weeks (DTP, Polio), 10 weeks (DTP, Polio), 14 weeks (DTP, Polio), 9 months (Measles), 16-24 months (DTP, MMR).",
            pregnancy: "During pregnancy: eat nutritious food, take prenatal vitamins, have regular check-ups, stay hydrated, avoid alcohol and smoking, get adequate rest.",
            hello: "Hello! I'm here to help you with your health questions. What would you like to know?",
            default: "I'm here to help with health information. You can ask about symptoms, vaccination, pregnancy care, or general health advice."
        },
        'hi': {
            fever: "बुखार के लिए पर्याप्त आराम लें और हाइड्रेटेड रहें। यदि बुखार 3 दिनों से अधिक समय तक बना रहता है तो डॉक्टर से संपर्क करें।",
            vaccination: "बच्चों को टीके लगवाने चाहिए: जन्म पर (बीसीजी, हेपेटाइटिस बी), 6 सप्ताह (डीटीपी, पोलियो), 10 सप्ताह (डीटीपी, पोलियो), 14 सप्ताह (डीटीपी, पोलियो), 9 महीने (खसरा)।",
            pregnancy: "गर्भावस्था के दौरान: पौष्टिक भोजन खाएं, प्रेनेटल विटामिन लें, नियमित जांच करवाएं, हाइड्रेटेड रहें, शराब और धूम्रपान से बचें।",
            hello: "नमस्ते! मैं आपके स्वास्थ्य संबंधी प्रश्नों में सहायता के लिए यहाँ हूँ। आप क्या जानना चाहते हैं?",
            default: "मैं स्वास्थ्य जानकारी में सहायता के लिए यहाँ हूँ। आप लक्षण, टीकाकरण, गर्भावस्था देखभाल के बारे में पूछ सकते हैं।"
        },
        'or': {
            fever: "ଜ୍ବର ପାଇଁ ଯଥେଷ୍ଟ ବିଶ୍ରାମ ନିଅନ୍ତୁ ଏବଂ ପାଣି ପିଅନ୍ତୁ। ଯଦି ଜ୍ବର 3 ଦିନରୁ ଅଧିକ ସମୟ ପାଇଁ ରହିଥାଏ ତେବେ ଡାକ୍ତରଙ୍କ ସହିତ ଯୋଗାଯୋଗ କରନ୍ତୁ।",
            vaccination: "ଶିଶୁମାନେ ଟୀକା ନେବା ଉଚିତ: ଜନ୍ମ ସମୟରେ (BCG, ହେପାଟାଇଟିସ B), 6 ସପ୍ତାହରେ (DTP, ପୋଲିଓ), 10 ସପ୍ତାହରେ (DTP, ପୋଲିଓ), 14 ସପ୍ତାହରେ (DTP, ପୋଲିଓ), 9 ମାସରେ (ମିଜଲସ)।",
            pregnancy: "ଗର୍ଭାବସ୍ଥା ସମୟରେ: ପୁଷ୍ଟିକର ଖାଦ୍ୟ ଖାଆନ୍ତୁ, ପ୍ରେନାଟାଲ ଭିଟାମିନ ନିଅନ୍ତୁ, ନିୟମିତ ଯାଞ୍ଚ କରାନ୍ତୁ, ପାଣି ପିଅନ୍ତୁ।",
            hello: "ନମସ୍କାର! ମୁଁ ଆପଣଙ୍କର ସ୍ୱାସ୍ଥ୍ୟ ପ୍ରଶ୍ନରେ ସାହାଯ୍ୟ କରିବାକୁ ଏଠାରେ ଅଛି। ଆପଣ କଣ ଜାଣିବାକୁ ଚାହାଁନ୍ତି?",
            default: "ମୁଁ ସ୍ୱାସ୍ଥ୍ୟ ସୂଚନା ସାହାଯ୍ୟ ପାଇଁ ଏଠାରେ ଅଛି। ଆପଣ ଲକ୍ଷଣ, ଟୀକାକରଣ, ଗର୍ଭାବସ୍ଥା ଯତ୍ନ ବିଷୟରେ ପଚାରିପାରିବେ।"
        }
    };

    const langResponses = responses[language] || responses['en'];

    if (lowerMessage.includes('fever') || lowerMessage.includes('ज्वर') || lowerMessage.includes('ଜ୍ବର')) {
        return langResponses.fever;
    } else if (lowerMessage.includes('vaccination') || lowerMessage.includes('vaccine') || lowerMessage.includes('टीका') || lowerMessage.includes('ଟୀକା')) {
        return langResponses.vaccination;
    } else if (lowerMessage.includes('pregnancy') || lowerMessage.includes('maternal') || lowerMessage.includes('गर्भावस्था') || lowerMessage.includes('ଗର୍ଭାବସ୍ଥା')) {
        return langResponses.pregnancy;
    } else if (lowerMessage.includes('hello') || lowerMessage.includes('hi') || lowerMessage.includes('नमस्ते') || lowerMessage.includes('ନମସ୍କାର')) {
        return langResponses.hello;
    } else {
        return langResponses.default;
    }
}

// Utility functions
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Scroll to demo section
function scrollToDemo() {
    document.getElementById('demo').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// Update active navigation link
function updateActiveNavLink() {
    const sections = ['home', 'features', 'demo', 'about'];
    const navLinks = document.querySelectorAll('.nav-link');
    
    let currentSection = '';
    
    sections.forEach(sectionId => {
        const section = document.getElementById(sectionId);
        if (section) {
            const rect = section.getBoundingClientRect();
            if (rect.top <= 100 && rect.bottom >= 100) {
                currentSection = sectionId;
            }
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${currentSection}`) {
            link.classList.add('active');
        }
    });
}

// Add click handlers for sample queries
document.addEventListener('DOMContentLoaded', function() {
    const queryItems = document.querySelectorAll('.query-category li');
    queryItems.forEach(item => {
        item.addEventListener('click', function() {
            const query = this.textContent.replace(/[""]/g, '');
            messageInput.value = query;
            sendMessage();
        });
    });
});