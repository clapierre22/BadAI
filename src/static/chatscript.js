document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chatBox');
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const typingIndicator = document.getElementById('typingIndicator');

    // Send message on button click
    sendButton.addEventListener('click', () => {
        sendMessage();
    });

    // Send message on key press (enter key)
    userInput.addEventListener('keypress', (e) => {
        if (e.key ==='Enter') {
            sendMessage();
        }
    });

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message || message.length === 0) {
            return;
        }
        appendMessage(message, true);
        userInput.value = '';
        await processInput(message);
    })

    function sendMessage() {
        const message = userInput.value.trim();
        if (!message || message.length === 0) {
            alert('Please enter a message.');
            return;
        }

        appendMessage('You', message);
        userInput.value = '';

        fetch('/process_input', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',

            },
            body: JSON.stringify({ input: message }),
        })
        .then(response => response.json())
        .then(data => {
            appendMessage('BadAI', data.response);
        })
        .catch(error => {
            console.error('ERROR:', error);
            appendMessage('BadAI', 'Sorry, an error occured.');
        });
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
            const response = await fetch(
                '/process_input',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ user_input: input }),
                }
            );
            hideTyping();
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            if (data.error) {
                console.error('Error:', data.error);
                appendMessage('BadAI', 'Sorry, an error occurred.');
            } else {
                appendMessage(data.response, false);
            }
        } catch (error) {
            console.error('Error processing input:', error);
            hideTyping();
            addMessage('Sorry, an error occurred while processing your request.', false);
        }  
    }
})