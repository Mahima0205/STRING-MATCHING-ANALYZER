import time
import matplotlib.pyplot as plt
import streamlit as st
from algorithms import kmp_search, boyer_moore_search

# --- Page Configuration ---
st.set_page_config(
    page_title="DAA String Matching Analyzer",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .highlight {
        background-color: #ffeb3b;
        padding: 2px 4px;
        border-radius: 4px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.title("🔎 String Matching Algorithm Analyzer")
st.markdown("##### **Design and Analysis of Algorithms (DAA) Mini Project**")
st.markdown(
    "A comparative web interface evaluating **KMP (Knuth-Morris-Pratt)** and "
    "**Boyer–Moore (Bad-Character Heuristic)** algorithms across character comparisons and execution times."
)
st.markdown("---")

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Configuration & Inputs")

# Presets for quick testing
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

text = st.sidebar.text_area("Enter the text (Haystack)", value=default_text, height=140)
pattern = st.sidebar.text_input("Enter pattern to search", value=default_pattern)

run_button = st.sidebar.button("🚀 Run Comparison", type="primary", use_container_width=True)

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
        st.subheader("📊 Execution Results")
        col1, col2 = st.columns(2, gap="medium")

        with col1:
            with st.container(border=True):
                st.markdown("### 🔵 KMP Algorithm")
                st.metric("Matches Found", len(kmp_positions))
                st.markdown(f"**Match Indices (0-based):** `{kmp_positions if kmp_positions else 'None'}`")
                st.markdown(f"**Character Comparisons:** `{kmp_comparisons:,}`")
                st.markdown(f"**Execution Time:** `{kmp_time:.4f} ms`")

        with col2:
            with st.container(border=True):
                st.markdown("### 🟢 Boyer–Moore Algorithm")
                st.metric("Matches Found", len(bm_positions))
                st.markdown(f"**Match Indices (0-based):** `{bm_positions if bm_positions else 'None'}`")
                st.markdown(f"**Character Comparisons:** `{bm_comparisons:,}`")
                st.markdown(f"**Execution Time:** `{bm_time:.4f} ms`")

        # Validation Check
        if kmp_positions == bm_positions:
            st.success("✨ Verification Passed: Both algorithms successfully returned identical match positions.")
        else:
            st.error("⚠️ Discrepancy detected between algorithm outputs.")

        # --- Visual Highlights of Matches ---
        if kmp_positions:
            with st.expander("🔍 View Matches Highlighted in Text"):
                highlighted_text = ""
                last_idx = 0
                for pos in kmp_positions:
                    highlighted_text += text[last_idx:pos] + f"<span class='highlight'>{text[pos:pos+len(pattern)]}</span>"
                    last_idx = pos + len(pattern)
                highlighted_text += text[last_idx:]
                st.markdown(f"<p style='font-size: 1.1rem; line-height: 1.6;'>{highlighted_text}</p>", unsafe_allow_html=True)

        # --- Performance Charts ---
        st.markdown("---")
        st.subheader("📈 Performance Comparison Charts")
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
        labels = ["KMP", "Boyer–Moore"]
        colors = ['#4C72B0', '#55A868']

        # Comparisons Bar Chart
        bars1 = axes[0].bar(labels, [kmp_comparisons, bm_comparisons], color=colors, width=0.5)
        axes[0].set_title("Character Comparisons (Lower is Better)", fontsize=11, fontweight='bold')
        axes[0].set_ylabel("Number of Comparisons")
        axes[0].grid(axis='y', linestyle='--', alpha=0.5)
        for bar in bars1:
            yval = bar.get_height()
            axes[0].text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:,}', ha='center', va='bottom', fontsize=10)

        # Execution Time Bar Chart
        bars2 = axes[1].bar(labels, [kmp_time, bm_time], color=colors, width=0.5)
        axes[1].set_title("Execution Time (Lower is Better)", fontsize=11, fontweight='bold')
        axes[1].set_ylabel("Time (Milliseconds)")
        axes[1].grid(axis='y', linestyle='--', alpha=0.5)
        for bar in bars2:
            yval = bar.get_height()
            axes[1].text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.4f} ms', ha='center', va='bottom', fontsize=10)

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

else:
    st.info("👈 Adjust your text and pattern in the sidebar, then click **Run Comparison** to begin.")

# --- Footer Notes ---
st.markdown("---")
with st.expander("📚 Algorithm & Complexity Quick Reference"):
    st.markdown(
        """
        - **KMP Algorithm:** Preprocesses the pattern to build an LPS (Longest Prefix Suffix) table. It avoids redundant re-scans of characters, giving a strict time complexity of **O(n + m)**.
        - **Boyer–Moore Algorithm:** Scans the pattern from right-to-left and uses the **Bad-Character Heuristic** to skip large windows of text instantly, performing exceptionally well on larger alphabets and long patterns.
        - `n` = length of text | `m` = length of pattern.
        """
    )