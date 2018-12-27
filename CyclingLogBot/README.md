# CyclingLog: cycling tracks info manager &amp; data analyzer

CyclingLog stores (in sqlite DB) and analyze track information. Its server side is a CLI tool for user management and bot launching. It also has a TelegramBot interface to add info and analyze data.

## Basic usage

    # launch bot if only one user registered
    cylog

    # launch bot for a given user
    cylog -u user_name

    # adding new user
    cylog -u user_name --url user_dir_url

    # updating the user_dir_url of given user
    cylog -u user_name --update user_dir_url

    # deleting user
    cylog --delete user_name
