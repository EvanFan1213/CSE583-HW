cd Desktop/UWCourses/CSE583
mkdir pronto
cd pronto
touch README.txt
echo "This directory holds the pronto data." > README.txt
cat README.txt
mkdir data
cd data
curl -O https://s3.amazonaws.com/pronto-data/open_data_year_one.zip
unzip open_data_year_one.zip
head 2015_trip_data.csv
