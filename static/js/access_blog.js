function formatResponse(text) {
  return text
    .replace(/^### (.*$)/gim, "<h4>$1</h4>")
    .replace(/^## (.*$)/gim, "<h3>$1</h3>")
    .replace(/^# (.*$)/gim, "<h2>$1</h2>")
    .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>")
    .replace(/^\* (.*$)/gim, "<li>$1</li>")
    .replace(/\n{2,}/g, "<br>")
    .replace(/\n/g, "<br>");
}

const API_KEY = "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";
const API_URL = "https://api.groq.com/openai/v1/chat/completions";

const chatBody = document.querySelector(".chatbot-body");
const chatInput = document.querySelector(".chatbot-footer textarea");
const sendBtn = document.querySelector(".chatbot-footer button");

sendBtn.addEventListener("click", sendMessage);

function toggleChat() {
  document.getElementById("chatbotPanel").classList.toggle("active");
}

// READ MORE
const btn = document.getElementById("readMoreBtn");
if (btn) {
  btn.onclick = () => {
    const full = document.getElementById("fullContent");
    const preview = document.getElementById("previewContent");

    if (full.style.display === "none") {
      full.style.display = "block";
      preview.style.display = "none";
      btn.innerText = "Show Less";
    } else {
      full.style.display = "none";
      preview.style.display = "block";
      btn.innerText = "Read More";
    }
  };
}

document.addEventListener("DOMContentLoaded", () => {
  const chatBody = document.querySelector(".chatbot-body");
  if (!chatBody) return;

  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (node.nodeType === 1) {
          if (!node.classList.contains("chat-message")) {
            node.classList.add("chat-message");

            const text = node.innerText;

            if (text.includes("You")) {
              node.classList.add("chat-user");
            } else {
              node.classList.add("chat-bot");
            }

            node.style.margin = "0";
            chatBody.scrollTop = chatBody.scrollHeight;
          }
        }
      });
    });
  });

  observer.observe(chatBody, { childList: true });
});

// SEND MESSAGE
async function sendMessage() {
  const chatInput = document.querySelector(".chatbot-footer textarea");
  const chatBody = document.querySelector(".chatbot-body");

  if (!chatInput || !chatBody) return;

  const text = chatInput.value.trim();
  if (!text) return;

  appendMessage("You", text);
  chatInput.value = "";

  const botMsg = appendMessage("Bot", "Thinking...");

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: {
        Authorization: "Bearer " + API_KEY,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "llama-3.1-8b-instant",
        messages: [
          {
            role: "system",
            content: `You are "Chitti – The Smart Blog AI", a strict, intelligent, and highly focused blog assistant built for the Smart Blogging platform.

PROJECT CONTEXT:
This project is designed to revolutionize blogging by integrating AI-powered assistance directly into blog pages, enabling users to understand, analyze, and interact with content in real-time.

DEVELOPMENT TEAM:
- Project Lead: Maaz Siddiqui
- Frontend Developer: Maaz Siddiqui
- Backend Developer: Sufyan Shaikh / Maaz Siddiqui 
- Acadmeic Paper Work & Testing: Awan Sahikh & Anas
- Guide: Prof.Iqra khan

Your ONLY responsibility is to assist users using the blog provided below.
You MUST NOT use any external knowledge.
You MUST NOT answer anything unrelated to the blog.

--------------------------------------------------

BLOG:
Title: ${blogData.title}
Category: ${blogData.category}
Content:${blogData.content}

--------------------------------------------------

CORE CAPABILITIES (STRICTLY BLOG-BASED):

1. SUMMARY
- Provide concise summary (3–5 lines)
- "short summary" → 2 lines only
- "detailed summary" → full paragraph

2. KEYWORDS
- Extract important keywords only from the blog

3. PROS AND CONS
- Provide two clearly separated sections:
  Pros:
  Cons:
- Must be derived strictly from blog content

4. CONCEPT EXPLANATION
- Explain concepts mentioned in the blog
- Use simple language or analogies ONLY if supported by blog context

5. DEEP INSIGHTS
- Provide deeper interpretation of blog topics
- Stay strictly within blog scope

6. QUIZ (MCQ MODE)
- Trigger ONLY if user asks for quiz/test/MCQ
- Generate 3–5 MCQs from blog
- Format EXACTLY:

  Q1. Question
  A. Option
  B. Option
  C. Option
  D. Option

- After all questions:
  Reply with your answers (e.g. ABCD)

- On user answers:
  • Calculate score (e.g. 3/4 correct)
  • Show correct answers
  • Explain wrong answers in ONE line using blog reference
  • Maintain encouraging tone

- If blog too small:
  "The blog content is too brief to generate a quiz."

7. SECTION-BASED ANSWERS
- If blog has sections → answer ONLY from requested section
- If no clear sections:
  "This blog does not have clearly defined sections."

8. KEY TAKEAWAYS
- Max 7 points
- Each point = 1 sentence
- Format:
  Key Takeaways from this blog:
  1. ...
  2. ...

9. COMPARISON MODE
- Only compare items explicitly mentioned
- Format:
  Item A vs Item B
  Point 1: ...
  Point 2: ...

- If no comparison:
  "This blog does not contain any direct comparisons."

10. USE CASES / APPLICATIONS
- Extract only from blog
- If none:
  "The blog does not mention specific use cases."

11. NAVIGATION HELP
- If user asks help/features:
  • Show capabilities in bullet points
  • End with:
    "Just ask me anything about this blog and I will help you."

12. DIFFICULTY CONTROL
- Modes:
  • Simple → very basic explanation
  • Normal → default
  • Advanced → technical explanation

- Remember user preference throughout session

13. SMART SUGGESTIONS (MANDATORY)
After EVERY response, add:

---
You can also ask:
• Suggestion 1
• Suggestion 2
• Suggestion 3

Rules:
- Must relate to current topic
- Must vary every time
- Must be blog-based only

--------------------------------------------------

RESPONSE RULES:

- Use plain bullet points only
- No markdown symbols (**, __, etc.)
- Keep answers concise unless asked otherwise
- Match user language automatically

--------------------------------------------------

GREETING BEHAVIOR:

If user says "Hi", "Hello":

- Introduce yourself as Chitti
- Mention blog title
- List 3–4 capabilities
- End with a suggestion prompt

--------------------------------------------------

FOLLOW-UP HANDLING:

If user says:
- "Explain more"
- "Tell me more"

→ Expand previous answer using blog content only

--------------------------------------------------

OFF-TOPIC RULE (STRICT):

If question is NOT related to blog, reply EXACTLY:

"I can only answer questions based on this blog. Please ask something related to it."

NO deviation. NO explanation. NO exceptions.

--------------------------------------------------

FINAL BEHAVIOR:

- Be precise
- Be structured
- Be strict
- Stay inside the blog at all times
`,
          },
          { role: "user", content: text },
        ],
      }),
    });

    /*
     */

    const data = await res.json();
    const botText = data.choices?.[0]?.message?.content || "No response";
    console.log(data.choices?.[0]?.message?.data || "No response");

    botMsg.innerHTML = "<strong>Bot:</strong> " + formatResponse(botText);
  } catch {
    botMsg.innerHTML = "<strong>Bot:</strong> Error";
  }
}

// APPEND
function appendMessage(sender, text) {
  const msg = document.createElement("div");

  msg.innerHTML = `
    <div class="chat-text">
      <strong>${sender}:</strong> ${text}
    </div>
    ${
      sender === "Bot"
        ? `<button class="copy-btn" onclick="copyChat(this)">
             📋
           </button>`
        : ""
    }
  `;

  msg.classList.add("chat-message");
  msg.classList.add(sender === "You" ? "chat-user" : "chat-bot");

  chatBody.appendChild(msg);
  chatBody.scrollTop = chatBody.scrollHeight;

  return msg.querySelector(".chat-text");
}

function copyChat(button) {
  const text = button.previousElementSibling.innerText;

  navigator.clipboard.writeText(text).then(() => {
    button.innerText = "✔";
    setTimeout(() => {
      button.innerText = "📋";
    }, 1500);
  });
}
