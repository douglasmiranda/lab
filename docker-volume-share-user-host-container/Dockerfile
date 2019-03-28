FROM alpine:3.9

# Default first user UID for some common Operating Systems
# Ubuntu/Debian: 1001
# MacOS: 501
#
# But you can get the UID for your current user with:
# id -u $USER
# My user is "douglas", so in my terminal: id -u douglas
# will give me: 1001
#
# For automating you want to use something more like:
# $(id -u $(whoami))
# OR
# $(id -u $USER)
# it will give you the id for your current user logged on to the terminal
#
ARG UID=1001
ENV HOMEAPP=/myapp
# Using a non-privileged user to own our code and things related to the project
RUN adduser -S -h $HOMEAPP -u ${UID} myapp

# So some stuff as sudo, and then:

USER myapp

# ./code:/myapp/code
VOLUME ["$HOMEAPP/code"]
