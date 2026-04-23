import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="PhysioAssist AI", page_icon="🦴", layout="centered")

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/physiotherapy.png", width=80)
    st.title("PhysioAssist AI")
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
    st.warning("⚠️ This app does not replace professional physiotherapy advice. Always consult a licensed physiotherapist for diagnosis and treatment.")
    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Main Area ---
st.title("🦴 PhysioAssist AI")
st.caption("Physiotherapy guidance, available anytime.")

# --- Initialize chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Body Map ---
with st.expander("🗺️ Use Body Map — tap where it hurts", expanded=False):
    st.components.v1.html("""
    <style>
      body { margin: 0; font-family: sans-serif; background: transparent; }
      .body-wrap { display: flex; flex-direction: column; align-items: center; padding: 0.5rem 0; }
      .body-title { font-size: 14px; color: #888; margin-bottom: 0.75rem; text-align: center; }
      .body-container { display: flex; gap: 2rem; align-items: flex-start; justify-content: center; flex-wrap: wrap; }
      .views-label { font-size: 12px; color: #aaa; text-align: center; margin-bottom: 4px; }
      .selected-info { margin-top: 1rem; background: #f7f7f7; border-radius: 10px; border: 1px solid #e0e0e0; padding: 0.75rem 1rem; width: 100%; max-width: 460px; box-sizing: border-box; }
      .selected-label { font-size: 12px; color: #888; margin-bottom: 4px; }
      .selected-parts { font-size: 14px; font-weight: 500; color: #222; min-height: 20px; }
      .hint { font-size: 11px; color: #bbb; margin-top: 4px; }
      .ask-btn { margin-top: 0.75rem; padding: 8px 18px; border-radius: 8px; border: 1px solid #1D9E75; background: #1D9E75; color: white; font-size: 13px; cursor: pointer; display: none; }
      .ask-btn:hover { background: #0F6E56; }
      .clear-btn { margin-top: 0.75rem; margin-left: 8px; padding: 8px 14px; border-radius: 8px; border: 1px solid #ccc; background: transparent; color: #888; font-size: 12px; cursor: pointer; display: none; }
      .clear-btn:hover { background: #f0f0f0; }
      .btn-row { display: flex; align-items: center; flex-wrap: wrap; gap: 4px; }
      .front .region { fill: #E1F5EE; stroke: #1D9E75; stroke-width: 1; cursor: pointer; }
      .front .region:hover { fill: #9FE1CB; }
      .front .region.active { fill: #1D9E75; }
      .front .region-label { font-size: 9px; fill: #085041; pointer-events: none; text-anchor: middle; }
      .front .region.active .region-label { fill: white; }
      .back .region { fill: #E6F1FB; stroke: #378ADD; stroke-width: 1; cursor: pointer; }
      .back .region:hover { fill: #B5D4F4; }
      .back .region.active { fill: #378ADD; }
      .back .region-label { font-size: 9px; fill: #0C447C; pointer-events: none; text-anchor: middle; }
      .back .region.active .region-label { fill: white; }
      .body-outline { fill: #F1EFE8; stroke: #B4B2A9; stroke-width: 1; }
    </style>

    <div class="body-wrap">
      <p class="body-title">Tap the area(s) where you feel pain or discomfort</p>
      <div class="body-container">

        <div>
          <p class="views-label">Front</p>
          <svg class="front" width="150" height="340" viewBox="0 0 160 360" xmlns="http://www.w3.org/2000/svg">
            <g class="region" data-part="Head" onclick="toggle(this)"><ellipse cx="80" cy="30" rx="20" ry="24"/><text class="region-label" x="80" y="33">Head</text></g>
            <g class="region" data-part="Neck" onclick="toggle(this)"><rect x="72" y="53" width="16" height="12" rx="3"/><text class="region-label" x="80" y="62">Neck</text></g>
            <g class="region" data-part="Left shoulder" onclick="toggle(this)"><ellipse cx="56" cy="70" rx="12" ry="10"/><text class="region-label" x="56" y="73">L.Shldr</text></g>
            <g class="region" data-part="Right shoulder" onclick="toggle(this)"><ellipse cx="104" cy="70" rx="12" ry="10"/><text class="region-label" x="104" y="73">R.Shldr</text></g>
            <g class="region" data-part="Chest" onclick="toggle(this)"><rect x="68" y="82" width="24" height="30" rx="4"/><text class="region-label" x="80" y="100">Chest</text></g>
            <g class="region" data-part="Left upper arm" onclick="toggle(this)"><rect x="55" y="80" width="11" height="28" rx="4"/><text class="region-label" x="60" y="97">L.Arm</text></g>
            <g class="region" data-part="Right upper arm" onclick="toggle(this)"><rect x="94" y="80" width="11" height="28" rx="4"/><text class="region-label" x="99" y="97">R.Arm</text></g>
            <g class="region" data-part="Left elbow" onclick="toggle(this)"><ellipse cx="60" cy="112" rx="7" ry="6"/><text class="region-label" x="60" y="115">L.Elbow</text></g>
            <g class="region" data-part="Right elbow" onclick="toggle(this)"><ellipse cx="100" cy="112" rx="7" ry="6"/><text class="region-label" x="100" y="115">R.Elbow</text></g>
            <g class="region" data-part="Abdomen" onclick="toggle(this)"><rect x="68" y="114" width="24" height="28" rx="4"/><text class="region-label" x="80" y="131">Abdomen</text></g>
            <g class="region" data-part="Left forearm" onclick="toggle(this)"><rect x="55" y="118" width="10" height="26" rx="4"/><text class="region-label" x="60" y="134">L.Fore</text></g>
            <g class="region" data-part="Right forearm" onclick="toggle(this)"><rect x="95" y="118" width="10" height="26" rx="4"/><text class="region-label" x="100" y="134">R.Fore</text></g>
            <g class="region" data-part="Left wrist and hand" onclick="toggle(this)"><ellipse cx="60" cy="150" rx="8" ry="7"/><text class="region-label" x="60" y="153">L.Wrist</text></g>
            <g class="region" data-part="Right wrist and hand" onclick="toggle(this)"><ellipse cx="100" cy="150" rx="8" ry="7"/><text class="region-label" x="100" y="153">R.Wrist</text></g>
            <g class="region" data-part="Hips and pelvis" onclick="toggle(this)"><rect x="66" y="144" width="28" height="22" rx="4"/><text class="region-label" x="80" y="158">Hips</text></g>
            <g class="region" data-part="Left thigh" onclick="toggle(this)"><rect x="66" y="166" width="13" height="28" rx="4"/><text class="region-label" x="72" y="183">L.Thigh</text></g>
            <g class="region" data-part="Right thigh" onclick="toggle(this)"><rect x="81" y="166" width="13" height="28" rx="4"/><text class="region-label" x="87" y="183">R.Thigh</text></g>
            <g class="region" data-part="Left knee" onclick="toggle(this)"><ellipse cx="72" cy="200" rx="9" ry="8"/><text class="region-label" x="72" y="203">L.Knee</text></g>
            <g class="region" data-part="Right knee" onclick="toggle(this)"><ellipse cx="88" cy="200" rx="9" ry="8"/><text class="region-label" x="88" y="203">R.Knee</text></g>
            <g class="region" data-part="Left shin" onclick="toggle(this)"><rect x="64" y="210" width="14" height="50" rx="4"/><text class="region-label" x="71" y="238">L.Shin</text></g>
            <g class="region" data-part="Right shin" onclick="toggle(this)"><rect x="82" y="210" width="14" height="50" rx="4"/><text class="region-label" x="89" y="238">R.Shin</text></g>
            <g class="region" data-part="Left ankle and foot" onclick="toggle(this)"><ellipse cx="71" cy="266" rx="10" ry="8"/><text class="region-label" x="71" y="269">L.Ankle</text></g>
            <g class="region" data-part="Right ankle and foot" onclick="toggle(this)"><ellipse cx="89" cy="266" rx="10" ry="8"/><text class="region-label" x="89" y="269">R.Ankle</text></g>
          </svg>
        </div>

        <div>
          <p class="views-label">Back</p>
          <svg class="back" width="150" height="340" viewBox="0 0 160 360" xmlns="http://www.w3.org/2000/svg">
            <g class="region" data-part="Back of head" onclick="toggle(this)"><ellipse cx="80" cy="30" rx="20" ry="24"/><text class="region-label" x="80" y="33">Head</text></g>
            <g class="region" data-part="Neck (back)" onclick="toggle(this)"><rect x="72" y="53" width="16" height="12" rx="3"/><text class="region-label" x="80" y="62">Neck</text></g>
            <g class="region" data-part="Left shoulder (back)" onclick="toggle(this)"><ellipse cx="56" cy="70" rx="12" ry="10"/><text class="region-label" x="56" y="73">L.Shldr</text></g>
            <g class="region" data-part="Right shoulder (back)" onclick="toggle(this)"><ellipse cx="104" cy="70" rx="12" ry="10"/><text class="region-label" x="104" y="73">R.Shldr</text></g>
            <g class="region" data-part="Upper back" onclick="toggle(this)"><rect x="68" y="82" width="24" height="26" rx="4"/><text class="region-label" x="80" y="97">Upper back</text></g>
            <g class="region" data-part="Mid back" onclick="toggle(this)"><rect x="68" y="110" width="24" height="22" rx="4"/><text class="region-label" x="80" y="124">Mid back</text></g>
            <g class="region" data-part="Lower back" onclick="toggle(this)"><rect x="68" y="134" width="24" height="22" rx="4"/><text class="region-label" x="80" y="148">Lower back</text></g>
            <g class="region" data-part="Left glute" onclick="toggle(this)"><rect x="66" y="158" width="13" height="20" rx="4"/><text class="region-label" x="72" y="171">L.Glute</text></g>
            <g class="region" data-part="Right glute" onclick="toggle(this)"><rect x="81" y="158" width="13" height="20" rx="4"/><text class="region-label" x="87" y="171">R.Glute</text></g>
            <g class="region" data-part="Left hamstring" onclick="toggle(this)"><rect x="65" y="180" width="13" height="30" rx="4"/><text class="region-label" x="71" y="198">L.Hmstr</text></g>
            <g class="region" data-part="Right hamstring" onclick="toggle(this)"><rect x="82" y="180" width="13" height="30" rx="4"/><text class="region-label" x="88" y="198">R.Hmstr</text></g>
            <g class="region" data-part="Left knee (back)" onclick="toggle(this)"><ellipse cx="71" cy="216" rx="9" ry="8"/><text class="region-label" x="71" y="219">L.Knee</text></g>
            <g class="region" data-part="Right knee (back)" onclick="toggle(this)"><ellipse cx="89" cy="216" rx="9" ry="8"/><text class="region-label" x="89" y="219">R.Knee</text></g>
            <g class="region" data-part="Left calf" onclick="toggle(this)"><rect x="63" y="226" width="14" height="36" rx="4"/><text class="region-label" x="70" y="247">L.Calf</text></g>
            <g class="region" data-part="Right calf" onclick="toggle(this)"><rect x="83" y="226" width="14" height="36" rx="4"/><text class="region-label" x="90" y="247">R.Calf</text></g>
            <g class="region" data-part="Left heel and Achilles" onclick="toggle(this)"><ellipse cx="70" cy="268" rx="10" ry="8"/><text class="region-label" x="70" y="271">L.Heel</text></g>
            <g class="region" data-part="Right heel and Achilles" onclick="toggle(this)"><ellipse cx="90" cy="268" rx="10" ry="8"/><text class="region-label" x="90" y="271">R.Heel</text></g>
          </svg>
        </div>

      </div>

      <div class="selected-info">
        <div class="selected-label">Selected area(s):</div>
        <div class="selected-parts" id="selected-display">None selected — tap a region above</div>
        <p class="hint" id="hint-text">You can select multiple areas</p>
        <div class="btn-row">
          <button class="ask-btn" id="ask-btn" onclick="askPhysio()">Ask PhysioAssist about this</button>
          <button class="clear-btn" id="clear-btn" onclick="clearAll()">Clear</button>
        </div>
      </div>
    </div>

    <script>
      const selected = new Set();

      function toggle(el) {
        const part = el.getAttribute('data-part');
        if (selected.has(part)) {
          selected.delete(part);
          el.classList.remove('active');
        } else {
          selected.add(part);
          el.classList.add('active');
        }
        updateDisplay();
      }

      function updateDisplay() {
        const display = document.getElementById('selected-display');
        const askBtn = document.getElementById('ask-btn');
        const clearBtn = document.getElementById('clear-btn');
        const hint = document.getElementById('hint-text');
        if (selected.size === 0) {
          display.textContent = 'None selected — tap a region above';
          askBtn.style.display = 'none';
          clearBtn.style.display = 'none';
          hint.style.display = 'block';
        } else {
          display.textContent = Array.from(selected).join(', ');
          askBtn.style.display = 'inline-block';
          clearBtn.style.display = 'inline-block';
          hint.style.display = 'none';
        }
      }

      function clearAll() {
        selected.clear();
        document.querySelectorAll('.region.active').forEach(el => el.classList.remove('active'));
        updateDisplay();
      }

      function askPhysio() {
        const parts = Array.from(selected).join(', ');
        const msg = 'I have pain or discomfort in the following area(s): ' + parts + '. Can you help me understand what might be causing it and what I should do?';
        window.parent.postMessage({ type: 'streamlit:setComponentValue', value: msg }, '*');
      }
    </script>
    """, height=520, scrolling=False)

# --- Body map message handler ---
st.markdown("""
<script>
window.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'streamlit:setComponentValue') {
        const input = window.parent.document.querySelector('textarea[data-testid="stChatInput"]');
        if (input) {
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
            nativeInputValueSetter.call(input, event.data.value);
            input.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }
});
</script>
""", unsafe_allow_html=True)

# --- Welcome message ---
if len(st.session_state.messages) == 0:
    st.markdown("""
    👋 **Welcome! I'm PhysioAssist AI.**
    
    I'm here to help you with physiotherapy-related questions and concerns.
    Whether you're dealing with pain, recovering from an injury, or looking for 
    exercise guidance — just ask me anything!
    
    **You can either:**
    - Use the **Body Map** above to tap where it hurts
    - Or type your question directly in the chat below
    
    > ⚠️ I provide general guidance only. For diagnosis and treatment, please see a licensed physiotherapist.
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
            You are PhysioAssist AI, a professional and friendly physiotherapy assistant
            for the general public. You specialize in musculoskeletal and orthopedic rehab.

            Your goal is to provide safe, simple, and helpful physiotherapy guidance.
            You do NOT replace a licensed physiotherapist — always remind users to seek
            professional help for diagnosis and treatment.

            If a question is completely unrelated to physiotherapy or health, politely
            let the user know that you only handle physiotherapy-related questions.

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
if prompt := st.chat_input("Describe your pain or ask a physiotherapy question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat(prompt)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
