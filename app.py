import streamlit as st
import time

# Page configuration
st.set_page_config(
    page_title="DSA Visualizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Glassmorphism & Minimalist UI Styling
st.markdown("""
    <style>
    /* Dark Theme Setup */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Sidebar Styling */
    div[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }

    /* Cards & Containers */
    .metric-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    /* Custom Array Visualization Container */
    .viz-container {
        display: flex;
        align-items: flex-end;
        justify-content: center;
        gap: 8px;
        height: 220px;
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 1.5rem 1rem;
        margin: 1rem 0;
    }

    /* Array Bar Base */
    .viz-bar {
        width: 38px;
        border-radius: 4px 4px 0 0;
        display: flex;
        align-items: flex-end;
        justify-content: center;
        padding-bottom: 6px;
        font-weight: 600;
        font-size: 0.85rem;
        color: #0d1117;
        transition: height 0.3s ease, background-color 0.3s ease;
    }

    /* Bar Color States */
    .bar-default { background-color: #38bdf8; }
    .bar-compare { background-color: #facc15; }
    .bar-swap { background-color: #f87171; }
    .bar-sorted { background-color: #4ade80; }

    /* Node Box for Searching */
    .node-box {
        width: 48px;
        height: 48px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1rem;
        border: 2px solid #30363d;
        background: #0d1117;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.markdown("### ⚡ **DSA Visualizer**")
st.sidebar.caption("Interactive State Visualizer")

selected_algo = st.sidebar.radio(
    "Select Algorithm",
    ["Bubble Sort", "Binary Search", "BFS Shortest Path"],
    index=0
)

st.sidebar.divider()
delay = st.sidebar.slider("⏱️ Animation Delay (s)", 0.1, 1.5, 0.4, step=0.1)

# Helper function to render modern bar graphs
def render_bars(arr, highlights=[], swaps=[], sorted_idx=None):
    max_val = max(arr) if arr else 1
    bars_html = '<div class="viz-container">'
    
    for idx, val in enumerate(arr):
        height = max(15, int((val / max_val) * 160))
        
        # Color coding states
        bar_class = "bar-default"
        if idx in swaps:
            bar_class = "bar-swap"
        elif idx in highlights:
            bar_class = "bar-compare"
        elif sorted_idx is not None and idx >= sorted_idx:
            bar_class = "bar-sorted"
            
        bars_html += f'<div class="viz-bar {bar_class}" style="height: {height}px;">{val}</div>'
    
    bars_html += '</div>'
    return bars_html

# -----------------------------------------------------------------------------
# ALGORITHM 1: BUBBLE SORT
# -----------------------------------------------------------------------------
if selected_algo == "Bubble Sort":
    st.title("Bubble Sort")
    st.caption("Repeatedly steps through the array, compares adjacent elements, and swaps them if out of order.")

    col1, col2 = st.columns([3, 1])
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
                    # Highlight items being compared
                    chart_box.markdown(render_bars(arr, highlights=[j, j+1], sorted_idx=n-i), unsafe_allow_html=True)
                    status_box.info(f"Comparing index `{j}` (`{arr[j]}`) and `{j+1}` (`{arr[j+1]}`)")
                    time.sleep(delay)

                    if arr[j] > arr[j + 1]:
                        # Swap highlight
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
                        chart_box.markdown(render_bars(arr, swaps=[j, j+1], sorted_idx=n-i), unsafe_allow_html=True)
                        status_box.warning(f"Swapping `{arr[j+1]}` and `{arr[j]}`")
                        time.sleep(delay)

            # Final state - all sorted
            chart_box.markdown(render_bars(arr, sorted_idx=0), unsafe_allow_html=True)
            status_box.success("🎉 Sorting complete!")

# -----------------------------------------------------------------------------
# ALGORITHM 2: BINARY SEARCH
# -----------------------------------------------------------------------------
elif selected_algo == "Binary Search":
    st.title("Binary Search")
    st.caption("Efficient search algorithm that halves the search space on every iteration.")

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
        status_box = st.empty()
        display_box = st.empty()
        
        # Initial draw
        display_box.write(f"Array: `{arr}`")

        if st.button("Start Search", type="primary"):
            low, high = 0, len(arr) - 1
            found = False

            while low <= high:
                mid = (low + high) // 2
                display_box.markdown(
                    f"**Low:** `{low}` (`{arr[low]}`) | "
                    f"**Mid:** `{mid}` (`{arr[mid]}`) | "
                    f"**High:** `{high}` (`{arr[high]}`)"
                )

                if arr[mid] == target:
                    status_box.success(f"🎯 Target `{target}` found at index `{mid}`!")
                    found = True
                    break
                elif arr[mid] < target:
                    status_box.info(f"`{arr[mid]}` < `{target}` → Target lies in the right half.")
                    low = mid + 1
                else:
                    status_box.info(f"`{arr[mid]}` > `{target}` → Target lies in the left half.")
                    high = mid - 1

                time.sleep(delay)

            if not found:
                status_box.error(f"Target `{target}` not found in array.")

# -----------------------------------------------------------------------------
# ALGORITHM 3: BFS TRAVERSAL
# -----------------------------------------------------------------------------
elif selected_algo == "BFS Shortest Path":
    st.title("BFS Shortest Path")
    st.caption("Breadth-First Search finds the shortest path between two nodes in an unweighted graph.")

    default_graph = '{\n  "A": ["B", "C"],\n  "B": ["A", "D", "E"],\n  "C": ["A", "F"],\n  "D": ["B"],\n  "E": ["B", "F"],\n  "F": ["C", "E"]\n}'
    graph_input = st.text_area("Adjacency List (JSON):", value=default_graph, height=160)
    
    col1, col2 = st.columns(2)
    with col1:
        start_node = st.text_input("Start Node:", value="A")
    with col2:
        goal_node = st.text_input("Goal Node:", value="F")

    if st.button("Explore BFS Path", type="primary"):
        import json
        try:
            graph = json.loads(graph_input)
            queue = [[start_node]]
            visited = set()
            status_box = st.empty()
            found = False

            while queue:
                path = queue.pop(0)
                node = path[-1]

                status_box.info(f"🔍 Exploring path: **{' ➔ '.join(path)}** | Current node: `{node}`")
                time.sleep(delay)

                if node == goal_node:
                    status_box.success(f"🏆 Shortest path found: **{' ➔ '.join(path)}**")
                    found = True
                    break

                if node not in visited:
                    visited.add(node)
                    for neighbor in graph.get(node, []):
                        if neighbor not in path:
                            queue.append(path + [neighbor])

            if not found:
                status_box.error("No path exists between start and target nodes.")

        except json.JSONDecodeError:
            st.error("Invalid JSON format.")