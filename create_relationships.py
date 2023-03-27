"""
Description:
 Creates the relationships table in the Social Network database
 and populates it with 100 fake relationships.
Usage:
 python create_relationships.py
"""

import os             #What don't we need os for?
import sqlite3    #We need Sqlite3 to communicate with the database
import random #We need random and its functions to base results and create fake information based on random choices and integers
from random import randint
from random import choice
from faker import Faker     #Faker helps create our fake people that fill up the database
from datetime import datetime     #Datetime is used at random to get full dates for people

# Determine the path of the database
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'social_network.db')

def main():
    create_people_table()       #In case the database does not exist, create it
    populate_people_table()      #Populate the table with fake people
    create_relationships_table()      #Create relationships of two within that data
    populate_relationships_table()    #And populate the database with those relationships


def create_people_table():
    """Creates the people table in the database"""

    connect = sqlite3.connect('social_network.db')   #Connect to the database
    cursor = connect.cursor()                     #Activate our cursor

    #Create a query that will include a list of people. The values included
    #must NOT be blank. This include the id, name, email and biography of the fake person
    create_ppl_tbl_query = """
            CREATE TABLE IF NOT EXISTS ppl
            (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                province TEXT NOT NULL,
                bio TEXT,
                age INTEGER,
                created_time DATETIME NOT NULL,
                updated_time DATETIME NOT NULL
            );
            """
  
    cursor.execute(create_ppl_tbl_query)      #Execute the query
    connect.commit()                   #Commit it to the connection
    connect.close()                     #And close it after it is done
    return

def populate_people_table():
    """Populates the people table with 200 fake people"""
  
    connect = sqlite3.connect('social_network.db') #Initiate the connection with the db
    cursor = connect.cursor()                      #and our cursor as well

    #We must create a query that fills in the values given
    #in the query created above. This will be filled in and replacing the
    #"?" wildcards, which accept any type of matching data it recieves.
    add_person_query = """
            INSERT INTO ppl
            (
                name,
                email,
                address,
                city,
                province,
                bio,
                age,
                created_time,
                updated_time
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """
  
    #To fill in these values, we use faker and its ability to generate random info regarding a
    #fake person to add to the db. For this, we select en_ca to specify a fake Canadian resident
    #and add all of our results to execution which will fill in the wildcards when generating.
    fake = Faker("en_ca")       #Select english as our generated information (Canadian resident)
    for num in range (200):            #Generate at least 200 people
        new_person =  (                #Store the generated info in a tuple
                fake.name(),
                fake.free_email(),            #Faker comes with its own functions to generate
                fake.street_address(),    #fake information, so most of this is self-explanatory
                fake.city(),
                fake.province(),
                fake.sentence(nb_words=9),  #For the biography, we will limit the sentence down to nine words so it doesn't extend too far
                fake.random_int(min=5, max=85),  #For the age, Faker uses a random number from five to 85, indicating 5 to 85 years old (lol)
                datetime.now(),               #And for the start and updated dates, we use the current dates with Datetime
                datetime.now(),
            )

        # Execute query to add new person to people table
        cursor.execute(add_person_query, new_person)   #Execute each iteration of this tuple until we break out of the loop
      
    connect.commit()  #Commit all of the results and close connection
    connect.close()
    return

#Now with the generated data, we must create relationships between two people

def create_relationships_table():
    """Creates the relationships table in the DB"""

    connect = sqlite3.connect('social_network.db') #Initiate connection to the db
    cursor = connect.cursor()                         #And our cursor

    #For this query, a relationship is defined as person1 and person2's ids (unique identifiers in the database) along with a generated start date indicating an anniversary. The values must not be left blank
  
    create_relationships_tbl_query = """
        CREATE TABLE IF NOT EXISTS relationships
        (
            id INTEGER PRIMARY KEY,
            person1_id INTEGER NOT NULL,
            person2_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            start_date DATE NOT NULL,
            FOREIGN KEY (person1_id) REFERENCES ppl (id),
            FOREIGN KEY (person2_id) REFERENCES ppl (id)
        );
        """
  
    cursor.execute(create_relationships_tbl_query)    #Execute our query
    connect.commit()       #Commit it and close connection
    connect.close()
    return

#Since we generated data of relationships with uniquely chosen people based on their ids, we must now populate the table with these relationships so they can be generated later.

def populate_relationships_table():
    """Adds 100 random relationships to the DB"""
  
    connect = sqlite3.connect('social_network.db')  #Connect to the DB
    cursor = connect.cursor()                     #Bring up the cursor
  
    #To add relationships, we need the ids of each person as well as the type of relationship and the date of the beginning. There are several types of relationships, but the one we want is the 'spouse' one, which we yield later. The "?" characters are wildcards for information that will be overwritten into those values as we implement relationships into the database.
  
    add_relationship_query = """
        INSERT INTO relationships
        (
            person1_id,
            person2_id,
            type,
            start_date
        )
        VALUES (?, ?, ?, ?);
        """
    #Here is where we randomly select members of the relationship group. We do this by picking a random number, which indicates a person in the database and randomize the type of relationship, putting it all together in a tuple to be further used.
  
    fake = Faker()  #We need Faker in this section for a false date, which will be the beginning date of the relationship
    for num in range(100):    #Get at least 100 results
        person1_id = randint(1, 200)              #pick a number between 1 and 200
        person2_id = randint(1, 200)

        #If two ids match, keep randomizing it until they are different. This prevents someone from loving themself
        while person2_id == person1_id:
            person2_id = randint(1, 200)
          
        relate = choice(('spouse', 'partner', 'relative'))  #Pick a random relationship
        start_date = fake.date_between(start_date='-50y', end_date='today') #Choose a date from 50 years ago to today
        relationship = (person1_id, person2_id, relate, start_date) #store it all in a tuple
      
        cursor.execute(add_relationship_query, relationship) #Excecute each iteration of the tuple until the loop comes to an end
      
    connect.commit() #Commit it all and end connection
    connect.close()

    return 

if __name__ == '__main__':
   main()