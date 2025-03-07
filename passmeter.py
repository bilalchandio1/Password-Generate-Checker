import re
import random
import string
import streamlit as st

# Blacklist of weak passwords
BLACKLISTED_PASSWORDS = {"password123", "12345678", "qwerty123", "letmein", "admin", "welcome"}

# Function to generate a strong password
def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(random.choice(characters) for _ in range(length))

# Function to check password strength
def check_password_strength(password):
    if password in BLACKLISTED_PASSWORDS:
        return "❌ This password is too common and easily guessed. Choose a different one.", 0
    
    score = 0
    feedback = []

    # Scoring weights
    weights = {
        "length": 2 if len(password) >= 12 else 1,
        "uppercase": 1 if re.search(r"[A-Z]", password) else 0,
        "lowercase": 1 if re.search(r"[a-z]", password) else 0,
        "digit": 1 if re.search(r"\d", password) else 0,
        "special": 2 if re.search(r"[!@#$%^&*]", password) else 0,
    }

    # Evaluate strength
    score = sum(weights.values())
    
    if weights["length"] == 1:
        feedback.append("Password should be at least 12 characters long.")
    if not weights["uppercase"]:
        feedback.append("Include at least one uppercase letter.")
    if not weights["lowercase"]:
        feedback.append("Include at least one lowercase letter.")
    if not weights["digit"]:
        feedback.append("Add at least one number (0-9).")
    if not weights["special"]:
        feedback.append("Include at least one special character (!@#$%^&*).")
    
    # Strength Rating
    if score >= 6:
        return "✅ Strong Password!", score, feedback
    elif score >= 4:
        return "⚠️ Moderate Password - Consider strengthening it.", score, feedback
    else:
        return "❌ Weak Password - Improve it using the suggestions above.", score, feedback

# Streamlit UI
def main():
    st.title("🔐 Generate_Strong_Password")
    username = st.text_input("Enter your username")
    password = st.text_input("Enter your password", type="password")
    
    if password:
        message, score, feedback = check_password_strength(password)
        st.write(message)
        if feedback:
            with st.expander("🔍 Password Suggestions"):
                for tip in feedback:
                    st.write(f"- {tip}")
    
    if st.button("Submit"):
        if username and password:
            if score >= 6:
                st.success("🎉 Password created successfully!")
            else:
                st.error("⚠️ Improve your password before signing up.")
        else:
            st.error("Please fill in all fields.")
    
    if st.button("Generate Strong Password"):
        strong_password = generate_strong_password()
        st.success(f"Suggested Password: `{strong_password}`")

if __name__ == "__main__":
    main()

    