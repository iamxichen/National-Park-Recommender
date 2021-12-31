# National & State Parks Data

This project is the term project for DSCI 511 for winter term 2021 at Drexel University, Philadelphia, PA.

## Authors

- Group member 1
    - Name: Ashwina Mistry
    - Email: am4828@drexel.edu
- Group member 2
    - Name: Tien Nguyen
    - Email: thn44@drexel.edu
- Group member 3
    - Name: Xi Chen
    - Email: xc98@drexel.edu
- Group member 4
    - Name: Rishav Sarangi
    - Email: rs3563@drexel.edu

---

## Table of Contents

- Introduction
- Project Description
- Usage
- Development
- Challenges and Limitations

---

## Introduction

This project collects the data of 468 US national parks and state parks from all 50 states which provides information about the park. The data we collect will be helpful for anyone looking to visit the national parks and spend time in the vicinity of nature for recreation. This collected data is stored in .csv files and can be used for further development by anyone to locate the park on a map, display its description, activities and weatherinfo. 

## Project Description

The data source for national parks will be from the National Park Service website which contains information about the 468 parks in the country. The columns will include park name, latitude, longitude, description, activites and weather info. The state parks will be extracted from wikipedia and will contain similar information including the title, park code, latitude, longitude, description at each park. 

## Usage

Download the files NationalParks.ipynb and StateParks.ipynb. Prior to running NationalParks.ipynb and StateParks.ipynb, install all required libraries. If running on Jupyter Notebook, only the Wikipedia library needs to be installed. Install the Wikipedia library by running:

    $ pip install wikipedia

Once installed, the user can simply run the code to access and view the necessary information about the national parks and state parks from the given websites.  

## Development
### NationalParks.ipynb 

The code navigates to https://www.nps.gov/findapark/index.htm and collects all the national park name codes by web scraping using BeautifulSoup. Function park(code) is defined and called for each park. Function park(code) creates the API request using the park code. Park name, latitude, longitude, description, weatherInfo, and activities are gathered from the response and stored in dictionary. Nationalpark.csv file stores the values of dictionary if they do not exist in the file. The function can be carried out up to 468 times to collect information for all national parks. The information will also be displayed in a table using pandas. 

### Stateparks.ipynb 

Stateparks.ipynb creates a list of 50 states, which is collected by web scraping from https://en.wikipedia.org/wiki/Lists_of_state_parks_by_U.S._state. Once the state names are collected, URL is created for each state park by filling the URL format with the state names. For example, for the state of Alabama, the URL is: https://en.wikipedia.org/wiki/List_of_Alabama_state_parks.  

Data is then scraped from each state's website about state parks to get individual park names. URL is created for each park of the state (example : https://en.wikipedia.org/wiki/Blue_Springs_State_Park) and data is scraped from each individual park website for name, latitude, longitude, and description. Data will be collected for each park in the state. This can be repeated for up to 50 times to collect information on states parks from all 50 states.

## Challenges and Limitations

One of the challenges was that the code was sending multiple requests in a short amount of time and these requests are sometimes blocked. Resolved this by placing a time delay before each request is sent. Another challenge was the request limit for nps.gov website, which is 1000. While trobleshooting, the code sometimes reached the request limit, and hence the website was blocking the requests sent as the maximum number of retries is exceeded.

Also, information about state parks on Wikipedia is inconsistent. The name of the categories are mostly different from park to park, from state to state. Therefore, using the same script to extract information from all the park websites is impossible. For example, we were able to extract information about "activities" for state parks in Alabama, but that would not work for New York and other states. Each state requires a different script to extract the desired information. Due to a lack of required data on Wikipedia, we also could not find information on weather. 

In addition, not all state park Wikipedia articles contain their coordinates. A lot of state parks did not have coordinates information and code was failing while trying to get values for coordinates. The code had to be run through each state park to collect the parks without coordinates and then create a list of those parks so that those parks can be skipped during web scraping. Due to time constraint and data issues, data could not be collected for Texas, Vermont, Connecticut, Illinois, Iowa, Kentucky, Louisiana, Massachusetts, Michigan, Minnesota, Nevada, New Hampshire, New Jersey, New York, North Carolina, Pennsylvania, Rhode Island, South Carolina, Tennessee.

Another limitation is that Wikipedia is not a reliable source. Information on Wikipedia can be edited by anyone at anytime. This means the information in contains can be a work in progress, not up to date, or plain wrong. We decided to use Wikipedia to generate information of state parks because we were not able to find state park information on any other website.dia to generate information of state parks because we were not able to find state park information on any other website.
