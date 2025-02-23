import streamlit as st

st.header("📧: Get In Touch Wth Me!")

contact_form = """
<form action="https://formsubmit.co/mazzather@gmail.com" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your Name" required>
     <input type="hidden" name="_autoresponse" value="Thank-you so much for message , i'll be connect to you as soon as possible ! ">
     <input type="hidden" name="_template" value="table">
     <input type="email" name="email" placeholder="Your Email" required>
     <textarea name='message' placeholder='your message here'></textarea>
     <button type="submit">Send</button>
</form>
"""

st.markdown(contact_form , unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")