
# create an image from scratch
FROM openjdk:8

# Set the working directory to /app
WORKDIR /app

ADD init_container.sh /tmp/init_container.sh
ADD init_sql.sql init_sql.sql
ADD toyapp.py toyapp.py

RUN \
	bash /tmp/init_container.sh


CMD ["bash"]
