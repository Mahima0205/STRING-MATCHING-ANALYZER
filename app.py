import time
import matplotlib.pyplot as plt
import streamlit as st
from algorithms import kmp_search, boyer_moore_search

# --- Page Configuration ---
st.set_page_config(
    page_title="DAA String Matching Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Modern Custom CSS Styling ---
st.markdown("""
    <style>
    /* Main Background & Font */
    .stApp {
        background-color: #0e1117;
        color: #c9d1d9;
    }
    
    /* Header Styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #58a6ff, #bc8cff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    /* Custom Card Containers */
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    /* Highlight Badge */
    .highlight {
        background-color: #ffd33d;
        color: #000000;
        padding: 2px 6px;
        border-radius: 6px;
        font-weight: 700;
    }
    
    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #010409;
        border-right: 1px solid #30363d;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown('<p class="main-header">⚡ String Matching Algorithm Analyzer</p>', unsafe_allow_html=True)
st.markdown("##### **Design and Analysis of Algorithms (DAA) Mini Project • KMP vs. Boyer–Moore**")
st.markdown("---")

# --- Sidebar Controls ---
st.sidebar.markdown("### 🎛️ Control Panel")

preset_option = st.sidebar.selectbox(
    "Choose Test Preset",
    ["Custom Input", "Standard Text", "Repetitive Pattern", "Long Technical Text"]
)

if preset_option == "Standard Text":
    default_text = "Design and Analysis of Algorithms helps us study efficient solutions. String matching algorithms find a pattern inside a larger text."
    default_pattern = "algorithms"
elif preset_option == "Repetitive Pattern":
    default_text = "AABAAABAAABAAABAAABAAABAA"
    default_pattern = "AABA"
elif preset_option == "Long Technical Text":
    default_text = "Computer engineering students learn multiple data structures and algorithms such as sorting, searching, graph traversal, and dynamic programming to optimize software applications and systems."
    default_pattern = "algorithms"
else:
    default_text = "Design and Analysis of Algorithms helps us study efficient solutions. String matching algorithms find a pattern inside a larger text."
    default_pattern = "algorithms"

text = st.sidebar.text_area("📝 Enter Text (Haystack)", value=default_text, height=140)
pattern = st.sidebar.text_input("🔍 Enter Pattern to Search", value=default_pattern)

run_button = st.sidebar.button("🚀 Run Performance Analysis", type="primary", use_container_width=True)

# --- Main Logic ---
if run_button:
    if not pattern:
        st.warning("⚠️ Please enter a non-empty search pattern.")
    elif not text:
        st.warning("⚠️ Please enter target text to search through.")
    elif len(pattern) > len(text):
        st.error("❌ Pattern length cannot be greater than the text length.")
    else:
        # Run KMP
        start = time.perf_counter()
        kmp_positions, kmp_comparisons = kmp_search(text, pattern)
        kmp_time = (time.perf_counter() - start) * 1000

        # Run Boyer-Moore
        start = time.perf_counter()
        bm_positions, bm_comparisons = boyer_moore_search(text, pattern)
        bm_time = (time.perf_counter() - start) * 1000

        # --- Results Section ---
        st.markdown("### 📊 Execution Results & Metrics")
        col1, col2 = st.columns(2, gap="medium")

        with col1:
            with st.container(border=True):
                st.markdown("### 🔵 KMP Algorithm")
                st.metric("Matches Found", len(kmp_positions))
                st.markdown(f"**Match Indices:** `{kmp_positions if kmp_positions else 'None'}`")
                st.markdown(f"**Character Comparisons:** `{kmp_comparisons:,}`")
                st.markdown(f"**Execution Time:** `{kmp_time:.4f} ms`")

        with col2:
            with st.container(border=True):
                st.markdown("### 🟢 Boyer–Moore Algorithm")
                st.metric("Matches Found", len(bm_positions))
                st.markdown(f"**Match Indices:** `{bm_positions if bm_positions else 'None'}`")
                st.markdown(f"**Character Comparisons:** `{bm_comparisons:,}`")
                st.markdown(f"**Execution Time:** `{bm_time:.4f} ms`")

        # Validation Check
        if kmp_positions == bm_positions:
            st.success("✨ **Verification Passed:** Both algorithms returned identical match positions successfully.")
        else:
            st.error("⚠️ Discrepancy detected between algorithm outputs.")

        # --- Visual Highlights of Matches ---
        if kmp_positions:
            with st.expander("🔍 View Visual Match Highlights in Text", expanded=True):
                highlighted_text = ""
                last_idx = 0
                for pos in kmp_positions:
                    highlighted_text += text[last_idx:pos] + f"<span class='highlight'>{text[pos:pos+len(pattern)]}</span>"
                    last_idx = pos + len(pattern)
                highlighted_text += text[last_idx:]
                st.markdown(f"<p style='font-size: 1.15rem; line-height: 1.8; color: #e6edf3;'>{highlighted_text}</p>", unsafe_allow_html=True)

        # --- Performance Charts ---
        st.markdown("---")
        st.markdown("### 📈 Comparative Visualizations")
        
        # Dark-mode styled matplotlib chart setup
        plt.style.use('dark_background')
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
        fig.patch.set_facecolor('#0e1117')
        
        labels = ["KMP", "Boyer–Moore"]
        colors = ['#1f6feb', '#238636']

        # Comparisons Bar Chart
        axes[0].set_facecolor('#161b22')
        bars1 = axes[0].bar(labels, [kmp_comparisons, bm_comparisons], color=colors, width=0.45)
        axes[0].set_title("Character Comparisons (Lower is Better)", fontsize=11, fontweight='bold', color='#f0f6fc')
        axes[0].set_ylabel("Number of Comparisons", color='#8b949e')
        axes[0].grid(axis='y', linestyle='--', alpha=0.2)
        for bar in bars1:
            yval = bar.get_height()
            axes[0].text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:,}', ha='center', va='bottom', fontsize=10, color='white')

        # Execution Time Bar Chart
        axes[1].set_facecolor('#161b22')
        bars2 = axes[1].bar(labels, [kmp_time, bm_time], color=colors, width=0.45)
        axes[1].set_title("Execution Time (Lower is Better)", fontsize=11, fontweight='bold', color='#f0f6fc')
        axes[1].set_ylabel("Time (Milliseconds)", color='#8b949e')
        axes[1].grid(axis='y', linestyle='--', alpha=0.2)
        for bar in bars2:
            yval = bar.get_height()
            axes[1].text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.4f} ms', ha='center', va='bottom', fontsize=10, color='white')

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

else:
    st.info("👈 **Get Started:** Select a preset or customize your inputs in the sidebar, then click **Run Performance Analysis**.")

# --- Footer Notes ---
st.markdown("---")
with st.expander("📚 Algorithm & Time Complexity Deep Dive"):
    st.markdown(
        """
        - **KMP Algorithm:** Uses an LPS (Longest Prefix Suffix) preprocessing table to skip redundant checks. Guaranteed linear time complexity of **O(n + m)**.
        - **Boyer–Moore Algorithm:** Scans text from right-to-left utilizing the **Bad-Character Heuristic** to skip large blocks of text instantaneously.
        - `n` = length of the text | `m` = length of the pattern.
        """
    )
