import streamlit as st
from src.rag_pipeline import get_answer

st.set_page_config(
    page_title="E-Commerce Support Bot",
    page_icon="🛍️",
    layout="wide"
)

# Custom CSS Styling
st.markdown("""
<style>
.chat-container {
    background-color: #f5f7fa;
    padding: 20px;
    border-radius: 10px;
}
.user-message {
    background-color: #d1e7ff;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
}
.bot-message {
    background-color: #e8f5e9;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🛒 E-Commerce Customer Support Chatbot")
st.write("Get instant help on returns, refunds, warranty, shipping and more.")

# Sidebar
st.sidebar.title("📌 Help Topics")
st.sidebar.markdown("""
- Return Policy  
- Refund Policy  
- Warranty  
- Shipping  
- Cancellation  
- Payment  
- Account Security  
""")

# Chat History
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.chat_input("Ask your question here...")

if user_input:
    answer = get_answer(user_input)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", answer))

# Display chat messages
for sender, message in st.session_state.history:
    if sender == "You":
        st.markdown(f"<div class='user-message'><b>🧑 You:</b><br>{message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-message'><b>🤖 Support Bot:</b><br>{message}</div>", unsafe_allow_html=True)