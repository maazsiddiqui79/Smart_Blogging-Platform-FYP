// publish blog msg
function copyBlogLink() {
  const text = document.getElementById("publishedLink").innerText;
  const message = document.getElementById("copyMessage");

  navigator.clipboard.writeText(text).then(function () {
    message.innerText = "Link copied successfully.";
    message.style.display = "block";

    setTimeout(function () {
      message.style.display = "none";
    }, 3000);
  });
}

// CKEditor 5 (FULL FREE BUILD)
CKEDITOR.replace("editor", {
  height: 350,

  allowedContent: true,

  toolbar: [
    ["Source"],
    ["Format", "Font", "FontSize"],
    ["Bold", "Italic", "Underline", "-", "Strike", "RemoveFormat"],
    ["TextColor", "BGColor"],
    ["Superscript", "Subscript"],
    ["NumberedList", "BulletedList", "-", "Outdent", "Indent"],
    [
      "NumberedList",
      "BulletedList",
      "-",
      "Outdent",
      "Indent",
      "-",
      "Blockquote",
      "JustifyLeft",
      "JustifyCenter",
      "JustifyRight",
    ],
    ["Link", "Unlink"],
    ["Image", "Table", "HorizontalRule", "CodeSnippet"],
    ["Undo", "Redo"],
    ["Cut", "Copy", "Paste"],
    ["Preview", "Print"],
    ["Maximize"],
  ],
});

function toggleChatbot() {
  const panel = document.getElementById("chatbotPanel");
  panel.classList.toggle("active");
}

// ---------------- FORMAT RESPONSE ----------------
function formatResponse(text) {
  return (
    text
      // Headings (#, ##, ###)
      .replace(/^### (.*$)/gim, "<h4>$1</h4>")
      .replace(/^## (.*$)/gim, "<h3>$1</h3>")
      .replace(/^# (.*$)/gim, "<h2>$1</h2>")

      // Bold
      .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>")

      // Lists (* item)
      .replace(/^\* (.*$)/gim, "<li>$1</li>")

      // Numbered points (fix spacing issue)
      .replace(/^\d+\.\s+(.*$)/gim, "<p><b>$&</b></p>")

      // Remove excessive line breaks
      .replace(/\n{2,}/g, "<br>")

      // Normal line break
      .replace(/\n/g, "<br>")
  );
}

// ---------------- GROQ CONFIG ----------------
const API_KEY = "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";
const API_URL = "https://api.groq.com/openai/v1/chat/completions";
const MODEL = "llama-3.1-8b-instant";

// ---------------- ELEMENTS ----------------
const chatBody = document.querySelector(".chatbot-body");
const chatInput = document.querySelector(".chatbot-footer textarea");
const sendBtn = document.querySelector(".chatbot-footer button");

// ---------------- EVENTS ----------------
sendBtn.addEventListener("click", sendMessage);

chatInput.addEventListener("keydown", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// ---------------- SEND MESSAGE ----------------
async function sendMessage() {
  const userText = chatInput.value.trim();
  if (!userText) return;

  appendMessage("You", userText);
  chatInput.value = "";

  const botMsg = appendMessage("Bot", "Thinking...");

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        Authorization: "Bearer " + API_KEY,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: MODEL,
        messages: [
          {
            role: "system",
            content: `
You are **"Chitti – Smart Blog AI Assistant"**, an intelligent writing assistant inside the Smart Blogging platform.

Developed by:

* Maaz Siddiqui (Project Lead / Frontend & Backend Developer)
* Suffiyan Shakih (Backend Developer)
* Awan , Anas (Paper work and Assitant)
* Final Year Diploma Project developed to solve Problems Like Time-consuming writing, Poor structure, Lack of ideas, Weak grammar, Inconsistent formatting, No SEO optimization, Difficult editing, No summarization, Content rewriting issues, CKEditor formatting difficulty, Poor organization, No smart assistance, Inefficient workflow
* College: M.H. Saboo Siddik College (Computer Engineering)

---

## 🎯 CORE ROLE

You help users in:

* Blog writing
* Blog improvement
* Content editing
* Content structuring
* Idea generation

You are NOT restricted to a single blog. You work dynamically based on user instructions.

---

## 🧠 HOW YOU SHOULD BEHAVE

You must:

* Follow the user’s instruction exactly
* Modify only what the user asks
* Not add unnecessary content
* Keep responses clean and structured

---

## ✍️ WHAT YOU CAN DO

### • BLOG GENERATION

* Create full blogs from scratch
* Include: Title, Introduction, Body, Conclusion
* Keep it readable and structured

---

### • CONTENT IMPROVEMENT

* Improve grammar and clarity
* Make content more engaging
* Keep original meaning intact

---

### • CONTENT MODIFICATION (IMPORTANT)

You MUST support instructions like:

* "Remove the title"
* "Remove introduction"
* "Shorten this paragraph"
* "Expand this section"
* "Rewrite this part professionally"

Only modify requested parts. Do NOT change everything.

---

### • SUMMARIZATION

* Short summary → 2–3 lines
* Normal summary → 3–5 lines
* Detailed summary → paragraph

---

### • IDEA GENERATION

* Blog topic ideas
* Section ideas
* Content expansion ideas
* Headline suggestions

---

### • STRUCTURING CONTENT

* Convert plain text into structured blog
* Add headings and subheadings
* Organize into sections

---

## 🧩 CKEDITOR OUTPUT MODE (VERY IMPORTANT)

When user asks:

* "Give CKEditor code"
* "Format for editor"
* "Generate HTML"

You MUST:

* Output clean HTML only
* No explanation
* Use only these tags:

<h1>, <h2>, <h3>, <p>, <ul>, <ol>, <li>, <strong>, <em>, <blockquote> , <tr>,<td>

* No CSS
* No JS
* No inline styling

Example structure:

<h1>Title</h1>
<p>Introduction...</p>
<h2>Section</h2>
<p>Content...</p>

---

## 💬 RESPONSE RULES

* Keep answers clean and direct
* Use proper formatting
* No unnecessary symbols or decoration
* Be concise unless user asks for detail

---

## 🤖 GREETING RULE

If user says "Hi" or "Hello":

* Introduce yourself as Chitti
* Say you can help with writing, editing, and formatting blogs

---

## 🚫 RESTRICTIONS

* Do NOT over-modify content
* Do NOT ignore user instructions
* Do NOT add extra sections unless asked

---

## 🎯 GOAL

Act like a **real writing assistant** that:

* Helps users build blogs step-by-step
* Edits content precisely
* Generates clean CKEditor-compatible output
* Provides useful ideas when needed
`,
          },
          {
            role: "user",
            content: userText,
          },
        ],
        temperature: 0.7,
        max_tokens: 1024,
      }),
    });

    const data = await response.json();

    const botText =
      data.choices?.[0]?.message?.content || "No response from AI.";

    botMsg.innerHTML = "<strong>Bot:</strong> " + formatResponse(botText);
  } catch (error) {
    botMsg.innerHTML = "<strong>Bot:</strong> Error connecting to AI.";
    console.error(error);
  }
}

// ---------------- APPEND MESSAGE ----------------
function appendMessage(sender, text) {
  const msg = document.createElement("div");

  msg.innerHTML = `
    <div class="chat-text">
      <strong>${sender}:</strong> ${text}
    </div>
    ${
      sender === "Bot"
        ? `<button class="copy-btn" onclick="copyChat(this)">
             <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
               <path d="M10 1H3a2 2 0 0 0-2 2v9h1V3a1 1 0 0 1 1-1h7V1z"/>
               <path d="M13 3H6a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h7a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2zm0 11H6a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1z"/>
             </svg>
           </button>`
        : ""
    }
  `;

  chatBody.appendChild(msg);
  chatBody.scrollTop = chatBody.scrollHeight;
  return msg.querySelector(".chat-text");
}
// Copy Button functionality
function copyChat(button) {
  const text = button.previousElementSibling.innerText;

  navigator.clipboard.writeText(text).then(() => {
    button.innerHTML = "✔"; // icon change on copy
    setTimeout(() => {
      button.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
          <path d="M10 1H3a2 2 0 0 0-2 2v9h1V3a1 1 0 0 1 1-1h7V1z"/>
          <path d="M13 3H6a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h7a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2zm0 11H6a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1z"/>
        </svg>`;
    }, 1500);
  });
}
//Scripts to handle UI interactions and fix dynamically injected JS messages

function toggleChatUi() {
  const panel = document.getElementById("chatbotPanel");
  const hamburger = document.querySelector(".hamburger-icon");
  const closeIcon = document.querySelector(".close-icon");

  panel.classList.toggle("active");

  if (panel.classList.contains("active")) {
    hamburger.style.display = "none";
    closeIcon.style.display = "block";
  } else {
    hamburger.style.display = "block";
    closeIcon.style.display = "none";
  }
}

/* =========================================================
     AUTO-FORMATTER FOR NEW CHATS ADDED BY YOUR JS FILE
     This watches the chat and automatically styles any new 
     messages your JS file adds, so you don't need to change it!
  ========================================================= */
document.addEventListener("DOMContentLoaded", () => {
  const chatBody = document.querySelector(".chatbot-body");
  if (!chatBody) return;

  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (node.nodeType === 1) {
          // If a new HTML element was added

          // Add the base bubble style if missing
          if (!node.classList.contains("chat-message")) {
            node.classList.add("chat-message");

            // Check if it's a User message or Bot message
            const textContent = node.textContent || node.innerText;

            // We check if it says "You" like in your previous HTML
            if (textContent.includes("You:") || textContent.includes("You")) {
              node.classList.add("chat-user");
            } else {
              node.classList.add("chat-bot");
            }

            // Remove any default margins that your Javascript might add (like on <p> tags)
            node.style.margin = "0";

            // Automatically scroll to the bottom when a new message is added
            chatBody.scrollTop = chatBody.scrollHeight;
          }
        }
      });
    });
  });

  // Start observing the chat body for new messages
  observer.observe(chatBody, { childList: true });
});
