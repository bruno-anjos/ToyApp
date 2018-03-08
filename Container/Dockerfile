
# create an image from scratch
FROM openjdk:8

# Set the working directory to /app
WORKDIR /app

ADD database_creation.sql database_creation.sql
ADD toyapp.py toyapp.py
ADD init_container.sh init_container.sh

RUN apt-get update 
RUN apt-get install -y python3.5 
RUN apt-get install -y python3-mysqldb 
RUN apt-get install -y mysql-server 
RUN apt-get install -y mysql-client 
	

# Define default command.
CMD ["bash"]