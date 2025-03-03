import streamlit as st
import re
from datetime import datetime

# Function to handle chatbot responses
def chatbot_response(user_input):
    user_input = user_input.lower()

    # Greetings
    if re.search(r"\b(hello|hi|hey)\b", user_input):
        return "Hey! How's it going? 😊"
    elif re.search(r"\b(how are you|how's it going)\b", user_input):
        return "I'm just a bot, but I'm doing great! How about you? Anything exciting happening?"

    # Bot identity
    elif re.search(r"\b(your name|who are you)\b", user_input):
        return "I'm your friendly chatbot buddy! You can call me Bot. 🤖 What's up?"

    # Goodbye
    elif re.search(r"\b(bye|goodbye)\b", user_input):
        return "See you later! Don't forget to smile today! 🌟"

    # Help
    elif re.search(r"\b(help|what can you do)\b", user_input):
        return "I'm here to chat with you! We can talk about your day, the weather, or even tell jokes. What's on your mind?"

    # Time
    elif re.search(r"\b(time|what's the time)\b", user_input):
        now = datetime.now()
        return f"Sure! It's {now.strftime('%I:%M %p')}. Time flies, right? ⏰"

    # Weather
    elif re.search(r"\b(weather|how's the weather)\b", user_input):
        return "I don't have real-time weather data, but I hope it's sunny and bright where you are! ☀️ If not, maybe grab a coffee and enjoy the vibe?"

    # Jokes
    elif re.search(r"\b(tell me a joke|joke)\b", user_input):
        return "Why don't skeletons fight each other? They don't have the guts! 😄"

    # Thank you
    elif re.search(r"\b(thank you|thanks)\b", user_input):
        return "No problem at all! Always here to help. 😊 What else can I do for you?"

    # Compliments
    elif re.search(r"\b(you're awesome|you're cool)\b", user_input):
        return "Aww, thanks! You're pretty awesome yourself! 😎"

    # Hobbies
    elif re.search(r"\b(what do you like|your hobbies)\b", user_input):
        return "I love chatting with you! Besides that, I enjoy learning new things and telling jokes. What about you? What do you like to do?"

    # Food
    elif re.search(r"\b(food|what should I eat)\b", user_input):
        return "Hmm, how about pizza? 🍕 Or maybe some sushi? 🍣 Whatever you choose, make sure it's delicious!"

    # Movies
    elif re.search(r"\b(movie recommendation|watch a movie)\b", user_input):
        return "Ooh, I love movies! How about watching a comedy to lighten the mood? Or maybe an action-packed thriller? 🍿"

    # Default response
    else:
        return "Hmm, I'm not sure what you mean. Can you tell me more? Or maybe ask me something else? 😅"

# Streamlit UI
st.set_page_config(page_title="Chatbot", page_icon="🤖")
st.title("🤖 Your Personal Chatbot Buddy")

# Custom CSS for better UI
st.markdown(
    """
    <style>
    .stTextInput input {
        border-radius: 10px;
        padding: 10px;
        width: 100%;
    }
    .stButton button {
        border-radius: 10px;
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        cursor: pointer;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .chat-message {
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        max-width: 70%;
        border: 2px solid;
    }
    .user-message {
        border-color: #1E90FF; /* Blue border for user messages */
        margin-left: auto;
        margin-right: 0;
    }
    .bot-message {
        border-color: #FF4500; /* Red border for bot messages */
        margin-left: 0;
        margin-right: auto;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
st.write("### Chat History:")
chat_container = st.container()

with chat_container:
    for sender, message in st.session_state.messages:
        if sender == "You":
            st.markdown(f'<div class="chat-message user-message">🧑 You: {message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message">🤖 Bot: {message}</div>', unsafe_allow_html=True)

# Input form
with st.form(key="chat_form", clear_on_submit=True):
    # Create two columns for the input field and the button
    col1, col2 = st.columns([4, 1])

    # Input field in the first column
    with col1:
        user_input = st.text_input("You:", value="", key="temp_input", placeholder="Type a message...", label_visibility="collapsed")

    # Send button in the second column
    with col2:
        submit_button = st.form_submit_button("Send")

# Process input only when the button is pressed
if submit_button and user_input.strip():
    response = chatbot_response(user_input.strip())

    # Store messages in session state
    st.session_state.messages.append(("You", user_input.strip()))
    st.session_state.messages.append(("Bot", response))

    # Refresh UI
    st.rerun()