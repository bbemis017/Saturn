# Saturn

Saturn is a lightweight web page generator designed for people who would like to build their own modern look and decent web page.

TODO: add summary, description, documentations.



# Amazon Web Services (AWS) info

Public DNS: ec2-52-71-144-214.compute-1.amazonaws.com

Public IP:  52.71.144.214

In order to ssh into the server you will need the key file which will be sent to everyone on slack. The ssh command should be formatted like this:

ssh -i saturnkey.pem ubuntu@52.71.144.214

Keep in mind that there is only one account to ssh in with, so you should avoid staying logged in very long. I have installed apache2, mysql, php, git, and phpmyadmin to this server instance. If we need to install anything else to the server instance we just need to keep in mind that the server is running Ubuntu 14.04.

phpmyadmin
accessible at: http://52.71.144.214/phpmyadmin

username: root

password: saturn

Web files:

currently I have apache configured to search for web files under the directory /var/www anything outside this directory should not be accessible publicly. We can change this directory once we actually start hosting files.


