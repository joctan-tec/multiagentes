# This Dockerfile will create a web server using Apache and will serve the files from the /var/www/html directory.
FROM httpd:2.4

# Copy the HTML and Javascript files to the Apache server's document root from app/
COPY app/ /usr/local/apache2/htdocs/
