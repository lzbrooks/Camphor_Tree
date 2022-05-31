from flask import Flask, request, redirect

from google_api import GMailMessage


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def console():
    if request.args and 'code' in request.args:
        print("")
        print("...Getting GMail Refresh Token...")
        auth_code = request.args.get('code')
        gmail_message = GMailMessage()
        refresh_token = gmail_message.get_refresh_token(auth_code)
        print("")
        print("Update Heroku Environment Variable CAMPHOR_TREE_REFRESH_TOKEN with value " + refresh_token)
        print("")
        print("Please CTRL-C Out of Server")
        print("")
        return "Update Heroku Environment Variable CAMPHOR_TREE_REFRESH_TOKEN with value " + refresh_token, 200
    if not GMailMessage().read_auth_config("%m/%d/%Y, %H:%M:%S"):
        print("")
        print("...Refreshing GMail Token...")
        print("Login to Google Account With CAMPHOR_TREE_EMAIL Credentials")
        gmail_message = GMailMessage()
        return redirect(gmail_message.get_auth_code_url())
    print("")
    print("Credentials Already Written")
    print("")
    return "Credentials Already Written To File", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context='adhoc')
