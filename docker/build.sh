docker login $1
cd chroma
docker build -t $1/chroma:latest .
docker push $1/chroma:latest
cd ..
cd flask-api
docker build -t $1/flask-api:latest .
docker push $1/flask-api:latest
cd ..
cd web-apache
docker build -t $1/web-apache:latest .
docker push $1/web-apache:latest
cd ..