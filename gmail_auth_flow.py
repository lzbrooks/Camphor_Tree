from __future__ import print_function

import sys

from apis.google_api import GMailAuth


def gmail_auth_flow(args):
    auth_option = get_auth_option(args)
    gmail_auth = GMailAuth()
    if auth_option == "re_watch":
        gmail_auth.re_watch()
    elif auth_option == "refresh":
        gmail_auth.refresh_with_browser()
        print(f"\nUpdate Python Anywhere .env file "
              f"CAMPHOR_TREE_REFRESH_TOKEN with {gmail_auth.token_file} contents")
    else:
        print_help(auth_option)


def get_auth_option(args):
    try:
        auth_option = args[1]
    except IndexError:
        auth_option = None
    return auth_option


def print_help(auth_option):
    print(f"Argument '{auth_option}' given is not valid")
    print("Valid arguments are either 're_watch' or 'refresh'")
    print("\nEnvironment Variables needed are:")
    print("GOOGLE_APPLICATION_CREDENTIALS: 'credentials.json' client credentials file path")
    print("CAMPHOR_TREE_ACCESS_TOKEN_FILE: 'token.json' refresh token file path")
    print("\nre_watch specific environment variable needed is:")
    print("CAMPHOR_TREE_TOPIC: google pub/sub topic string")


if __name__ == "__main__":  # pragma: no cover
    gmail_auth_flow(sys.argv)
