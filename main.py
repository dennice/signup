import webapp2
import re


form="""<form method="post">
        <h1>Signup</h1>
        <label>
            Username <input type="text" name="username" value="%(username)s">
        </label><div style="color: red">%(error_username)s</div>
        <br>
        <label>
            Password <input type="password" name="password" value="%(password)s">
        </label><div style="color: red">%(error_password)s</div>
        <br>
        <label>
            Verify Password <input type="password" name="verify" value="%(verify)s">
        </label><div style="color: red">%(error_verify)s</div>
        <br>
        <label>
            Email (optional) <input type="text" name="email" value="%(email)s">
        </label><div style="color: red">%(error_email)s</div>
        <br>

    <input type="submit">
</form>"""


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)


class MainHandler(webapp2.RequestHandler):
    def write_form(self, username="", error_username="", password="", error_password="", verify="", error_verify="", email="",error_email=""):
        self.response.out.write(form % {"username": (username), "error_username": (error_username),
                                        "password": (password), "error_password": (error_password),
                                        "verify": (verify), "error_verify": (error_verify),
                                        "email": (email), "error_email": (error_email)})

    def get(self):
        self.write_form()

    def post(self):

        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        is_valid_username = valid_username(username)
        is_valid_password = valid_password(password)
        is_valid_email = valid_email(email)

        error_username = "that's not a valid username."
        error_password = "that's not a valid password."
        error_verify = "passwords don't match."
        error_email = "that's not a valid email address"

        if (is_valid_username and is_valid_password and (is_valid_email or email == "") and password==verify):
            self.redirect("/welcome?username=" + username)
        else:
            if is_valid_username:
                error_username = ""
            if is_valid_password:
                error_password = ""
            if (is_valid_email or email == ""):
                error_email = ""
            if password == verify:
                error_verify = ""
            self.write_form(username, error_username, password, error_password, verify, error_verify, email, error_email)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.out.write("Welcome, %s" %username)
        # if username == "hello":

        # else:
        #     self.redirect('/')

app = webapp2.WSGIApplication([('/', MainHandler), ('/welcome', WelcomeHandler)], debug=True)
