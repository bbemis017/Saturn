# Saturn

Saturn is a lightweight web page generator designed for people who would like to build their own web page.

TODO: add summary, description, documentation.



### Amazon Web Services (AWS) info

Public DNS: ec2-52-71-144-214.compute-1.amazonaws.com

Public IP:  52.71.144.214

In order to ssh into the server you will need the key file which will be sent to everyone on slack. The ssh command should be formatted like this:

    ssh -i saturnkey.pem ubuntu@52.71.144.214

### Web files

currently I have apache configured to search for web files under the directory /var/www anything outside this directory should not be accessible publicly. We can change this directory once we actually start hosting files.


