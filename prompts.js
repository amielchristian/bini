import csv from 'csv';

let endpoint = 'http://localhost:1234/v1/chat/completions'

async function getResponses(prompt)   {
    const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: `{
            "model": "HuggingFaceTB/smollm-360M-instruct-v0.2-Q8_0-GGUF/smollm-360m-instruct-add-basics-q8_0.gguf",
            "messages": [
            { "role": "system", "content": "You are a Tagalog-speaking AI assistant that accepts Tagalog prompts and returns Tagalog responses." },
            { "role": "user", "content": "${prompt}" }
            ],
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": false
        }`
    });

    let data = await response.json();
    let message = data.message;
    let messageHeader = data['message-header']

    console.log(message);
    return message;
}

async function getData() {
    try {
        return await $.getJSON('./data.json').promise();
    }
    catch (error) {
        console.log("error" + error);
    }
    finally {
        console.log('done');
    }
}