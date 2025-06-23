docker login
cd chroma
docker build -t joctan04/chroma:latest .
# docker push joctan04/chroma:latest
cd ..
cd flask-api
docker build -t joctan04/flask-api:latest .
# docker push joctan04/flask-api:latest
cd ..
cd web-apache
docker build -t joctan04/web-apache:latest .
# docker push joctan04/web-apache:latest
cd ..