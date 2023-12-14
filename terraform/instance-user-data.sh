#!/bin/bash
sudo yum install -y httpd
sudo systemctl start httpd && sudo systemctl enable httpd
sudo echo "<h2 color="red">Hi!</h2> instance hostname: $(hostname)" > /var/www/html/index.html