"""
Description:
 Generates a CSV reports containing all married couples in
 the Social Network database.
Usage:
 python marriage_report.py
"""
import os
import sqlite3                #We need sqlite3 to interact with the database
from create_relationships import db_path #We need the database path used to create relationships
import pandas as pd #Pandas is used to generate a CSV file of all the married couples

def main():
    # Query DB for list of married couples
    married_couples = get_married_couples()

    # Save all married couples to CSV file
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'married.csv')
    save_married_couples_csv(married_couples, csv_path)


#We have to search the database for every couple under the Spouse catagory, and save the results to a variable. This will be used to convert the data into a csv file.

def get_married_couples():
    """Queries the Social Network database for all married couples.
    Returns:
        list: (name1, name2, start_date) of married couples 
    """

    connect = sqlite3.connect('social_network.db')   #Connect to the DB
    cursor = connect.cursor()                      #Initiate the cursor

    #For married couples,we must select the two randomly generated people, but ONLY if they
    #have the 'spouse' type. We join these two values together (person 1 and 2) which indicate the relationship
    married_couples = """
        SELECT person1.name, person2.name, start_date FROM relationships
        JOIN ppl person1 ON person1_id = person1.id
        JOIN ppl person2 ON person2_id = person2.id
        WHERE type = 'spouse';
        """
    cursor.execute(married_couples)       #Execute the query
    married_couples = cursor.fetchall()      #We need a variable to get the results from said query, it is used later
    connect.close() #close connection
    return married_couples

#Now we save the amount of married couples to a csv file that can be viewed in Excel.
#This is easily done in Pandas
def save_married_couples_csv(married_couples, csv_path):
    """Saves list of married couples to a CSV file, including both people's 
    names and their wedding anniversary date  
    Args:
        married_couples (list): (name1, name2, start_date) of married couples
        csv_path (str): Path of CSV file
    """

    #Generate and save our csv file with the married couples we just collected and our custom headers for the columns
    df = pd.DataFrame(married_couples, columns=['Person #1', 'Person #2', 'Date of Anniversary'])
    df.to_csv(csv_path, index=False)
    return

if __name__ == '__main__':
   main()
