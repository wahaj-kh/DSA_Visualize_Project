import streamlit as st
import time
import json

st.set_page_config(
    page_title="DSA Visualizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f17;
        color: #e2e8f0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Target main content labels specifically (avoiding top bar & global overrides) */
    div[data-testid="stMainBlockContainer"] label[data-testid="stWidgetLabel"] p {
        color: #f8fafc !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }

    /* Target inputs, text areas, and number fields in the main container */
    div[data-testid="stMainBlockContainer"] .stTextInput input, 
    div[data-testid="stMainBlockContainer"] .stNumberInput input, 
    div[data-testid="stMainBlockContainer"] .stTextArea textarea {
        color: #ffffff !important;
        background-color: #1f2937 !important;
        border: 1px solid #4b5563 !important;
        border-radius: 8px !important;
    }

    div[data-testid="stMainBlockContainer"] .stTextInput input:focus, 
    div[data-testid="stMainBlockContainer"] .stNumberInput input:focus, 
    div[data-testid="stMainBlockContainer"] .stTextArea textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 1px #38bdf8 !important;
    }

    /* Target JSON / Monospace inner text inside text area specifically */
    div[data-testid="stMainBlockContainer"] textarea {
        font-family: 'Fira Code', 'Courier New', monospace !important;
        font-size: 0.95rem !important;
        color: #38bdf8 !important;
    }

    /* Sidebar explicit contrast fix */
    div[data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1f2937 !important;
    }

    div[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }

    .viz-container {
        display: flex;
        align-items: flex-end;
        justify-content: center;
        gap: 12px;
        height: 240px;
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }

    .viz-bar {
        width: 42px;
        border-radius: 6px 6px 0 0;
        display: flex;
        align-items: flex-end;
        justify-content: center;
        padding-bottom: 8px;
        font-weight: 700;
        font-size: 0.85rem;
        color: #0b0f17;
        transition: all 0.2s ease;
    }

    .bar-default { background-color: #38bdf8; }
    .bar-compare { background-color: #facc15; }
    .bar-swap { background-color: #f87171; }
    .bar-sorted { background-color: #4ade80; }

    .node-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        flex-wrap: wrap;
        min-height: 240px;
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }

    .node-card {
        width: 56px;
        height: 56px;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1rem;
        border: 2px solid #374151;
        background: #1f2937;
        color: #9ca3af;
        transition: all 0.2s ease;
    }

    .node-label {
        font-size: 0.65rem;
        font-weight: 800;
        margin-top: 2px;
        letter-spacing: 0.05em;
    }

    .node-default { border-color: #374151; background: #1f2937; color: #9ca3af; }
    .node-mid { border-color: #facc15; background: rgba(250, 204, 21, 0.15); color: #facc15; transform: scale(1.08); }
    .node-bound { border-color: #38bdf8; background: rgba(56, 189, 248, 0.15); color: #38bdf8; }
    .node-found { border-color: #4ade80; background: rgba(74, 222, 128, 0.2); color: #4ade80; transform: scale(1.1); }
    .node-active { border-color: #facc15; background: rgba(250, 204, 21, 0.15); color: #facc15; }
    .node-visited { border-color: #818cf8; background: rgba(129, 140, 248, 0.15); color: #818cf8; }
    .node-path { border-color: #4ade80; background: rgba(74, 222, 128, 0.2); color: #4ade80; transform: scale(1.08); }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("### ⚡ **DSA Visualizer**")
st.sidebar.caption("Interactive State Engine")

selected_algo = st.sidebar.radio(
    "Select Algorithm",
    ["Bubble Sort", "Binary Search", "BFS Shortest Path"],
    index=0
)

st.sidebar.divider()
delay = st.sidebar.slider("⏱️ Animation Delay (s)", 0.1, 1.5, 0.4, step=0.1)

def render_bars(arr, highlights=[], swaps=[], sorted_idx=None):
    max_val = max(arr) if arr else 1
    bars_html = ['<div class="viz-container">']
    for idx, val in enumerate(arr):
        height = max(18, int((val / max_val) * 160))
        bar_class = "bar-default"
        if idx in swaps:
            bar_class = "bar-swap"
        elif idx in highlights:
            bar_class = "bar-compare"
        elif sorted_idx is not None and idx >= sorted_idx:
            bar_class = "bar-sorted"
            
        bars_html.append(f'<div class="viz-bar {bar_class}" style="height: {height}px;">{val}</div>')
    bars_html.append('</div>')
    return "".join(bars_html)

def render_binary_nodes(arr, low=-1, mid=-1, high=-1, found=False):
    nodes_html = ['<div class="node-container">']
    for idx, val in enumerate(arr):
        node_class = "node-default"
        label = ""

        if found and idx == mid:
            node_class = "node-found"
            label = "TARGET"
        elif idx == mid:
            node_class = "node-mid"
            label = "MID"
        elif idx == low:
            node_class = "node-bound"
            label = "LOW"
        elif idx == high:
            node_class = "node-bound"
            label = "HIGH"

        nodes_html.append(f'<div class="node-card {node_class}"><span>{val}</span><span class="node-label">{label}</span></div>')
    nodes_html.append('</div>')
    return "".join(nodes_html)

def render_bfs_nodes(nodes, current=None, visited=[], path=[]):
    nodes_html = ['<div class="node-container">']
    for n in nodes:
        node_class = "node-default"
        label = ""

        if n in path:
            node_class = "node-path"
            label = "PATH"
        elif n == current:
            node_class = "node-active"
            label = "CURRENT"
        elif n in visited:
            node_class = "node-visited"
            label = "VISITED"

        nodes_html.append(f'<div class="node-card {node_class}"><span>{n}</span><span class="node-label">{label}</span></div>')
    nodes_html.append('</div>')
    return "".join(nodes_html)

if selected_algo == "Bubble Sort":
    st.title("Bubble Sort")
    st.caption("Repeatedly steps through the array, compares adjacent elements, and swaps them if out of order.")

    col1, _ = st.columns([3, 1])
    with col1:
        default_array = "45, 12, 89, 34, 67, 23, 90"
        user_input = st.text_input("Input Array (comma separated):", value=default_array)

    try:
        arr = [int(x.strip()) for x in user_input.split(",") if x.strip() != ""]
    except ValueError:
        st.error("Please enter a valid list of numbers.")
        arr = []

    if arr:
        chart_box = st.empty()
        status_box = st.empty()
        chart_box.markdown(render_bars(arr), unsafe_allow_html=True)

        if st.button("Start Visualization", type="primary"):
            n = len(arr)
            for i in range(n):
                for j in range(0, n - i - 1):
                    chart_box.markdown(render_bars(arr, highlights=[j, j+1], sorted_idx=n-i), unsafe_allow_html=True)
                    status_box.info(f"Comparing index `{j}` (`{arr[j]}`) and `{j+1}` (`{arr[j+1]}`)")
                    time.sleep(delay)

                    if arr[j] > arr[j + 1]:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
                        chart_box.markdown(render_bars(arr, swaps=[j, j+1], sorted_idx=n-i), unsafe_allow_html=True)
                        status_box.warning(f"Swapping `{arr[j+1]}` and `{arr[j]}`")
                        time.sleep(delay)

            chart_box.markdown(render_bars(arr, sorted_idx=0), unsafe_allow_html=True)
            status_box.success("🎉 Sorting complete!")

elif selected_algo == "Binary Search":
    st.title("Binary Search")
    st.caption("Halves the search space on each step by comparing target value against the middle element.")

    col1, col2 = st.columns([3, 1])
    with col1:
        user_input = st.text_input("Input Array (auto-sorted):", value="10, 23, 35, 47, 52, 68, 81, 94")
    with col2:
        target = st.number_input("Target Number:", value=52, step=1)

    try:
        arr = sorted([int(x.strip()) for x in user_input.split(",") if x.strip() != ""])
    except ValueError:
        st.error("Please enter valid numbers.")
        arr = []

    if arr:
        chart_box = st.empty()
        status_box = st.empty()
        chart_box.markdown(render_binary_nodes(arr), unsafe_allow_html=True)

        if st.button("Start Search", type="primary"):
            low, high = 0, len(arr) - 1
            found = False

            while low <= high:
                mid = (low + high) // 2
                chart_box.markdown(render_binary_nodes(arr, low, mid, high), unsafe_allow_html=True)
                
                if arr[mid] == target:
                    chart_box.markdown(render_binary_nodes(arr, low, mid, high, found=True), unsafe_allow_html=True)
                    status_box.success(f"🎯 Target `{target}` found at index `{mid}`!")
                    found = True
                    break
                elif arr[mid] < target:
                    status_box.info(f"`{arr[mid]}` < `{target}` → Searching right half.")
                    low = mid + 1
                else:
                    status_box.info(f"`{arr[mid]}` > `{target}` → Searching left half.")
                    high = mid - 1

                time.sleep(delay)

            if not found:
                status_box.error(f"Target `{target}` was not found in the array.")

elif selected_algo == "BFS Shortest Path":
    st.title("BFS Shortest Path")
    st.caption("Breadth-First Search systematically traverses graph nodes layer by layer to discover the shortest route.")

    default_graph = '{\n  "A": ["B", "C"],\n  "B": ["A", "D", "E"],\n  "C": ["A", "F"],\n  "D": ["B"],\n  "E": ["B", "F"],\n  "F": ["C", "E"]\n}'
    
    col1, col2 = st.columns([2, 1])
    with col1:
        graph_input = st.text_area("Adjacency List (JSON):", value=default_graph, height=180)
    with col2:
        start_node = st.text_input("Start Node:", value="A")
        goal_node = st.text_input("Goal Node:", value="F")

    try:
        graph = json.loads(graph_input)
        all_nodes = sorted(list(graph.keys()))
    except json.JSONDecodeError:
        st.error("Invalid JSON format.")
        graph = {}
        all_nodes = []

    if all_nodes:
        chart_box = st.empty()
        status_box = st.empty()
        chart_box.markdown(render_bfs_nodes(all_nodes), unsafe_allow_html=True)

        if st.button("Explore BFS Path", type="primary"):
            queue = [[start_node]]
            visited = set()
            found = False

            while queue:
                path = queue.pop(0)
                node = path[-1]

                chart_box.markdown(render_bfs_nodes(all_nodes, current=node, visited=list(visited)), unsafe_allow_html=True)
                status_box.info(f"🔍 Exploring path: **{' ➔ '.join(path)}** | Current Node: `{node}`")
                time.sleep(delay)

                if node == goal_node:
                    chart_box.markdown(render_bfs_nodes(all_nodes, visited=list(visited), path=path), unsafe_allow_html=True)
                    status_box.success(f"🏆 Shortest path found: **{' ➔ '.join(path)}**")
                    found = True
                    break

                if node not in visited:
                    visited.add(node)
                    for neighbor in graph.get(node, []):
                        if neighbor not in path:
                            queue.append(path + [neighbor])

            if not found:
                status_box.error(f"No path exists between `{start_node}` and `{goal_node}`.")