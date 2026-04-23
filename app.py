import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Physio Support Bot", page_icon="🦴", layout="centered")

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/physiotherapy.png", width=80)
    st.title("Physio Support Bot")
    st.markdown("""
    **Your AI-powered physiotherapy assistant.**
    
    I can help with:
    - 🦴 Joint & muscle pain
    - 🏃 Sports injuries
    - 🧍 Posture problems
    - 🔄 Recovery & rehab exercises
    - ❓ General physio questions
    """)
    st.divider()
    st.warning("⚠️ This app does not replace professional physiotherapy advice. Always consult a licensed physiotherapist.")
    st.divider()

    with st.expander("🗺️ Body Map", expanded=False):
        st.caption("Tap where it hurts → Copy message → Paste in chat")
        st.components.v1.html("""
        <style>
          * { box-sizing: border-box; margin: 0; padding: 0; }
          body { background: transparent; font-family: sans-serif; }
          .wrap { display: flex; flex-direction: column; align-items: center; padding: 0.25rem 0; }
          .figures { display: flex; gap: 10px; justify-content: center; }
          .fig-col { display: flex; flex-direction: column; align-items: center; gap: 2px; }
          .fig-label { font-size: 10px; color: #aaa; text-transform: uppercase; letter-spacing: 0.04em; }
          .info-box { margin-top: 8px; background: #f5f5f5; border-radius: 8px; padding: 8px 10px; width: 100%; border: 1px solid #e0e0e0; }
          .info-label { font-size: 10px; color: #999; margin-bottom: 3px; text-transform: uppercase; }
          .info-parts { font-size: 11px; font-weight: 500; color: #222; min-height: 16px; line-height: 1.4; }
          .info-hint { font-size: 10px; color: #bbb; margin-top: 2px; }
          .msg-box { margin-top: 6px; background: #fff; border: 1px solid #ddd; border-radius: 6px; padding: 6px 8px; font-size: 10px; color: #444; display: none; line-height: 1.4; }
          .copy-btn { margin-top: 6px; padding: 6px 14px; border-radius: 6px; border: none; background: #c0392b; color: #fff; font-size: 11px; cursor: pointer; font-weight: 500; display: none; width: 100%; }
          .copy-btn:hover { background: #a93226; }
          .clr-btn { margin-top: 4px; padding: 5px 10px; border-radius: 6px; border: 1px solid #ddd; background: transparent; color: #999; font-size: 10px; cursor: pointer; display: none; width: 100%; }
          .copy-confirm { font-size: 10px; color: #27ae60; margin-top: 4px; display: none; font-weight: 500; text-align: center; }
          .region { cursor: pointer; }
          .region:hover { opacity: 0.75; }
          .base { fill: #D4A574; }
          .highlight { fill: #E8C49A; }
          .shadow { fill: #B8865A; }
          .muscle { fill: #C49060; }
          .region.active .base { fill: #c0392b; }
          .region.active .highlight { fill: #e74c3c; }
          .region.active .shadow { fill: #922b21; }
          .region.active .muscle { fill: #a93226; }
        </style>

        <div class="wrap">
          <div class="figures">
            <div class="fig-col">
              <span class="fig-label">Front</span>
              <svg width="100" height="280" viewBox="0 0 180 460" xmlns="http://www.w3.org/2000/svg">
                <g class="region" data-part="Head" onclick="toggle(this)"><ellipse class="base" cx="90" cy="34" rx="26" ry="30"/><ellipse class="highlight" cx="83" cy="24" rx="10" ry="8"/><ellipse class="shadow" cx="90" cy="56" rx="18" ry="8"/></g>
                <g class="region" data-part="Neck" onclick="toggle(this)"><path class="base" d="M80 62 Q78 72 77 80 L103 80 Q102 72 100 62 Z"/></g>
                <g class="region" data-part="Left shoulder" onclick="toggle(this)"><path class="base" d="M77 80 Q60 78 50 88 Q44 96 46 108 Q52 104 60 102 Q68 96 74 88 Z"/></g>
                <g class="region" data-part="Right shoulder" onclick="toggle(this)"><path class="base" d="M103 80 Q120 78 130 88 Q136 96 134 108 Q128 104 120 102 Q112 96 106 88 Z"/></g>
                <g class="region" data-part="Chest" onclick="toggle(this)"><path class="base" d="M77 82 L103 82 Q112 86 114 100 Q116 116 112 124 L68 124 Q64 116 66 100 Q68 86 77 82 Z"/><path class="highlight" d="M80 84 Q90 82 100 84 Q106 88 108 98 Q96 92 90 92 Q84 92 72 98 Q74 88 80 84 Z" fill-opacity="0.4"/></g>
                <g class="region" data-part="Left upper arm" onclick="toggle(this)"><path class="base" d="M46 108 Q38 114 36 130 Q34 148 38 162 Q44 168 52 164 Q58 156 60 140 Q62 124 60 108 Z"/></g>
                <g class="region" data-part="Right upper arm" onclick="toggle(this)"><path class="base" d="M134 108 Q142 114 144 130 Q146 148 142 162 Q136 168 128 164 Q122 156 120 140 Q118 124 120 108 Z"/></g>
                <g class="region" data-part="Left elbow" onclick="toggle(this)"><ellipse class="base" cx="42" cy="166" rx="12" ry="10"/></g>
                <g class="region" data-part="Right elbow" onclick="toggle(this)"><ellipse class="base" cx="138" cy="166" rx="12" ry="10"/></g>
                <g class="region" data-part="Abdomen" onclick="toggle(this)"><path class="base" d="M68 124 L112 124 Q116 140 114 162 Q112 176 90 178 Q68 176 66 162 Q64 140 68 124 Z"/></g>
                <g class="region" data-part="Left forearm" onclick="toggle(this)"><path class="base" d="M38 168 Q30 176 28 194 Q26 212 30 224 Q36 228 44 224 Q50 214 52 196 Q54 178 48 170 Z"/></g>
                <g class="region" data-part="Right forearm" onclick="toggle(this)"><path class="base" d="M142 168 Q150 176 152 194 Q154 212 150 224 Q144 228 136 224 Q130 214 128 196 Q126 178 132 170 Z"/></g>
                <g class="region" data-part="Left wrist and hand" onclick="toggle(this)"><path class="base" d="M30 226 Q24 234 22 244 Q22 252 28 256 Q34 258 40 254 Q46 248 48 238 Q50 228 44 224 Z"/></g>
                <g class="region" data-part="Right wrist and hand" onclick="toggle(this)"><path class="base" d="M150 226 Q156 234 158 244 Q158 252 152 256 Q146 258 140 254 Q134 248 132 238 Q130 228 136 224 Z"/></g>
                <g class="region" data-part="Hips and pelvis" onclick="toggle(this)"><path class="base" d="M66 178 Q64 188 62 200 Q60 214 66 222 Q76 228 90 228 Q104 228 114 222 Q120 214 118 200 Q116 188 114 178 Z"/></g>
                <g class="region" data-part="Left thigh" onclick="toggle(this)"><path class="base" d="M66 224 Q60 232 58 252 Q56 272 58 294 Q62 306 72 310 Q80 310 84 300 Q86 282 86 260 Q86 238 84 224 Z"/></g>
                <g class="region" data-part="Right thigh" onclick="toggle(this)"><path class="base" d="M114 224 Q120 232 122 252 Q124 272 122 294 Q118 306 108 310 Q100 310 96 300 Q94 282 94 260 Q94 238 96 224 Z"/></g>
                <g class="region" data-part="Left knee" onclick="toggle(this)"><ellipse class="base" cx="72" cy="314" rx="16" ry="14"/></g>
                <g class="region" data-part="Right knee" onclick="toggle(this)"><ellipse class="base" cx="108" cy="314" rx="16" ry="14"/></g>
                <g class="region" data-part="Left shin" onclick="toggle(this)"><path class="base" d="M58 326 Q54 340 54 360 Q54 380 58 396 Q64 404 72 404 Q78 402 80 394 Q82 376 80 356 Q78 336 74 326 Z"/></g>
                <g class="region" data-part="Right shin" onclick="toggle(this)"><path class="base" d="M122 326 Q126 340 126 360 Q126 380 122 396 Q116 404 108 404 Q102 402 100 394 Q98 376 100 356 Q102 336 106 326 Z"/></g>
                <g class="region" data-part="Left ankle and foot" onclick="toggle(this)"><path class="base" d="M54 396 Q50 408 50 420 Q50 432 58 438 Q66 442 76 440 Q84 436 86 428 Q88 420 84 412 Q80 404 72 402 Z"/></g>
                <g class="region" data-part="Right ankle and foot" onclick="toggle(this)"><path class="base" d="M126 396 Q130 408 130 420 Q130 432 122 438 Q114 442 104 440 Q96 436 94 428 Q92 420 96 412 Q100 404 108 402 Z"/></g>
              </svg>
            </div>

            <div class="fig-col">
              <span class="fig-label">Back</span>
              <svg width="100" height="280" viewBox="0 0 180 460" xmlns="http://www.w3.org/2000/svg">
                <g class="region" data-part="Back of head" onclick="toggle(this)"><ellipse class="base" cx="90" cy="34" rx="26" ry="30"/><ellipse class="highlight" cx="83" cy="22" rx="9" ry="7" fill-opacity="0.4"/></g>
                <g class="region" data-part="Neck (back)" onclick="toggle(this)"><path class="base" d="M80 62 Q78 72 77 80 L103 80 Q102 72 100 62 Z"/></g>
                <g class="region" data-part="Left shoulder (back)" onclick="toggle(this)"><path class="base" d="M77 80 Q60 78 50 88 Q44 96 46 108 Q52 104 60 102 Q68 96 74 88 Z"/></g>
                <g class="region" data-part="Right shoulder (back)" onclick="toggle(this)"><path class="base" d="M103 80 Q120 78 130 88 Q136 96 134 108 Q128 104 120 102 Q112 96 106 88 Z"/></g>
                <g class="region" data-part="Upper back" onclick="toggle(this)"><path class="base" d="M74 82 L106 82 Q114 86 116 104 Q118 118 112 124 L68 124 Q62 118 64 104 Q66 86 74 82 Z"/><path class="muscle" d="M87 84 L87 124 M93 84 L93 124" stroke="#B8865A" stroke-width="1.5" fill="none" opacity="0.35"/></g>
                <g class="region" data-part="Mid back" onclick="toggle(this)"><path class="base" d="M68 124 L112 124 Q116 138 114 152 Q112 162 90 164 Q68 162 66 152 Q64 138 68 124 Z"/></g>
                <g class="region" data-part="Lower back" onclick="toggle(this)"><path class="base" d="M66 164 Q64 176 64 186 Q64 198 68 206 Q76 212 90 212 Q104 212 112 206 Q116 198 116 186 Q116 176 114 164 Z"/></g>
                <g class="region" data-part="Left glute" onclick="toggle(this)"><path class="base" d="M64 208 Q58 218 58 230 Q58 244 64 252 Q70 258 80 256 Q88 252 90 244 Q90 230 88 218 Q86 208 76 206 Z"/></g>
                <g class="region" data-part="Right glute" onclick="toggle(this)"><path class="base" d="M116 208 Q122 218 122 230 Q122 244 116 252 Q110 258 100 256 Q92 252 90 244 Q90 230 92 218 Q94 208 104 206 Z"/></g>
                <g class="region" data-part="Left hamstring" onclick="toggle(this)"><path class="base" d="M58 256 Q54 268 54 288 Q54 308 58 322 Q64 330 74 328 Q82 324 84 312 Q86 292 84 270 Q82 256 72 254 Z"/></g>
                <g class="region" data-part="Right hamstring" onclick="toggle(this)"><path class="base" d="M122 256 Q126 268 126 288 Q126 308 122 322 Q116 330 106 328 Q98 324 96 312 Q94 292 96 270 Q98 256 108 254 Z"/></g>
                <g class="region" data-part="Left knee (back)" onclick="toggle(this)"><ellipse class="base" cx="70" cy="330" rx="16" ry="13"/></g>
                <g class="region" data-part="Right knee (back)" onclick="toggle(this)"><ellipse class="base" cx="110" cy="330" rx="16" ry="13"/></g>
                <g class="region" data-part="Left calf" onclick="toggle(this)"><path class="base" d="M56 342 Q52 356 52 374 Q52 392 56 406 Q62 414 72 412 Q80 408 82 398 Q84 380 82 360 Q80 344 70 340 Z"/></g>
                <g class="region" data-part="Right calf" onclick="toggle(this)"><path class="base" d="M124 342 Q128 356 128 374 Q128 392 124 406 Q118 414 108 412 Q100 408 98 398 Q96 380 98 360 Q100 344 110 340 Z"/></g>
                <g class="region" data-part="Left heel and Achilles" onclick="toggle(this)"><path class="base" d="M54 408 Q50 418 50 428 Q50 440 58 446 Q66 450 76 446 Q84 440 84 430 Q84 420 80 412 Q74 408 66 408 Z"/></g>
                <g class="region" data-part="Right heel and Achilles" onclick="toggle(this)"><path class="base" d="M126 408 Q130 418 130 428 Q130 440 122 446 Q114 450 104 446 Q96 440 96 430 Q96 420 100 412 Q106 408 114 408 Z"/></g>
                <g class="region" data-part="Left upper arm (back)" onclick="toggle(this)"><path class="base" d="M46 108 Q38 114 36 130 Q34 148 38 162 Q44 168 52 164 Q58 156 60 140 Q62 124 60 108 Z"/></g>
                <g class="region" data-part="Right upper arm (back)" onclick="toggle(this)"><path class="base" d="M134 108 Q142 114 144 130 Q146 148 142 162 Q136 168 128 164 Q122 156 120 140 Q118 124 120 108 Z"/></g>
              </svg>
            </div>
          </div>

          <div class="info-box">
            <div class="info-label">Selected</div>
            <div class="info-parts" id="sel-display">None — tap above</div>
            <div class="info-hint" id="sel-hint">Select multiple areas</div>
            <div class="msg-box" id="msg-box"></div>
            <button class="copy-btn" id="copy-btn" onclick="copyMsg()">Copy message</button>
            <button class="clr-btn" id="clr-btn" onclick="clearAll()">Clear</button>
            <div class="copy-confirm" id="copy-confirm">✅ Copied! Paste it in the chat.</div>
          </div>
        </div>

        <script>
          const sel = new Set();
          function toggle(el) {
            const part = el.getAttribute('data-part');
            if (sel.has(part)) { sel.delete(part); el.classList.remove('active'); }
            else { sel.add(part); el.classList.add('active'); }
            update();
          }
          function update() {
            const d = document.getElementById('sel-display');
            const h = document.getElementById('sel-hint');
            const mb = document.getElementById('msg-box');
            const cb = document.getElementById('copy-btn');
            const clr = document.getElementById('clr-btn');
            const conf = document.getElementById('copy-confirm');
            conf.style.display = 'none';
            if (sel.size === 0) {
              d.textContent = 'None — tap above';
              h.style.display = 'block';
              mb.style.display = 'none';
              cb.style.display = 'none';
              clr.style.display = 'none';
            } else {
              d.textContent = Array.from(sel).join(', ');
              h.style.display = 'none';
              const msg = 'I have pain or discomfort in the following area(s): ' + Array.from(sel).join(', ') + '. Can you help me understand what might be causing it and what I should do?';
              mb.textContent = msg;
              mb.style.display = 'block';
              cb.style.display = 'block';
              clr.style.display = 'block';
            }
          }
          function clearAll() {
            sel.clear();
            document.querySelectorAll('.region.active').forEach(e => e.classList.remove('active'));
            update();
          }
          function copyMsg() {
            const msg = 'I have pain or discomfort in the following area(s): ' + Array.from(sel).join(', ') + '. Can you help me understand what might be causing it and what I should do?';
            navigator.clipboard.writeText(msg).then(() => {
              document.getElementById('copy-confirm').style.display = 'block';
            }).catch(() => {
              document.execCommand('copy');
              document.getElementById('copy-confirm').style.display = 'block';
            });
          }
        </script>
        """, height=500, scrolling=True)

    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Main Area ---
st.title("🦴 Physio Support Bot")
st.caption("Physiotherapy guidance, available anytime.")

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Welcome message ---
if len(st.session_state.messages) == 0:
    st.markdown("""
    👋 **Welcome! I'm Physio Support Bot.**

    I'm here to help with physiotherapy-related questions and concerns.
    Whether you're dealing with pain, an injury, or need exercise guidance — just ask!

    **How to use:**
    - Type your question directly below, or
    - Open the **Body Map** in the left sidebar, tap where it hurts, copy the message and paste it below

    > ⚠️ I provide general guidance only. Always consult a licensed physiotherapist for diagnosis and treatment.
    """)

# --- Display chat history ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat function ---
def chat(user_input):
    messages = [
        {
            "role": "system",
            "content": """
            You are Physio Support Bot, a professional and friendly physiotherapy assistant
            for the general public. You specialize in musculoskeletal and orthopedic rehab.
            You do NOT replace a licensed physiotherapist — always remind users to seek
            professional help for diagnosis and treatment.
            If a question is unrelated to physiotherapy or health, politely let the user know.
            Always respond in this format:

            **Possible Cause:**
            ...

            **What To Do:**
            ...

            **What To Avoid:**
            ...

            **When To See a Physiotherapist:**
            ...

            Keep responses simple, clear, and patient-friendly.
            """
        }
    ]
    for msg in st.session_state.messages[-5:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )
    return response.choices[0].message.content

# --- Chat input ---
if prompt := st.chat_input("Describe your pain or paste your body map message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
