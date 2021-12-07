from flask import Flask, render_template, request, redirect, url_for
import smtplib, ssl, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


@app.route("/")
def home():
    return render_template("index.html", title="Home")

@app.route("/contactinfo", methods=["POST"])
def contactinfo():
    if request.method == "POST":
        name = request.form.get("fname")
        number = request.form.get("number")
        dob = request.form.get("dob")
        message=request.form.get("message")
        email = request.form.get("email")

        # Send an email to the user with the contact info
        send_email(name, number, dob, message, email)

        return render_template("index.html", message="Thank You for contacting us. You should get an automated email soon.")

def send_email(name, number, dob, message, email):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "noreply.uhf@gmail.com"  # Enter your address
    receiver_email = email # Enter receiver address
    password = os.getenv("PASSWORD")

    message = MIMEMultipart("alternative")
    message["Subject"] = "Thank you for Contacting Urban Healing formulla"
    message["From"] = sender_email
    message["To"] = receiver_email
    message_to_mom = MIMEMultipart("alternative")
    message_to_mom["Subject"] = f"{name}: Someone tried to contact you"
    message_to_mom["From"] = sender_email
    message_to_mom["To"] = "urbanhealingformulla@gmail.com"

 
    html = f"""\
        <html>
        <body>
            <h1>Hi, {name}</h1>
            <p>
            Thank you for connecting with us!<br>
            This is an automated email to let you know that we have recieved your message.
            We will get back to you as soon as possible.<br>
            </p>
        </body>
        </html>
        """
    html_to_mom = f"""\
        <html>
        <body>
            <p>
            name: {name}<br>
            number: {number}<br>
            dob: {dob}<br>
            message: {message}<br>
            email: {email}<br>
            </p>
        </body>
        </html>
        """
    part1= MIMEText(html, "html")
    part2= MIMEText(html_to_mom, "html")
    message.attach(part1)
    message_to_mom.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        try:
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("email sent to customer")
            server.sendmail(sender_email, "urbanhealingformulla@gmail.com", message_to_mom.as_string())
            print("Email sent to mom")
        except:
            pass

if __name__ == "__main__":
    app.run(host="0.0.0.0")