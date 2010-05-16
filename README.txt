setupy is a tool to automate the process of installing/updating/uninstalling
software on servers.

It's made in Python and have a command-line interface and an API acessible via
other Python software.

We call action something that you execute on the server, for example install some software.
We call recipe a collection of actions for the same software, for example: a MySQL recipe should have actions to install, configure and uninstall MySQL.
We call cookbooks a collection of recipes, for example: LAMP should be a recipe to install and configure Apache, MySQL and PHP on a Linux box.

If you want to contribute please read WISHLIST file.
