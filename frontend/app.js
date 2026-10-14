// Generate and persist a unique browser session

let sessionId = localStorage.getItem("session_id");

if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem("session_id", sessionId);
}


const button = document.getElementById("askButton");
const questionInput = document.getElementById("question");
const chat = document.getElementById("chat");
const status = document.getElementById("status");


button.addEventListener("click", askQuestion);


// Allow pressing Enter to send
// Shift + Enter creates newline

questionInput.addEventListener("keydown", (event) => {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        askQuestion();

    }

});


async function askQuestion() {

    const question = questionInput.value.trim();


    if (!question) {
        return;
    }


    button.disabled = true;

    button.textContent = "Thinking...";

    status.textContent = "● Thinking";


    // User message

    chat.innerHTML += `
        <div class="message user">
            <div class="avatar">You</div>
            <div class="bubble">
                ${escapeHtml(question)}
            </div>
        </div>
    `;


    // AI loading message

    const thinkingId = `thinking-${Date.now()}`;


    chat.innerHTML += `
        <div class="message assistant" id="${thinkingId}">
            <div class="avatar assistant-avatar">AI</div>
            <div class="bubble">
                Thinking...
            </div>
        </div>
    `;


    chat.scrollTop = chat.scrollHeight;

    questionInput.value = "";


    try {

        console.log(
            "Sending request to n8n:",
            CONFIG.WEBHOOK_URL
        );

        console.log(
            "Request body:",
            {
                session_id: sessionId,
                question: question
            }
        );


        const response = await fetch(
            CONFIG.WEBHOOK_URL,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    session_id: sessionId,
                    question: question
                })
            }
        );


        // --------------------------------------------------
        // Log HTTP response from n8n
        // --------------------------------------------------

        console.log(
            "Response received from n8n"
        );

        console.log(
            "HTTP status:",
            response.status
        );

        console.log(
            "HTTP status text:",
            response.statusText
        );

        console.log(
            "Response OK:",
            response.ok
        );


        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status}`
            );

        }


        // --------------------------------------------------
        // Read JSON response
        // --------------------------------------------------

        const json = await response.json();


        console.log(
            "JSON received from n8n:",
            json
        );


        // Remove thinking message

        const thinking = document.getElementById(thinkingId);


        if (thinking) {
            thinking.remove();
        }


        const sourceHtml = renderSources(
            json.sources
        );


        chat.innerHTML += `
            <div class="message assistant">

                <div class="avatar assistant-avatar">
                    AI
                </div>


                <div class="bubble">

                    <div>
                        ${escapeHtml(
                            json.answer ?? "No answer received."
                        )}
                    </div>


                    ${sourceHtml}

                </div>

            </div>
        `;


        status.textContent = "● Connected";


    } catch (err) {


        console.error(
            "Request to n8n failed:",
            err
        );


        const thinking = document.getElementById(thinkingId);


        if (thinking) {
            thinking.remove();
        }


        chat.innerHTML += `
            <div class="message assistant">

                <div class="avatar assistant-avatar">
                    AI
                </div>


                <div class="bubble">

                    <strong>Error</strong>
                    <br>

                    ${escapeHtml(err.message)}

                </div>

            </div>
        `;


        status.textContent = "● Error";


    } finally {


        button.disabled = false;

        button.textContent = "Ask Question";


        questionInput.focus();

        chat.scrollTop = chat.scrollHeight;

    }

}



// Display retrieved RAG sources

function renderSources(rawSources) {


    if (!rawSources) {
        return "";
    }


    let sources = [];


    // Already an array from FastAPI

    if (Array.isArray(rawSources)) {

        sources = rawSources;

    }


    // String from n8n Data Table

    else if (typeof rawSources === "string") {

        try {

            sources = JSON.parse(rawSources);

        } catch {

            sources = [];

        }

    }


    if (!sources.length) {

        return "";

    }


    const items = sources.map(source => {


        const parts = source.split("/");


        const filename = parts.pop();

        const path = parts.join("/");


        return `

            <li>

                <strong>
                    ${escapeHtml(filename)}
                </strong>

                <small>
                    📁 ${escapeHtml(path)}
                </small>

            </li>

        `;


    }).join("");



    return `

        <details class="sources">

            <summary>
                Sources (${sources.length})
            </summary>


            <ul>
                ${items}
            </ul>


        </details>

    `;

}



// Prevent HTML injection

function escapeHtml(text) {


    const div = document.createElement("div");


    div.textContent = String(text);


    return div.innerHTML;

}
