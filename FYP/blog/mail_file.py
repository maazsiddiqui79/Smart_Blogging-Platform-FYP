import smtplib

# Hello
class MAIL_SENDIND():
    def __init__(self, revicers_email, indent, username=None, otp=None,**kwargs):

        self.revicers_email = revicers_email
        self.indent = indent
        self.status = 'fail'
        self.title = kwargs.get("title")
        self.slug = kwargs.get("slug")
        self.created_at = kwargs.get("doc")


        sender_mail = "maaz.irshad.siddiqui@gmail.com"
        password = "tvud sggg rdle ywll"

        # -------- BUILD MESSAGE (USING YOUR TEXT) --------
        if indent == "reset-password":
            
            message = f"""Subject: OTP for Password Reset – Smart Blogger

Dear User,

Your OTP for password reset is:

OTP: {otp}

Do not share this OTP with anyone.

Smart Blogger Security Team
"""

        elif indent == "recover-username":
            
            message = f"""Subject: Username Recovery – Smart Blogger

Dear User,

You recently requested to recover the username associated with your Smart Blogger account.

Account Details:
------------------------------
Registered Email : {revicers_email}
Username         : {username}
------------------------------

Best regards,  
Smart Blogger Support Team  
This is an automated system-generated email. Please do not reply.
"""

        elif indent == "pass-update":
            
            message = f"""Subject: Password Change Alert – Smart Blogger

Dear User,

This is a security notification to inform you that the password for your Smart Blogger account has been changed.

Account Email:
------------------------------
{revicers_email}
------------------------------

If this was not you, please reset your password immediately.

Best regards,  
Smart Blogger Security Team  
This is an automated system-generated email. Please do not reply.
"""
        elif indent == "recover-username":
            
            message = f"""Subject: Username Recovery – Smart Blogger

Dear User,

You recently requested to recover the username associated with your Smart Blogger account.

Account Details:
------------------------------
Registered Email : {revicers_email}
Username         : {username}
------------------------------

Best regards,  
Smart Blogger Support Team  
This is an automated system-generated email. Please do not reply.
"""

        elif indent == "post-notify":
            
            message = f"""Subject: New Blog Post from an Author You Follow – Smart Blogger

Dear User,

An author you follow on Smart Blogger has published a new blog post. We wanted to keep you informed so you don’t miss the latest update.

Post Details:
------------------------------
Author       : {username}
Title        : {kwargs.get("title")}
Published On : {kwargs.get("doc")}
Read Article : /blog/{kwargs.get("slug")}
------------------------------

Visit Smart Blogger to read the full article and explore more content from authors you follow.

Best regards,  
Smart Blogger Team  
This is an automated system-generated email. Please do not reply.
"""
        elif indent == "verify-email":
            
            message = f"""Subject: Verify Your Email Address – Smart Blogger

Dear User,

Thank you for creating an account on Smart Blogger. To complete your registration and secure your account, please verify your email address using the One-Time Password (OTP) below.

Verification Details:
------------------------------
Email       : {self.revicers_email}
OTP Code    : {otp}
Valid For   : 10 minutes
------------------------------

Please enter this OTP on the verification screen to activate your account.  
If you did not request this verification, you can safely ignore this email.

Best regards,  
Smart Blogger Team  
This is an automated system-generated email. Please do not reply.
"""



        else:
            # Invalid indent → safe exit
            return

        # -------- SEND MAIL (ONCE, SAFELY) --------
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
                connection.login(sender_mail, password)
                connection.sendmail(
                    sender_mail,
                    revicers_email,
                    message.encode("utf-8")
                )
            self.status = 'success'
        except Exception as e:
            print("Mail sending failed:", e)
            self.status = 'fail'
