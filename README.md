# National-Park-Recommender
National park recommender based on web-scraped Wikipedia data and user survey responses

Stephen Yi, Tien Nguyen, Tuan Huynh, Xi Chen

Welcome to our national park recommender! Many national parks offer a wide range of experiencese, so we understand that it can be hard to choose which park to visit next.
Let's go!

TABLE OF CONTENTS
1. Group Background
2. Abstract
3. Scope
4. Potential Users/Applications
5. Implementation
6. Limitations/Challenges
7. Future Work 
8. Team Members' Workload

## 1. Group Background

*  Stephen Yi
   * Backrground/domain knowledge: Health Science background. Two years as a desktop support analyst at Vanguard. 
   * Skills: Python, statistics, and data preprocessing
* Tien Nguyen
   * Background/domain knowledge: Chemical engineering
   * Skills: Python, statistics, data preprocessing, and machine learning
* Tuan Huynh
   * Backrground/domain knowledge: Business and finance background. Five years as a logistics manager in the US Navy.
   * Skills: Python, web design (HTML&CSS)
* Xi Chen
   * Backrground/domain knowledge: Chemical engineering, statistical analysis
   * Skills: Python, data visualization

## 2. Abstract

The team consists of 4 team members with unique backgrounds and skill sets who will be using this opportunity to polish their data science skills and conduct analyses with the data. The datasets used will be from a DSCI 511 project and Kaggle. The dataset from DSCI 511 contains information about over 400 US national parks, and the dataset from Kaggle contains information about over 3000 hiking trails of 60 national parks. The analyses will utilize information from the datasets to make recommendations on which parks and trails to visit based on the user's interests.

## 3. Scope

A national park recommender model is created to provide visitors with suggestions and recommendations based on their interests. The model uses two datasets which contain information on US national parks and hiking trails at those parks. The model is developed using the Python programming language to conduct natural language processing on the datasets. The main libraries used are NumPy, pandas, and sklearn. 

## 4. Potential Users and Applications

National parks are high traffic locations frequented by people for many different reasons. Many just want to enjoy the beautiful scenery certain parks have to offer while others prefer to engage in activities such as camping and hiking. However, the United States has 423 national park locations. Therefore, this model hopes to provide a list of recommended parks based on an individual’s preferences.
This model can be used as an application because it will use user generated input to calculate the ideal parks for people. Information such as activities, weather, and landscapes can be collected to determine a list of parks. By providing accurate results of recommended parks, we hope to minimize the planning and research people may have to undergo prior to selecting a national park. 

## 5. Implementation

### 5.1. Gather Data from Kaggle and DSCI 511 Project:

Our first step in the project involved collecting data from 2 different datasets. The first was the Alltrails data - nationalpark.csv from Kaggle, and the second was the nationalpark.csv from a DSCI 511 project. Next we created a dataframe using pandas to store the data.

alltrails_df = pd.read_csv('AllTrails data - nationalpark.csv')
parks_df = pd.read_csv('nationalpark.csv')

Next, we implemented a quiz which prompts the user to answer questions, with the responses being used for our program to recommend a park and trail to visit. This was done with the prompts function in recs.py. The questions that we used were as followed: 

* What activities would you like to do at the parks? 
* What else is on the itinerary?
* What are you interested in learning about?
* What landscapes would you like to see?
* What type of weather would you like?
* What season are you most likely to find your park in? 
* What is your ideal length for hiking trails?
* How popular do you like your hiking trails to be?

The prompts function will return 8 outputs, each the number corresponding to the user’s answer to each question.

activities, itineraries, learnings, landscapes, weathers, seasons, length, popularity = recs.prompts()

Next, we will create two sets of recommendations based on each dataset.

### 5.2. Recommendation of National Parks

#### 5.2.1. Vectorize Dataset and Obtain TF-IDF Matrices

This step involved using the TfidfVectorizer feature from the sklearn module. For each dataset that we generated based on the user’s answers, we used the TfidfVectorizer to create a TF-IDF (term frequency–inverse document frequency) matrix. This matrix is used to reflect how important a keyword is in each column. 

def vec(column, parks):
vectorize= TfidfVectorizer(analyzer='word',stop_words= 'english', token_pattern=r'(?u)\b[A-Za-z]+\b')
response = vectorize.fit_transform(parks[column])
df_tfidf = pd.DataFrame(data = response.toarray(), index = parks['name'], columns = vectorize.get_feature_names())

#### 5.2.2. Generate Recommendations

Our final step brought the user’s input and the created TFIDF matrix together. Using the recommend function, we weighted each frequency based on the rank the user placed their response as. We then merged all the matrices together into one final TFIDF matrix, using the sum_tfidfs function, that we will use to recommend national parks that will best match the user’s responses. 

def sum_tfidfs(tfidfs, parks):
pd.concat(tfidfs)\
           .groupby('name')\
           .sum().reset_index().set_index(parks['name'])

From the weighted frequencies, we selected the top 25 rows from the entire data set. Afterwards, we merged the rankings and ranked the rows again based on the same weighting and returned the dataset containing the recommended park to visit. 

def merge_sum(list_df):
for i in range(len(list_df) - 1):
            list_df[i+1] = pd.merge(list_df[i], list_df[i+1], on = 'name', how = 'inner')
        merged = list_df[i+1]
        merged_sum = merged.sum(axis = 1).sort_values(ascending = False)[0:25]
         return merged_sum

### 5.3. Recommendation of Specific National Park Trails

Six functions were used to recommend specific national park trails to create a ranking based on activity, trail length, and trail popularity selections.. First, thecreate_idf function is used to create a TF-IDF matrix of the activity “scores” of each trail to base the recommendation on. Then, the rank_activity function is used to provide a sorted dataframe based on the values of the weighted average scores of the desired activities. The function punishes places that feature all of the above, along with something else, such as fishing, hiking, walking, and nature-trips. If a user would like to rank the top trails based on length of trail, from shortest to longest, it would be a simple matter of taking the average of all lengths, and then ranking it from there. There is no actual metric for what length is unfortunately, so we will proportionally rank them based on average. We will prompt a user if they want a short, short -medium, medium, medium-long, long, each being in 20% metrics or so.

The rank_length and rank_popularity functions are used to generate sorted dataframes based on the user’s trail length and popularity selections. The find_inersections function finds parks that appear in both of the inputs. Finally, everything is combined to provide a recommendation of the top 10 trails.

## 6. Limitations/ Challenges

While we improved from our scope to include both datasets and include more features to impact the recommendation, such as weather, location, difficulty, etc., this project is not without its challenges and limitations. A limitation was our utilization of the TF-IDF matrix for activities. For example, while many trails had multiple features, if a trail/park had fewer features that matched the user’s response, it was given a higher frequency value than another park that could match the criteria that had other features. This can skew data, punishing parks that had a lot of activities and favoring parks that had limited activities that just happened to match the features that the user requested.  
One challenge we encountered was how we weighted the user’s response. We wanted the user to have the option to rank their response for more personalization in the output. In our program, we decided on a weighting as 1-i/n, where i is the placement users’ placement, and n is the amount of options the user chose. This may not be the most optimal choice, and will most definitely change our output should we choose to modify this formula. 
Another challenge we encountered while utilizing the TF-IDF matrices was that some options that the user might be interested in are not present in all parks. For example, not all parks contain “canyons” in their descriptions. If the user selects “canyons” as an interest, the program will throw an error in the weighted average calculation function because of non-matching dimensions in the dot product calculation. To combat this, we limited the user response options to contain only words that appear in all datasets. However, this restricts the number of options that users are allowed to choose from. If the user’s true interests are not in the lists of options given, the program may not provide a good recommendation.

## 7. Future Work

The project has high potential for further development. More details and information of the national parks and trails can be added to further specify the users’ searches. We can look for or generate more datasets that could add more valuable information such as biodiversity, pictures, and foliage. Another suggestion would be visualizing the locations of all the parks and trails on a map. Each map could be identified by a flag, and the flag’s color could be varied based on the user's preferences. For example, the recommended parks and trails could be marked on the map with green flags and the rest could be blue.
The recommendation algorithm could be further refined in a couple of ways to provide better recommendations. One of the ways that the program can be improved is to provide interactive questions based on the user’s response to the previous question. For example, if the user’s activity of interest is “snowshoeing”, we will provide a different set of questions than if the activity of interest is “off-road driving”. This will allow us to ask more targeted questions and make the recommendation more accurate.
