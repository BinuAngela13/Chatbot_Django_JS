const sendBtn = document.querySelector(".b2 button");
const input = document.querySelector(".b2 input");
const contentBox = document.querySelector(".content")
let userMsg;
let notAnswered;    // flag (ans or not ans)
let notAnsQue = [];  // store not ans questions
let notAnsAns = [];  // stores the answers

//json 
//var strSimilar = require('string-similarity');
let bestMatch;
let botResponse;
const responseChat = (incomingChat) => {

    const messageElem = incomingChat.querySelector("span");

    fetch("http://127.0.0.1:8000/get_answer/", 
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    },
                body: JSON.stringify({ msg: userMsg}),
            })
        .then(res => res.json())
        .then(data => {
            console.log("data :", data);
            // showAnswer(data);

            if (data[0]){
                messageElem.textContent = data[0];  
            }               //display data in UI
            else{
                messageElem.textContent = "Sorry, I don't have a answer."
            }
                
        })
        .catch((err) => {
            messageElem.textContent = "Oops! Something went wrong. Kindly try again";
            console.log("error :", err)
        }).finally(() => contentBox.scrollTo(0, contentBox.scrollHeight));

    function showAnswer(data){
        messageElem.textContent = data[0]; 
        // if (data[0] != ''){
        //     messageElem.textContent = data[0];  
        // }               //display data in UI
        // else{
        //     messageElem.textContent = "Sorry, I don't have a answer."
        // }
        bestMatch = "";
        botResponse = "";
    }
}

const chatList = (message, className) => {
    const li = document.createElement("li");
    li.classList.add("chat", className);

    let content = className === "outgoing" ? `<span>${message}</span>`: `<img src="icon.png" class="incomingIcon"><span> ${message} </span>`;
    li.innerHTML = content;
    return li;
}

const chatSend = () => {
    userMsg = input.value.trim();
    console.log(userMsg)
    if (!input){
        return;
    }
    input.value = ""
    // Adding the user msg in content <ul>
    contentBox.appendChild(chatList(userMsg, "outgoing"));
    contentBox.scrollTo(0, contentBox.scrollHeight);
    setTimeout(() => {
        const incomingChat = chatList("Loading...", "incoming");
        contentBox.appendChild(incomingChat);
        contentBox.scrollTo(0, contentBox.scrollHeight);
        responseChat(incomingChat);
    }, 700);
}

sendBtn.addEventListener("click", chatSend);
