# Will create database for each stock that holds the calculated fundamentals fom set date to current

class Dataset:
    def populateDatabase(self):
        # Needs to check if csv file exists
        # If not, create
        # Populate array from set start date to current time
        
        # If file does exist check if the previous time is current time minus interval
        # If so then calculate current time and add to csv
        # If not populate from last date to current time

        print("Will populate database from set date to current time")