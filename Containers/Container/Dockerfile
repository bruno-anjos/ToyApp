
# create an image from scratch
FROM mysql:5.7.22

# Set the working directory to /app
WORKDIR /app

ADD DB_script.sql DB_script.sql
ADD toyapp.py toyapp.py
ADD init_container.sh init_container.sh

RUN apt-get update && apt-get install -y python3-mysqldb  --no-install-recommends
	

# Define default command.
CMD ["bash"] 
