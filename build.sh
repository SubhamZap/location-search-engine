docker build -t location-search-engine .
docker tag location-search-engine:latest 923812021176.dkr.ecr.ap-south-1.amazonaws.com/location-search-engine:latest
docker push 923812021176.dkr.ecr.ap-south-1.amazonaws.com/location-search-engine:latest