import streamlit as st
import smtplib as s
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

st.set_page_config(
    page_title="MailSender",
    page_icon="logo.png",
    menu_items={
        "About":"""Streamline your communication with our intuitive email sending platform. Whether you're reaching out to clients, colleagues, or friends, our user-friendly interface lets you effortlessly compose and send emails to multiple recipients at once."""
    }
)

st.markdown("## :orange[Instant Attachments, Seamless Sending!]")

st.write("<img src='https://plus.unsplash.com/premium_photo-1682309526815-efe5d6225117?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8ZW1haWx8ZW58MHx8MHx8fDA%3D' width='300' height='250' style='border-radius:7px;'><br>",unsafe_allow_html=True)

gmail=st.text_input(label="Enter Your Email",help="please enter your email address")
password=st.text_input(label="Enter Your App Password",type="password")

with st.expander("How To Get App Password?"):

    st.write("""<h6>1. Enable Two-Factor Authentication (2FA):</h6>
                <ul>
                    <li>Go to myaccount.google.com.</li>
                    <li>Under Security, (on) the 2-Step Verification.</li>
                </ul>
                <h6>2. Use the Search Box:</h6>
                <ul>
                    <li>At the top of the page, use the search box and type "App passwords".</li>
                </ul>
                <h6>3. Select App Passwords:</h6>
                <ul>
                    <li>Click on the search result for "App passwords".</li>
                </ul> 
                <h6>4. Generate App Password:</h6>
                <ul>
                    <li>Now it will ask you to create a App.</li>
                    <li>Create it and name it anything you want.</li>
                </ul>
                <h6>5. Use the Password:</h6>
                <ul>
                    <li>Copy the password and paste it inside the above App Password.</li>
                </ul>
             """,unsafe_allow_html=True)
    
mailto=st.text_input(label="Enter Recipient's Email",help="please enter receiver email address")

total_mail=[]
for i in mailto.split(","):
    total_mail.append(i.strip())

with st.expander("How To Send Email To Multiple Account?"):
    st.write("""
             <ul>
                <li>If you want to send email to single account then write e.g abc@gmail.com</li>
                <li>If you want to send email to multiple account then separate it with comma e.g abc@gmail.com, xyz@gmail.com</li>
             </ul>
             """,unsafe_allow_html=True)

subject=st.text_input(label="Enter Email Subject")
message=st.text_input(label="Enter Email Message")
attachments=st.file_uploader(label="Add Attachments",accept_multiple_files=True)

mailServer = s.SMTP('smtp.gmail.com' , 587)
msg = MIMEMultipart()

# Attaching from,to,subject and message
msg['From'] = gmail
msg['To'] = ", ".join(total_mail)
msg['Subject'] = subject
msg.attach(MIMEText(message, 'plain'))

# Attaching File 
if attachments:
    for attachment in attachments:
        filename = attachment.name
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {filename}")
        msg.attach(part)

send=st.button("Send")
if send:
    try:
        mailServer.starttls()
        mailServer.login(gmail,password)
        mailServer.sendmail(gmail,total_mail,msg.as_string())
        mailServer.quit()
        st.success("Email Send Successfully :)")
    except:
        st.error("Incorrect App Password :(")
