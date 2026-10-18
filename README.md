# DAA Mini Project: KMP vs. Boyer–Moore

## Files
- `app.py`: Streamlit user interface and performance comparison.
- `algorithms.py`: KMP and Boyer–Moore algorithm implementations.
- `requirements.txt`: Required Python packages.

## Run on Windows
1. Install Python 3.10 or newer from https://www.python.org/downloads/ if needed.
2. Open this folder in VS Code.
3. Open Terminal → New Terminal.
4. (Optional but recommended) Create a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt terminal and run:
   ```bat
   .venv\Scripts\activate.bat
   ```
5. Install packages:
   ```bash
   python -m pip install -r requirements.txt
   ```
6. Start the app:
   ```bash
   python -m streamlit run app.py
   ```
7. Streamlit will open the app in your browser. If it does not, open the local URL printed in the terminal (usually http://localhost:8501).

## Project demo
- Enter a paragraph and a pattern, such as `algorithms`.
- Click **Run comparison**.
- Compare match positions, character comparisons, and measured runtime.

## DAA concepts to explain
- String matching problem
- KMP and the LPS (Longest Prefix Suffix) array
- Boyer–Moore bad-character heuristic
- Time and space complexity
- Experimental comparison and why timing varies

## Complexity
Let `n` be text length and `m` be pattern length:
- KMP: O(n + m) time and O(m) auxiliary space.
- This Boyer–Moore version uses the bad-character heuristic only; its worst-case time can be O(nm), with O(k) space for the last-occurrence table, where k is the number of distinct pattern characters.

Note: This is an educational starter project. Test it with your lab's required compiler/language and format before submission.
