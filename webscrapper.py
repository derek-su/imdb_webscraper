from bs4 import BeautifulSoup
import requests

import time
import random

from datetime import datetime

import matplotlib.dates as mdates
import numpy as np 
import matplotlib.pyplot as plt

import csv

def scrape_spirited_reviews():
    
    # Access the main website for reviews
    spirited_url = 'https://www.imdb.com/title/tt0245429/reviews?ref_=tt_ov_rt'
    connection = requests.get(spirited_url)
    soup = BeautifulSoup(connection.content, 'html.parser')
    
    # Set up empty lists for the upcoming ratings and dates data (should be global)
    ratings_list = []
    dates_list = []
    edited_ratings_list = []
    datetime_list = []
    
    def grab_datakeys():
    
        # Create a Boolean variable for the upcoming while loop
        newpage = True

        # Grab the data-key and ajaxurl from the original user review website
        new_section = soup.select('.load-more-data')
        datakey = new_section[0]['data-key']
        print('Scrapping user review page. Utilizing original datakey: ' + datakey)
        ajax_link = new_section[0]['data-ajaxurl']

        # While the Boolean variable is true
        while newpage == True:

            # Check if there is still a datakey
            if datakey != None:

                # Combine the url to create the new link to the next page of reviews
                combine_url = 'http://www.imdb.com/' + ajax_link + '?paginationKey=' + datakey

                # Establish a new connection to this new url
                new_connection = requests.get(combine_url)

                # Parse the HTML content of the new page
                broth = BeautifulSoup(new_connection.content,'html.parser')

                # Select the class = 'load-more-data' on the page
                new_section = broth.select('.load-more-data')

                # Find all review text sections on this website
                n_allsections = broth.find_all('div', class_ = 'lister-item mode-detail imdb-user-review collapsable')

                # Define the function for scrapping the data (ratings and dates)
                def scrapping():

                    # For every review on the page:
                    for review in n_allsections:
                        # Try to store the rating into a variable (locate_rating)
                        
                        # NOTE: '.find' method must include .text.strip() to store as a string, else variable becomes a NoneType

                        # And store the dates into a variable (locate_date)
                        try:
                            locate_rating = review.find('span', class_ = 'rating-other-user-rating').text.strip()

                            locate_date = review.find('span', class_ = 'review-date').text.strip()
                        except:
                            
                            continue
                            
                        else:
                            ratings_list.append(locate_rating)
                            dates_list.append(locate_date)

                # Execute the scrapping function
                scrapping()


                # Test to see if can get the datakey
                try:
                    datakey = new_section[0]['data-key']

                except: # If you get an error for accessing the datakey, break out of the while loop
                    
                    # This may mean that you reached the end of the reviews, therefore break out of the loop
                    newpage = False
                    break
                    
                else: # If you can get an datakey, grab the new datakey and store it into the variable and repeat the loop

                    # Use the time function to make sure it creates a random time between 1 to 3 seconds before repeating the loop
                    time.sleep(random.randint(1,3))
                    print('\nScrapping next review page. Utilizing next datakey: ' + datakey)
                    continue

            else:
                newpage = False
                break
    
    # Execute the datakeys functon
    grab_datakeys()
    
    # Remove the '/10' from the Ratings List
    def filter_ratings():
        for rating in ratings_list:
            remove_slash = rating.split('/') 			# Remove the / from all the ratings, making each value an individual index
            popped_numer = remove_slash.pop(0) 			# Pop out all numerator values of each rating
            popped_numer = int(popped_numer)			# Convert the string values into integer values (necessary for plotting the data points later)
            edited_ratings_list.append(popped_numer) 	# Add these popped numerators into a new list
    
    # Execute the Filter Ratings Function
    filter_ratings()
    
    # Convert Dates to DateTime Type
    def convert_dates():
        
        # For every date in the Dates List (string type)
        for date in dates_list:
            
            # Convert each date from a string to a datetime type
            datetime_date = datetime.strptime(date, '%d %B %Y')
            
            # Append the new datetime dates into the empty list
            datetime_list.append(datetime_date)
    
    # Execute the converting date function
    convert_dates()
    
    # Import the data into a csv file
    with open('spirited_away_reviews.csv', 'w') as f:
        writer = csv.writer(f)

        # Create the header row
        writer.writerow(['Data of Review', 'Rating (Out of 10)'])

        # Use the zip function to 'zip' the two lists together so each item contains the date and its respective rating
        writer.writerows(zip(datetime_list, edited_ratings_list))
        
    f.close()
       
    # Import the data from the 2 lists into a scatterplot

    plt.plot_date(datetime_list, edited_ratings_list, c = 'blue')		# Plot_date because of x-axis being datetime format (instead of .scatter)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Set the x-axis to have ticks in the form of abbreviated month and full year
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))  # Set the x-axis to have an interval of 6 months per tick
    plt.yticks(np.arange(0, 11, 2))										# Have the y-axis have a range from 0-10 with an interval of 2 per tick
    plt.setp(plt.gca().xaxis.get_majorticklabels(),'rotation', 90)		# Rotate each x-axis tick label to be 90 degrees from horizontal (aka vertical)
    plt.gcf().set_size_inches((20, 10))									# Set the graph to be a size of 20 x 10 inches
    plt.xlabel('Date of Posted Review')
    plt.ylabel('Rating (out of 10)')
    plt.title('Ratings of Spirited Away Over the Years')
    plt.show()															# Show the graph
    
    print('\nScrapping Completed.')
    print('\nTotal Data Points: ')
    print(len(edited_ratings_list))

if __name__ == '__main__':
	scrape_spirited_reviews()
