# imdb_webscrapper
IMDB Webscrapper - Movie: Spirited Away
This project scrapes the rating and date of review for each user review on the IMDB website for the movie Spirited Away.

NOTE:

With the "load more" button in the IMDB user review page, this programs loads all reviews by scrapping each data-key on the page 
and reconnects to the website using the newly acquired data-key.
      
IMDB split the total reviews of a movie into different pages that can be accessed by combining
'http://www.imdb.com' + data-ajaxurl + '?paginationKey=' + data-key

data-ajaxurl and data-key are variables nested in the class "load-more-data". So, by accessing the new url, another set of reviews appear
with a new data-key being issued for each new page.
