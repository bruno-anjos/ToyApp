rm -r -f logs #removes previous logs
mkdir logs #creates a new directory to store logs
touch logs/install_log.txt #creates a new log file
touch logs/image_name.txt #creates a log to have the image name

echo "Building Docker image"
docker build Container > logs/install_log.txt # redirects all outpur to the logs file
cat logs/install_log.txt | grep "Successfully built" #just displays the success message

#does some magic stuff to get the image name into the file "image_name"
cat logs/install_log.txt | grep "Successfully built" > logs/image_name.txt
perl -pi -e 's/Successfully built//g' logs/image_name.txt
perl -pi -e 's/ //g' logs/image_name.txt


