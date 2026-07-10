import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Notes App", page_icon="📝", layout="centered")
st.title("📝 Notes App")

# ---------------------------------------------------------
# Session state to remember which action is selected
# ---------------------------------------------------------
if "action" not in st.session_state:
    st.session_state.action = None

# ---------------------------------------------------------
# 5 buttons for the 5 endpoints
# ---------------------------------------------------------
st.subheader("Choose an action")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("📋 Show All"):
        st.session_state.action = "all"
with col2:
    if st.button("🔍 Show by ID"):
        st.session_state.action = "get"
with col3:
    if st.button("➕ Add Note"):
        st.session_state.action = "add"
with col4:
    if st.button("✏️ Update Note"):
        st.session_state.action = "update"
with col5:
    if st.button("🗑️ Delete Note"):
        st.session_state.action = "delete"

st.divider()

# ---------------------------------------------------------
# Modular note display helpers
# ---------------------------------------------------------
def render_note_card(note: dict, expanded: bool = True):
    """Render a single note as a clean, self-contained card."""
    with st.container(border=True):
        header_col, badge_col = st.columns([5, 1])
        with header_col:
            st.markdown(f"#### {note['name']}")
        with badge_col:
            st.markdown(
                f"<div style='text-align:right;color:gray;font-size:0.85rem;"
                f"padding-top:8px;'>#{note['id']}</div>",
                unsafe_allow_html=True,
            )
        with st.expander("Content", expanded=expanded):
            st.text(note["content"])


def render_notes(data):
    """Accepts either a single note dict or a list of notes and renders them."""
    notes = data if isinstance(data, list) else [data]

    if not notes:
        st.info("No notes found.")
        return

    st.caption(f"{len(notes)} note{'s' if len(notes) != 1 else ''} found")
    for note in notes:
        render_note_card(note, expanded=(len(notes) == 1))


# Backwards-compatible alias used throughout the action handlers below
show_notes = render_notes

# ---------------------------------------------------------
# 1. Show all notes
# ---------------------------------------------------------
if st.session_state.action == "all":
    st.subheader("All Notes")
    try:
        response = requests.get(f"{BASE_URL}/notes")
        if response.status_code == 200:
            show_notes(response.json())
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend. Make sure it's running on http://127.0.0.1:8000")

# ---------------------------------------------------------
# 2. Show note by ID
# ---------------------------------------------------------
elif st.session_state.action == "get":
    st.subheader("Show Note by ID")
    with st.form("get_note_form"):
        note_id = st.number_input("Note ID", min_value=1, step=1)
        submitted = st.form_submit_button("Fetch Note")

    if submitted:
        try:
            response = requests.get(f"{BASE_URL}/notes/{note_id}")
            if response.status_code == 200:
                show_notes(response.json())
            elif response.status_code == 404:
                st.warning("Note not found.")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend. Make sure it's running on http://127.0.0.1:8000")

# ---------------------------------------------------------
# 3. Add a note
# ---------------------------------------------------------
elif st.session_state.action == "add":
    st.subheader("Add a New Note")
    with st.form("add_note_form"):
        note_id = st.number_input("Note ID", min_value=1, step=1)
        name = st.text_input("Name")
        content = st.text_area("Content")
        submitted = st.form_submit_button("Add Note")

    if submitted:
        if not name or not content:
            st.warning("Please fill in both name and content.")
        else:
            payload = {"id": int(note_id), "name": name, "content": content}
            try:
                response = requests.post(f"{BASE_URL}/notes", json=payload)
                if response.status_code == 200:
                    st.success(response.json())
                elif response.status_code == 409:
                    st.warning("A note with this ID already exists.")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend. Make sure it's running on http://127.0.0.1:8000")

# ---------------------------------------------------------
# 4. Update a note
# ---------------------------------------------------------
elif st.session_state.action == "update":
    st.subheader("Update an Existing Note")
    with st.form("update_note_form"):
        note_id = st.number_input("Note ID", min_value=1, step=1)
        name = st.text_input("New Name")
        content = st.text_area("New Content")
        submitted = st.form_submit_button("Update Note")

    if submitted:
        if not name or not content:
            st.warning("Please fill in both name and content.")
        else:
            payload = {"id": int(note_id), "name": name, "content": content}
            try:
                response = requests.put(f"{BASE_URL}/notes/{note_id}", json=payload)
                if response.status_code == 200:
                    st.success(response.json())
                elif response.status_code == 404:
                    st.warning("Note not found.")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend. Make sure it's running on http://127.0.0.1:8000")

# ---------------------------------------------------------
# 5. Delete a note
# ---------------------------------------------------------
elif st.session_state.action == "delete":
    st.subheader("Delete a Note")
    with st.form("delete_note_form"):
        note_id = st.number_input("Note ID", min_value=1, step=1)
        submitted = st.form_submit_button("Delete Note", type="primary")

    if submitted:
        try:
            response = requests.delete(f"{BASE_URL}/notes/{note_id}")
            if response.status_code == 200:
                st.success(response.json())
            elif response.status_code == 404:
                st.warning("Note not found.")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend. Make sure it's running on http://127.0.0.1:8000")

else:
    st.info("👆 Pick an action above to get started.")