document.addEventListener('DOMContentLoaded', () => {
    const chatbox = document.getElementById('chatbox');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');

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

    function appendMessage(test, className) {
        const messageDiv = document.createElement('div');
        messageDiv.className = className;
        messageDiv.innerHTML = `<p>${text}</p>`;
        chatbox.appendChild(messageDiv);
        chatbox.scrollTop = chatbox.scrollHeight;
    }
})