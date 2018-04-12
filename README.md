# fullstacknano-catalog
Item Catalog project for Udacity Full Stack Nanodegree

## Scenario
Develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit, and delete their own items.

#### Required Software
* Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* Install [Vagrant](https://www.vagrantup.com/downloads.html)
* [Google+ account](https://accounts.google.com)
* Download or Clone this repository and open a command prompt to the new folder with the project files

## Usage
Run the Vagrant VM, log in, and use python to run the flaskserver.py. This will start a web server on your localhost port 5000. Browse to [http://localhost:5000/](http://localhost:5000/) to view the web page. Once you login, you will have access to edit about half of the items and create new items.

Start the VM - this may take a few minutes

    vagrant up

Login to the VM

    vagrant ssh

Configure the initial database

    cd /vagrant
    python3 db_initialize.py

Run the web server using python.

    cd /vagrant
    python3 flaskserver.py
