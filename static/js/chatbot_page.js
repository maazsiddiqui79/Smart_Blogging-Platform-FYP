/* =========================
   FORMAT FUNCTION (UPGRADED)
========================= */
function formatResponse(text) {
  return (
    text
      // headings
      .replace(/^### (.*$)/gim, "<h4>$1</h4>")
      .replace(/^## (.*$)/gim, "<h3>$1</h3>")
      .replace(/^# (.*$)/gim, "<h2>$1</h2>")

      // bold
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")

      // bullets (• or - or *)
      .replace(/^[\-\*\•] (.*)$/gim, "<li>$1</li>")

      // wrap li into ul
      .replace(/(<li>.*<\/li>)/gims, "<ul>$1</ul>")

      // spacing
      .replace(/\n{2,}/g, "<br><br>")
      .replace(/\n/g, "<br>")
  );
}
const analyzeBtn = document.getElementById("analyze-btn");
const urlInput = document.getElementById("url-input");

const chatInput = document.getElementById("question-input");
const sendBtn = document.getElementById("send-btn");

const statusText = document.getElementById("analyze-status");

let blogData = null;

/* =========================
   FAKE PROGRESS SYSTEM
========================= */
function startProgress() {
  let percent = 0;
  const messages = [
    "Fetching blog...",
    "Extracting content...",
    "Cleaning data...",
    "Finalizing...",
  ];

  statusText.classList.remove("hidden");

  return setInterval(() => {
    percent += Math.random() * 12;
    if (percent > 95) percent = 95; // stop before 100 until done

    const msg = messages[Math.floor(percent / 25)] || "Processing...";
    statusText.innerText = `${msg} (${Math.floor(percent)}%)`;
  }, 300);
}

/* =========================
   ANALYZE BLOG
========================= */
analyzeBtn.addEventListener("click", async () => {
  const url = urlInput.value.trim();
  if (!url) return alert("Enter valid URL");

  chatInput.disabled = true;
  sendBtn.disabled = true;

  const progress = startProgress();

  try {
    const res = await fetch(
      `https://api.allorigins.win/raw?url=${encodeURIComponent(url)}`,
    );

    if (!res.ok) throw new Error("Fetch failed");

    const html = await res.text();

    const parser = new DOMParser();
    const doc = parser.parseFromString(html, "text/html");

    const title = doc.querySelector("title")?.innerText || "No title";

    let content = "";

    // improved extraction
    doc.querySelectorAll("article p, main p, p").forEach((p) => {
      const txt = p.innerText.trim();
      if (txt.length > 40) content += txt + "\n";
    });

    if (!content.trim()) throw new Error("Empty content");

    blogData = { title, content };

    appendMessage("ai", `✅ Blog analyzed: ${title}`);

    chatInput.disabled = false;
    sendBtn.disabled = false;

    statusText.innerText = "Analysis complete (100%) ✅";
    setTimeout(() => statusText.classList.add("hidden"), 2000);
  } catch (err) {
    appendMessage(
      "ai",
      "❌ Failed to analyze blog. This site may block scraping.",
    );
    statusText.classList.add("hidden");
  }

  clearInterval(progress);
});

/* =========================
   SEND MESSAGE (GROQ FIXED)
========================= */
sendBtn.addEventListener("click", sendMessage);

async function sendMessage() {
  const text = chatInput.value.trim();
  if (!text || !blogData) return;

  appendMessage("user", text);
  chatInput.value = "";

  const botMsg = appendMessage("ai", "Thinking...", true);

  try {
    const res = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: {
        Authorization:
          "Bearer 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", // 🔥 replace
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "llama-3.1-8b-instant",
        temperature: 0.3,
        messages: [
          {
            role: "system",
            content: `You are "Chitti – The Smart Blog AI", a strict and intelligent AI assistant integrated into the Smart Blogging platform.

Your role is to analyze and answer questions ONLY based on the provided blog content.

--------------------------------------------------

SYSTEM CONTEXT:

- The user first provides a blog URL
- The system extracts:
  • Blog Title
  • Blog Content
- This extracted data is passed to you

You MUST rely ONLY on this data.

--------------------------------------------------

BLOG DATA:

Title: ${blogData.title}
Content:
${blogData.content.substring(0, 8000)}
--------------------------------------------------

STRICT RULES:

- DO NOT use external knowledge
- DO NOT assume anything not in the blog
- DO NOT answer unrelated questions
- If information is missing → say it clearly

--------------------------------------------------

CORE CAPABILITIES:

1. SUMMARY
- Default: 3–5 lines
- "short summary" → 2 lines
- "detailed summary" → full paragraph

2. KEYWORDS
- Extract only from blog

3. PROS AND CONS
Format:
Pros:
- point
Cons:
- point

4. EXPLANATION
- Explain concepts from blog only
- Keep it simple unless asked advanced

5. INSIGHTS
- Provide deeper meaning based only on blog

6. QUIZ MODE
Trigger: "quiz", "mcq", "test"

Format:
Q1. Question
A. Option
B. Option
C. Option
D. Option

After questions:
Reply with answers like: ABCD

Evaluation:
- Show score
- Show correct answers
- Explain wrong ones briefly

If not enough content:
"The blog content is too brief to generate a quiz."

7. KEY TAKEAWAYS
Format:
Key Takeaways:
1. ...
2. ...

(max 7 points)

8. COMPARISON
Only if present in blog:
Item A vs Item B

Otherwise:
"No comparison found in the blog."

9. USE CASES
Only from blog
Else:
"No use cases mentioned in the blog."

10. HELP MODE
If user asks "help":
- Show capabilities
- End with:
"Ask me anything about this blog."

--------------------------------------------------

DIFFICULTY MODES:

- Simple → very easy explanation
- Normal → default
- Advanced → detailed/technical

Remember user preference.

--------------------------------------------------

FOLLOW-UP RULE:

If user says:
- "Explain more"
- "More details"

→ Expand previous answer ONLY using blog

--------------------------------------------------

OFF-TOPIC RULE:

If question is unrelated:

"I can only answer questions based on this blog. Please ask something related to it."

(NO explanation)

--------------------------------------------------

OUTPUT FORMAT RULES:

- Use clean bullet points
- No markdown symbols
- Keep answers structured
- Keep responses concise

--------------------------------------------------

SMART SUGGESTIONS (MANDATORY):

After EVERY answer:

---
You can also ask:
• (relevant question)
• (relevant question)
• (relevant question)

Rules:
- Must be based on blog
- Must be different each time

--------------------------------------------------

GREETING:

If user says "Hi" or "Hello":

- Introduce yourself as Chitti
- Mention blog title
- Show 3 capabilities
- End with suggestion

--------------------------------------------------

FINAL BEHAVIOR:

- Be strict
- Be accurate
- Stay inside blog
- Do not hallucinate`,
          },
          {
            role: "user",
            content: text,
          },
        ],
      }),
    });

    if (!res.ok) {
      const errText = await res.text();
      console.error("Groq Error:", errText);
      throw new Error("API failed");
    }

    const data = await res.json();

    let reply = "No response from AI";

    if (data && data.choices && data.choices.length > 0) {
      reply = data.choices[0].message.content.trim();
    }

    botMsg.innerHTML = `
      ${formatResponse(reply)}
      <span class="copy-btn" style="margin:2rem;" onclick="copyText(this)"><i class="bi bi-copy"></i></span>
    `;
  } catch (err) {
    console.error(err);
    botMsg.innerHTML = `<p>❌ AI failed. Try shorter query or re-analyze blog.</p>`;
  }
}

/* =========================
   APPEND MESSAGE
========================= */
function appendMessage(sender, text, isTyping = false) {
  const chatArea = document.querySelector(".chat-container");
  const msgDiv = document.createElement("div");

  if (sender === "user") {
    msgDiv.className = "chat-message user-message";
    msgDiv.innerHTML = `
    <div class="message-inner">
    
        <div class="bubble"><h6>User</h6>
        <p>${text}</p></div>
      </div>`;
  } else {
    msgDiv.className = "chat-message ai-message";
    msgDiv.innerHTML = `
      <div class="message-inner">
        <div class="bubble">
          ${isTyping ? "<p><em>Thinking...</em></p>" : `<h6>Bot</h6><p>${text}</p>`}
        </div>
      </div>`;
  }

  chatArea.appendChild(msgDiv);

  document.getElementById("chat-area").scrollTop = chatArea.scrollHeight;

  return msgDiv.querySelector(".bubble");
}

/* =========================
   COPY
========================= */
function copyText(el) {
  const text = el.parentElement.innerText.replace("Copy", "");
  navigator.clipboard.writeText(text);

  el.innerText = "Copied ✓";
  setTimeout(() => (el.innerHTML = '<i class="bi bi-copy"></i>'), 1500);
}
