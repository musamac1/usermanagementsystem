import streamlit as st
import pandas as pd

import requests



def local_css(file_names):
    css = ""
    for file_name in file_names:
        with open(file_name) as f:
            css += f"<style>{f.read()}</style>\n"
    st.markdown(css, unsafe_allow_html=True)

# Call the function with a list of CSS file names
local_css([ "styles.css","st.css","font-awesome.min.css"])





# Initialize user database (replace with a persistent storage solution in a real app)
if 'users' not in st.session_state:
  st.session_state['users'] = {'admin': 'admin'}
if 'user_profiles' not in st.session_state:
  st.session_state['user_profiles'] = {}
if 'user_pics' not in st.session_state:
  st.session_state['user_pics'] = {}
if 'user_links' not in st.session_state:
  st.session_state['user_links'] = {}
if 'announcements' not in st.session_state:
  st.session_state['announcements'] = []
if 'messages' not in st.session_state:
  st.session_state['messages'] = {}
if 'academic_records' not in st.session_state:
  st.session_state['academic_records'] = {}

def login():
  st.subheader("Login")
  username = st.text_input("Username")
  password = st.text_input("Password", type='password')
  if st.button("Login"):
     if username == "admin" and password == "admin":
      st.success("Logged in as admin")
      admin_view()
     elif username in st.session_state['users'] and st.session_state['users'][username] == password:
      st.success("Logged in as {}".format(username))
      st.session_state['logged_in'] = True
      st.session_state['current_user'] = username
     else:
      st.error("Invalid username or password")

def signup():
  st.subheader("Sign Up")
  new_username = st.text_input("New Username")
  new_password = st.text_input("New Password", type='password')
  new_email = st.text_input("Email")
  new_bio = st.text_area("Bio")
  uploaded_pic = st.file_uploader("Choose a profile picture", type=["jpg", "jpeg", "png"])
  if st.button("Sign Up"):
    if new_username not in st.session_state['users']:
      st.session_state['users'][new_username] = new_password
      st.session_state['user_profiles'][new_username] = {
          'email': new_email,
          'bio': new_bio
      }
      if uploaded_pic is not None:
        st.session_state['user_pics'][new_username] = uploaded_pic.read()
      st.success("Account created successfully. You can now log in.")
    else:
      st.error("Username already exists.")

def admin_view():
  st.subheader("Admin View")
  df = pd.DataFrame.from_dict(st.session_state['users'], orient='index', columns=['Password'])
  st.write("Number of users:", len(df))
  st.write(df)

  

def profile_view():
  st.subheader("Your Profile")
  st.write("Username:", st.session_state['current_user'])
  if st.session_state['current_user'] in st.session_state['user_pics']:
    
    st.image(st.session_state['user_pics'][st.session_state['current_user']], caption="Profile Picture", width=200)
  else:
    st.write("No profile picture uploaded.")
  if st.session_state['current_user'] in st.session_state['user_profiles']:
    st.write("Email:", st.session_state['user_profiles'][st.session_state['current_user']]['email'])
    st.write("Bio:", st.session_state['user_profiles'][st.session_state['current_user']]['bio'])
  

def link_management():
  st.subheader("Your Links")
  if st.session_state['current_user'] not in st.session_state['user_links']:
    st.session_state['user_links'][st.session_state['current_user']] = []

  for i, link in enumerate(st.session_state['user_links'][st.session_state['current_user']]):
    st.write(f"{i+1}. {link}")

  new_link = st.text_input("Add a new link:")
  if st.button("Add Link"):
    st.session_state['user_links'][st.session_state['current_user']].append(new_link)
    st.rerun()

def messaging():
  st.subheader("Messaging")
  recipient = st.text_input("Recipient:")
  message = st.text_area("Message:")
  if st.button("Send"):
    if recipient in st.session_state['users']:
      if recipient not in st.session_state['messages']:
        st.session_state['messages'][recipient] = []
      st.session_state['messages'][recipient].append((st.session_state['current_user'], message))
      st.success("Message sent!")
    else:
      st.error("Recipient not found.")

  st.subheader("Inbox")
  if st.session_state['current_user'] in st.session_state['messages']:
    for sender, msg in st.session_state['messages'][st.session_state['current_user']]:
      st.write(f"**From {sender}:** {msg}")
  else:
    st.write("No messages yet.")

def main():
  st.title("USER MANAGEMENT SYSTEM")

  if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

  if not st.session_state['logged_in']:
    choice = st.sidebar.radio("Select an option:", ["Login", "Sign Up"])
    if choice == "Login":
      login()
    elif choice == "Sign Up":
      signup()
  else:
    st.sidebar.title("Menu")
    if st.session_state['current_user'] == 'admin':
      menu_options = ["Admin View", "Profile", "Links", "Messages", "Logout","announcements","contact us","academic records"]
     
    else:
      menu_options = ["Profile", "Links", "Messages", "Logout","announcements","contact us","academic records"]
      choice = st.sidebar.radio("Go to", menu_options)

 
    if choice == "Profile":
      profile_view()
    elif choice == "Links":
      link_management()
    elif choice == "Messages":
      messaging()
  
    
    elif choice == "Logout":
     
      st.session_state['logged_in'] = False
      st.session_state['current_user'] = None
      st.rerun()
     
    elif choice =="announcements":
      handle_announcements()
    elif choice == "contact us":
      
      contact()
    elif choice=="academic records":
      academic_records()  
      
   
   
    # Display announcements
def handle_announcements():
  st.subheader("Announcements")
  for announcer, announcement in st.session_state['announcements']:
    st.write(f"**{announcer}:** {announcement}")  # Display announcer's name

  new_announcement = st.text_area("Make a new announcement:")
  if st.button("Announce"):
    st.session_state['announcements'].append((st.session_state['current_user'], new_announcement))  # Store announcer's name
    # Send the announcement to all users as a message
    for user in st.session_state['users']:
      if user not in st.session_state['messages']:
        st.session_state['messages'][user] = []
      st.session_state['messages'][user].append((f"Admin ({st.session_state['current_user']})", new_announcement))  # Include announcer in message
    st.experimental_rerun()
def contact():
 st.subheader("if any problem contact us")

 contact_form="""
     <form action="https://formsubmit.co/mmaqsoodulhaq@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>

    """
 st.markdown(contact_form,unsafe_allow_html=True)
def academic_records():
  st.subheader("Academic Records")
  if st.session_state['current_user'] in st.session_state['academic_records']:
    for record in st.session_state['academic_records'][st.session_state['current_user']]:
      st.write(f"- **{record['degree']}** from {record['institution']} ({record['year']})")
  else:
    st.write("No academic records added yet.")

  # Allow users to add academic records
  
  st.subheader("Add Academic Record")
  degree = st.text_input("Degree")
  institution = st.text_input("Institution")
  year = st.text_input("Year")
  if st.button("Add Record"):
    if st.session_state['current_user'] not in st.session_state['academic_records']:
      st.session_state['academic_records'][st.session_state['current_user']] = []
    st.session_state['academic_records'][st.session_state['current_user']].append({
        'degree': degree,
        'institution': institution,
        'year': year
    })
    st.rerun()


if __name__ == '__main__':
  main()

