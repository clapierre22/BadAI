document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chatBox');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const typingIndicator = document.getElementById('typingIndicator');

    // Send message on button click or Enter key
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) {
            alert('Please enter a message.');
            return;
        }

        appendMessage('You: ' + message, true);
        userInput.value = '';
        processInput(message);
    }

    function appendMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
            
        const messageContent = document.createElement('p');
        messageContent.textContent = content;
            
        messageDiv.appendChild(messageContent);
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function showTyping() {
        typingIndicator.classList.add('visible');
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function hideTyping() {
        typingIndicator.classList.remove('visible');
    }

    async function processInput(input) {
        showTyping();
        try {
            const response = await fetch('/process_input', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_input: input }),
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            const data = await response.json();
            hideTyping();
            
            if (data.error) {
                console.error('Error:', data.error);
                appendMessage('BadAI: Sorry, an error occurred.', false);
            } else {
                appendMessage('BadAI: ' + data.response, false);
            }
        } catch (error) {
            console.error('Error processing input:', error);
            hideTyping();
            appendMessage('BadAI: Sorry, an error occurred while processing your request.', false);
        }  
    }
});