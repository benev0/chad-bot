# chad-bot
A very simple bot for moderating discord usernames. Written in python with a postgres database using the discord.py and psycopg2 libraries.

## Features
When a user updates a username if that username does not include the substing that is in the database the bot will set the user's name to the substring. 

## Commands
- g - prefix works only in a guild
- a - requres admin
### ga - $name(user, policy)
Sets the users policy and checks the policy.

### ga - $runall(role=None)
Runs all users username check if the bot has just come back online for example. If a role is porvided then users without a policy will recieve that role.

### ga - $delete(user)
Deletes a user policy

### g  - $whoami
Displays sender's policy. Note that None will be sent if no policy exists in the database.

### g  - $whois(user)
Displays user's policy, Note that None will be sent if no policy exists in the database.

### g  - $status
Displays a message.

## Other
Licence: see issues
Feedback welcome.
PRs welcome if you want to (it is less than 200 lines), but use a fork.
