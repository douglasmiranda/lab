#!/usr/bin/env bash

# Install Xcode Command Line Tools.
xcode-select --install

# Install Homebrew.
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# Install brew basics (auto-updating).
brew install terminal-notifier
brew tap domt4/autoupdate
brew autoupdate --start --upgrade --cleanup --enable-notifications

# Install brew essentials.
brew install git
brew install ack

# Install download utilities.
brew install youtube-dl
brew install wget
brew install httpie

# Install fancy shell stuff.
brew install fish
brew install googler

# Install Python utlitlies.
brew install python2
brew install python3


# Make Python 3 system default.
rm -fr /usr/local/bin/python
ln -s /usr/local/bin/python3 /usr/local/bin/python

pip2 install virtualenv

touch ~/.config/fish/config.fish
echo "set -gx PATH $HOME/.local/bin \$PATH" >> ~/.config/fish/config.fish
curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | python2

# Install fish plugin https://github.com/fisherman/done

pipsi install pew
pipsi install pipenv

pipsi install fabric
pipsi install stormssh
