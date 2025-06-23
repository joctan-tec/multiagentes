cd docker
./build.sh $1
cd ..
cd charts
./uninstall.sh
sleep 5
./install.sh
cd ..
echo "Deployment complete. Access the web interface at http://localhost:30080"
echo "API is available at http://localhost:30500"

