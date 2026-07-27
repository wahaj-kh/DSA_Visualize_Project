import streamlit as st
import time

# Page setup for a wide, minimalist layout
st.set_page_config(page_title="DSA Visualizer", layout="wide")

# Custom CSS for clean dark mode spacing
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    div[data-testid="stSidebar"] { background-color: #161b22; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# LEFT SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.title("DSA Visualizer")
st.sidebar.markdown("Select an algorithm to visualize:")

selected_algo = st.sidebar.radio(
    "Algorithms",
    ["Bubble Sort", "Binary Search", "BFS Shortest Path"],
    label_visibility="collapsed"
)

st.sidebar.divider()
delay = st.sidebar.slider("Step Delay (seconds)", 0.1, 2.0, 0.6, step=0.1)

# -----------------------------------------------------------------------------
# ALGORITHM 1: BUBBLE SORT
# -----------------------------------------------------------------------------
if selected_algo == "Bubble Sort":
    st.header("Bubble Sort Visualizer")
    st.caption("Custom data input or default example array.")

    col1, col2 = st.columns([3, 1])
    with col1:
        default_array_str = "50, 10, 40, 70, 20, 90, 30"
        user_input = st.text_input("Enter comma-separated integers:", value=default_array_str)
    
    try:
        arr = [int(x.strip()) for x in user_input.split(",") if x.strip() != ""]
    except ValueError:
        st.error("Please enter a valid list of comma-separated integers.")
        arr = []

    if arr:
        if st.button("Start Visualization", type="primary"):
            n = len(arr)
            status_box = st.empty()
            chart_box = st.empty()
            
            chart_box.bar_chart(arr)
            status_box.info("Starting Bubble Sort...")
            time.sleep(delay)

            for i in range(n):
                for j in range(0, n - i - 1):
                    status_box.warning(f"Comparing index {j} (`{arr[j]}`) and {j+1} (`{arr[j+1]}`)")
                    time.sleep(delay)

                    if arr[j] > arr[j + 1]:
                        status_box.error(f"Swapping `{arr[j]}` and `{arr[j+1]}`")
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
                        chart_box.bar_chart(arr)
                        time.sleep(delay)
                    else:
                        status_box.info(f"No swap needed (`{arr[j]}` ≤ `{arr[j+1]}`)")
                        time.sleep(delay / 2)

            status_box.success("Sorting Complete! Final array: " + str(arr))
            chart_box.bar_chart(arr)

# -----------------------------------------------------------------------------
# ALGORITHM 2: BINARY SEARCH
# -----------------------------------------------------------------------------
elif selected_algo == "Binary Search":
    st.header("Binary Search Visualizer")
    st.caption("Binary search requires a sorted array. Your input will be automatically sorted.")

    col1, col2 = st.columns([2, 1])
    with col1:
        default_array_str = "4, 10, 19, 23, 32, 56, 87"
        user_input = st.text_input("Enter array values:", value=default_array_str)
    with col2:
        target_val = st.number_input("Target value:", value=32, step=1)

    try:
        arr = sorted([int(x.strip()) for x in user_input.split(",") if x.strip() != ""])
    except ValueError:
        st.error("Please enter valid integers.")
        arr = []

    if arr:
        st.write("**Sorted Target Array:**", arr)
        
        if st.button("Start Search", type="primary"):
            low, high = 0, len(arr) - 1
            found = False
            status_box = st.empty()
            state_box = st.empty()

            while low <= high:
                mid = (low + high) // 2
                
                state_box.markdown(
                    f"**Low Index:** `{low}` ({arr[low]}) | "
                    f"**Mid Index:** `{mid}` (**{arr[mid]}**) | "
                    f"**High Index:** `{high}` ({arr[high]})"
                )
                
                if arr[mid] == target_val:
                    status_box.success(f"Target `{target_val}` found at index `{mid}`!")
                    found = True
                    break
                elif arr[mid] < target_val:
                    status_box.info(f"`{arr[mid]}` < `{target_val}` → Searching right half.")
                    low = mid + 1
                else:
                    status_box.info(f"`{arr[mid]}` > `{target_val}` → Searching left half.")
                    high = mid - 1

                time.sleep(delay)

            if not found:
                status_box.error(f"Target `{target_val}` was not found in the array.")

# -----------------------------------------------------------------------------
# ALGORITHM 3: BFS SHORTEST PATH
# -----------------------------------------------------------------------------
elif selected_algo == "BFS Shortest Path":
    st.header("BFS Graph Shortest Path Visualizer")
    
    st.markdown("##### Define Adjacency List (JSON format):")
    default_graph = '{\n  "A": ["B", "C"],\n  "B": ["A", "D", "E"],\n  "C": ["A", "F"],\n  "D": ["B"],\n  "E": ["B", "F"],\n  "F": ["C", "E"]\n}'
    
    graph_input = st.text_area("Custom Graph Structure:", value=default_graph, height=180)
    
    col1, col2 = st.columns(2)
    with col1:
        start_node = st.text_input("Start Node:", value="A")
    with col2:
        goal_node = st.text_input("Goal Node:", value="F")

    if st.button("Start BFS Exploration", type="primary"):
        import json
        try:
            graph = json.loads(graph_input)
            
            if start_node not in graph or goal_node not in graph:
                st.error("Start or Goal node is missing from the graph keys.")
            else:
                queue = [[start_node]]
                visited = set()
                status_box = st.empty()
                visited_box = st.empty()
                found = False

                while queue:
                    path = queue.pop(0)
                    node = path[-1]

                    status_box.info(f"Exploring path: **{' ➔ '.join(path)}** (Current Node: `{node}`)")
                    visited_box.write(f"**Visited Nodes:** `{', '.join(sorted(visited)) if visited else 'None'}`")
                    time.sleep(delay)

                    if node == goal_node:
                        status_box.success(f"Shortest path found: **{' ➔ '.join(path)}**")
                        found = True
                        break

                    if node not in visited:
                        visited.add(node)
                        for neighbor in graph.get(node, []):
                            if neighbor not in path:
                                queue.append(path + [neighbor])

                if not found:
                    status_box.error(f"No valid path exists between `{start_node}` and `{goal_node}`.")

        except json.JSONDecodeError:
            st.error("Invalid JSON format for graph definition.")