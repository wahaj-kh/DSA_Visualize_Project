Markdown
# ⚡ DSA State Engine & Visualizer

A sleek, modern Data Structures and Algorithms (DSA) visualizer built in Python with **Streamlit**. Designed with a glassmorphic dark-mode interface and custom CSS card architecture, this application provides clear, step-by-step visual execution of foundational algorithms.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.20+-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

🔗 **Live Application:** [https://dsavisualizeproject-1.streamlit.app/](https://dsavisualizeproject-1.streamlit.app/)

---

## ✨ Features

- **Bubble Sort**: Real-time step-by-step state visualization with color-coded bar highlights for comparison, swapping, and sorted indices.
- **Binary Search**: Dynamic array visualization highlighting the `LOW`, `MID`, `HIGH`, and target states across halving search spaces.
- **BFS Shortest Path**: Graph traversal tracker tracking visited nodes, current active nodes, and final computed routes based on customized JSON adjacency lists.
- **Custom CSS Engine**: Handcrafted CSS state elements utilizing native HTML scoping for clean visual updates without external heavy frontend frameworks.
- **Interactive Controls**: Real-time adjustable execution speed/animation delay, custom user input parsing, and state status callouts.

---

## 🛠️ Tech Stack

- **Frontend / Framework**: [Streamlit](https://streamlit.io/)
- **Languages**: Python, HTML5, CSS3
- **Data Format**: JSON (Adjacency Lists)

---

## 🚀 Quickstart

### Prerequisites

Ensure you have Python 3.9 or higher installed on your system.

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/dsa-visualizer.git](https://github.com/your-username/dsa-visualizer.git)
   cd dsa-visualizer
Create and activate a virtual environment (optional but recommended):

Bash
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
Install dependencies:

Bash
pip install streamlit
Run the application:

Bash
streamlit run app.py
📂 Project Structure
Plaintext
dsa-visualizer/
├── app.py              # Main Streamlit application entry point & layout
├── README.md           # Project documentation
└── requirements.txt    # Application dependencies
🎨 Palette & Visual Tokens
State	Hex Code	Description
Primary Accent	#38bdf8	Default bars, target bounds, key highlights
Active / Mid	#facc15	Current active node / elements under comparison
Swap / Error	#f87171	Active swap operation state
Sorted / Match	#4ade80	Confirmed targets, path routes, sorted elements
Visited / Secondary	#818cf8	Visited graph nodes
📝 License
Distributed under the MIT License. See LICENSE for more information.