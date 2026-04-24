import streamlit as st
from rag_backend import build_chain
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

st.set_page_config(
    page_title="TubeAsk — Video Intelligence",
    page_icon="▶",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css():
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

with st.sidebar:

    st.markdown("""
    <div class="sb-brand">
        <div class="sb-brand-row">
            <div class="sb-brand-icon">▶</div>
            <span class="sb-brand-name">TUBE<span>ASK</span></span>
        </div>
        <div class="sb-brand-sub">VIDEO INTELLIGENCE SYSTEM v2.0</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section-label">// SOURCE VIDEO</div>', unsafe_allow_html=True)

    video_id = st.text_input("Video ID", placeholder="osKyvYJ3PRM", label_visibility="collapsed")

    st.markdown('<div class="sb-spacer"></div>', unsafe_allow_html=True)

    load_btn = st.button("▶  LOAD & ANALYZE", type="primary")

    if load_btn and video_id:
        with st.spinner("[ FETCHING TRANSCRIPT... ]"):
            try:
                chain = build_chain(video_id)
                st.session_state["chain"]    = chain
                st.session_state["video_id"] = video_id
                st.session_state["messages"] = []
                st.success("[ READY ] Video indexed successfully.")
            except TranscriptsDisabled:
                st.error("[ ERR ] Captions disabled for this video.")
            except NoTranscriptFound:
                st.error("[ ERR ] No English transcript found.")
            except Exception as e:
                st.error(f"[ ERR ] {e}")

    if "video_id" in st.session_state:
        st.markdown(f"""
        <div class="sb-video-card">
            <div class="sb-video-live">
                <span class="sb-video-live-dot">●</span> LIVE
            </div>
            <div class="sb-video-id">ID: <span>{st.session_state['video_id']}</span></div>
        </div>
        """, unsafe_allow_html=True)
        st.video(f"https://www.youtube.com/watch?v={st.session_state['video_id']}")

    st.markdown("""
    <div class="sb-tips">
        <div class="sb-tips-text">
            › Paste the 11-char video ID<br>
            › Works with English captions<br>
            › Powered by Gemini + FAISS RAG
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <div class="main-header-left">
        <div class="main-header-title">VIDEO <span>Q&A</span> TERMINAL</div>
        <div class="main-header-sub">RETRIEVAL-AUGMENTED GENERATION · GEMINI 2.5 FLASH · FAISS INDEX</div>
    </div>
    <div class="main-header-right">
        <div class="main-header-status">
            <span class="main-header-dot"></span>
            SYSTEM ONLINE
        </div>
        <div class="main-header-pipeline">RAG PIPELINE ACTIVE</div>
    </div>
</div>
""", unsafe_allow_html=True)

if "chain" not in st.session_state:

    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-corner-bl"></div>
        <div class="empty-state-corner-br"></div>
        <div class="empty-state-icon">▶</div>
        <div class="empty-state-title">NO VIDEO LOADED</div>
        <div class="empty-state-desc">
            Enter a YouTube Video ID in the sidebar<br>to initialize the RAG pipeline.
        </div>
        <div class="empty-state-chips">
            <span class="empty-state-chip">Summarize the video</span>
            <span class="empty-state-chip">Main topics covered?</span>
            <span class="empty-state-chip">Explain concept X</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    messages = st.session_state.get("messages", [])

    if not messages:
        st.markdown("""
        <div class="sys-banner">
            [ SYS ] Transcript indexed. Vector store ready. Ask your first question below.
        </div>
        """, unsafe_allow_html=True)

    for msg in messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-row user">
                <div class="msg-avatar user">YOU</div>
                <div class="msg-bubble user">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.container():
                st.markdown("""
                <div class="msg-row assistant">
                    <div class="msg-avatar assistant">▶</div>
                    <div class="msg-bubble assistant">
                """, unsafe_allow_html=True)
                st.markdown(msg["content"])  
                st.markdown("</div></div>", unsafe_allow_html=True)

    if question := st.chat_input("Query the video..."):
        st.session_state["messages"].append({"role": "user", "content": question})

        st.markdown(f"""
        <div class="msg-row user">
            <div class="msg-avatar user">YOU</div>
            <div class="msg-bubble user">{question}</div>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("[ QUERYING RAG PIPELINE... ]"):
            answer = st.session_state["chain"].invoke(question)

        with st.container():
            st.markdown("""
            <div class="msg-row assistant">
                <div class="msg-avatar assistant">▶</div>
                <div class="msg-bubble assistant">
            """, unsafe_allow_html=True)
            st.markdown(answer)
            st.markdown("</div></div>", unsafe_allow_html=True)

        st.session_state["messages"].append({"role": "assistant", "content": answer})