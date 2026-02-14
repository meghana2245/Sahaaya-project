import streamlit as st
from datetime import datetime
from style import apply_style

apply_style()

st.title("🌈 Recovery Stories & Reviews")

# ---------------------------------
# Initialize Storage
# ---------------------------------
if "recovery_stories" not in st.session_state:
    st.session_state.recovery_stories = []

if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False

st.markdown("---")

# ---------------------------------
# ADMIN LOGIN TOGGLE
# ---------------------------------
with st.expander("🔐 Admin Access"):
    password = st.text_input("Enter Admin Password", type="password")

    if password == "admin123":   # Change password here
        st.session_state.admin_mode = True
        st.success("Admin mode activated")
    elif password != "":
        st.error("Incorrect password")

# ---------------------------------
# SUBMIT STORY FORM
# ---------------------------------
st.subheader("📝 Share Your Recovery Story")

with st.form("recovery_form", clear_on_submit=True):

    name = st.text_input("👤 Your Name (or Anonymous)")
    age = st.number_input("🎂 Your Age", 10, 100)
    rating = st.slider("⭐ Rate your experience", 1, 5)
    story = st.text_area("📝 Share your story", height=150)

    submit = st.form_submit_button("Submit Story")

    if submit:
        if story.strip() == "":
            st.error("Please write your story.")
        else:
            st.session_state.recovery_stories.append({
                "Name": name if name.strip() else "Anonymous",
                "Age": age,
                "Rating": rating,
                "Story": story,
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Approved": False,
                "Helpful": 0,
                "Comments": []
            })

            st.success("💛 Story submitted! Waiting for admin approval.")

st.markdown("---")

# ---------------------------------
# ADMIN APPROVAL SECTION
# ---------------------------------
if st.session_state.admin_mode:
    st.subheader("🛠 Admin Panel – Approve Stories")

    for story in st.session_state.recovery_stories:
        if not story["Approved"]:
            st.markdown(f"""
            **{story['Name']} (Age {story['Age']})**
            ⭐ {'⭐' * story['Rating']}
            📝 {story['Story']}
            """)

            if st.button(f"Approve Story from {story['Name']}"):
                story["Approved"] = True
                st.success("Story Approved ✅")

            st.markdown("---")

st.markdown("---")

# ---------------------------------
# PUBLIC STORIES DISPLAY
# ---------------------------------
st.subheader("📚 Community Recovery Stories")

approved_stories = [
    s for s in st.session_state.recovery_stories if s["Approved"]
]

if not approved_stories:
    st.info("No approved stories yet. Check back soon 🌟")
else:
    for i, story in enumerate(reversed(approved_stories)):

        st.markdown(f"""
        ### 🌟 {story['Name']} (Age {story['Age']})
        ⭐ {'⭐' * story['Rating']}
        📝 {story['Story']}
        🕒 {story['Time']}
        """)

        # Helpful Button
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button(f"❤️ Helpful ({story['Helpful']})", key=f"helpful_{i}"):
                story["Helpful"] += 1
                st.rerun()

        # Comments Section
        st.markdown("💬 **Comments:**")

        if story["Comments"]:
            for comment in story["Comments"]:
                st.markdown(f"- {comment}")
        else:
            st.write("No comments yet.")

        # Add Comment
        new_comment = st.text_input(
            "Add a comment",
            key=f"comment_input_{i}"
        )

        if st.button("Post Comment", key=f"post_comment_{i}"):
            if new_comment.strip():
                story["Comments"].append(new_comment)
                st.rerun()

        st.markdown("---")
import streamlit as st
from datetime import datetime
from database import get_connection, create_tables
from style import apply_style

apply_style()
create_tables()

st.title("🌈 Recovery Stories & Reviews")

st.markdown("---")

# ---------------------------------
# ADMIN LOGIN TOGGLE
# ---------------------------------
admin_mode = False

with st.expander("🔐 Admin Access"):
    password = st.text_input("Enter Admin Password", type="password")

    if password == "admin123":
        admin_mode = True
        st.success("Admin mode activated")
    elif password != "":
        st.error("Incorrect password")

# ---------------------------------
# SUBMIT STORY FORM
# ---------------------------------
st.subheader("📝 Share Your Recovery Story")

with st.form("recovery_form", clear_on_submit=True):

    name = st.text_input("👤 Your Name (or Anonymous)")
    age = st.number_input("🎂 Your Age", 10, 100)
    rating = st.slider("⭐ Rate your experience", 1, 5)
    story = st.text_area("📝 Share your story", height=150)

    submit = st.form_submit_button("Submit Story")

    if submit:
        if story.strip() == "":
            st.error("Please write your story.")
        else:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO recovery_stories
                (name, age, rating, story, time, approved, helpful)
                VALUES (?, ?, ?, ?, ?, 0, 0)
            """, (
                name if name.strip() else "Anonymous",
                age,
                rating,
                story,
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ))

            conn.commit()
            conn.close()

            st.success("💛 Story submitted! Waiting for admin approval.")

st.markdown("---")

conn = get_connection()
cursor = conn.cursor()

# ---------------------------------
# ADMIN APPROVAL SECTION
# ---------------------------------
if admin_mode:
    st.subheader("🛠 Admin Panel – Approve Stories")

    cursor.execute("SELECT * FROM recovery_stories WHERE approved = 0")
    pending = cursor.fetchall()

    for story in pending:
        story_id = story[0]

        st.markdown(f"""
        **{story[1]} (Age {story[2]})**
        ⭐ {'⭐' * story[3]}
        📝 {story[4]}
        """)

        if st.button(f"Approve Story from {story[1]}", key=f"approve_{story_id}"):
            cursor.execute(
                "UPDATE recovery_stories SET approved = 1 WHERE id = ?",
                (story_id,)
            )
            conn.commit()
            st.success("Story Approved ✅")
            st.rerun()

        st.markdown("---")

st.markdown("---")

# ---------------------------------
# PUBLIC STORIES DISPLAY
# ---------------------------------
st.subheader("📚 Community Recovery Stories")

cursor.execute("SELECT * FROM recovery_stories WHERE approved = 1 ORDER BY id DESC")
approved_stories = cursor.fetchall()

if not approved_stories:
    st.info("No approved stories yet. Check back soon 🌟")
else:
    for story in approved_stories:

        story_id = story[0]

        st.markdown(f"""
        ### 🌟 {story[1]} (Age {story[2]})
        ⭐ {'⭐' * story[3]}
        📝 {story[4]}
        🕒 {story[5]}
        """)

        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button(f"❤️ Helpful ({story[7]})", key=f"help_{story_id}"):
                cursor.execute(
                    "UPDATE recovery_stories SET helpful = helpful + 1 WHERE id = ?",
                    (story_id,)
                )
                conn.commit()
                st.rerun()

        # Comments
        st.markdown("💬 **Comments:**")

        cursor.execute(
            "SELECT comment FROM comments WHERE story_id = ?",
            (story_id,)
        )
        comments = cursor.fetchall()

        if comments:
            for comment in comments:
                st.markdown(f"- {comment[0]}")
        else:
            st.write("No comments yet.")

        new_comment = st.text_input(
            "Add a comment",
            key=f"comment_{story_id}"
        )

        if st.button("Post Comment", key=f"post_{story_id}"):
            if new_comment.strip():
                cursor.execute(
                    "INSERT INTO comments (story_id, comment) VALUES (?, ?)",
                    (story_id, new_comment)
                )
                conn.commit()
                st.rerun()

        st.markdown("---")

conn.close()
