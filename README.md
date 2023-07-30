# Laptop Price Prediction using Web Scrapping and Decision Trees
## Project overview
The goal of this project is to extract laptop data from 'Asusiran.com' and then atore this information, and build a machine learning model to predict laptop prices. the project is divided into three main scripts:
1. Web Scrapping: The 'data_saver.py' script sends HTTP requests to the website, extract laptops details like CPU, GPU, RAM and more. then saves these data into a table of a database.
2.  Table to CSV: The  'convert_to_csv.py' reads the database and writes the data of that table into a csv file.
3.  Machine Learning: The 'predict_price.py' script loads the laptops data from the CSV file, preprocesses it, train a Decsion Tree model, and predicts laptop prices based on user-specifications.


## Technologies Used
- Python 3
- BeautifulSoup for web scraping
-  Requests for making HTTP requests
-  mysql.connector for inserting into database
-  Pandas for write the CSV file
-  Scikit-learn for machine learning

