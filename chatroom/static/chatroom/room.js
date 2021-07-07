// File to handle sending messages, receiving messages,
// and the visualization of the messages in a chatroom

function scrollToBottom(){
    let messages_div = document.getElementById("messages");
    messages_div.scrollTop = messages_div.scrollHeight;
}

scrollToBottom();

const room_name = JSON.parse(document.getElementById('room_name').textContent);
const username = JSON.parse(document.getElementById('username').textContent);

// Instance socket to send messages
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + room_name
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    // Show messages when the server sends them
    if (data.message){
        document.querySelector("#messages").innerHTML += ('<b>' + data.username + '</b>: ' + data.message + '<br>');
    }else {
        alert('The message is empty!');
    }
    scrollToBottom();
};

chatSocket.onclose = function(e) {
    console.log('The socket close unexpectadly.')
};

// Add functionality to button to send messages
document.querySelector("#send_message").onclick = function(e) {
    // Get the message to send
    const message_dom = document.querySelector('#input_message');
    const message_to_send = message_dom.value;

    // Send the message to the server as JSON
    chatSocket.send(JSON.stringify({
        'message': message_to_send,
        'username': username,
        'room_name': room_name
    }));

    // Clear the input message control 
    message_dom.value = '';
};