import pandas as pd
import numpy as np
import matplotlib as plt
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. Getting and processing user input

# 1.1. Define function "prompts" that aks user questions and store those answers

def parse_list_input(possible,inp):
    indexes = [int(i) - 1 for i in inp.split(' ')]
    return [p for (i,p) in enumerate(possible) if i in indexes]

def prompts():
    selected_activities = parse_list_input(activities, input('What activities would you like to do at the park(s) (response in order of preference)?\n\
1.	Birding\n\
2.	Hiking\n\
3.	Walking\n\
4.	Nature-trips\n\
5.	Trail running\n\
6.	Mountain biking\n\
7.	Horseback riding\n\
8.	Camping\n\
9.	Backpacking\n\
10.	Snowshoeing\n\
11.	Rock climbing\n\
12.	Off road driving\n'))

    selected_itineraries = parse_list_input(itineraries, input("---\nWhat else is on the itinerary?\n\
1.	Learning about our country's history\n\
2.	Meandering through fascinating exhibits\n\
3.	Seeing the scenes from the comfort of my car\n\
4.	Getting off the road and into the water\n\
5.	Walking through historic sites\n"))

    selected_learnings = parse_list_input(learnings, input("---\nWhat are you interested in learning about?\n\
1.	People & Culture\n\
2.	American History\n\
3.	Arts & Sciences\n\
4.	Nothing in particular\n"))

    selected_landscapes = parse_list_input(landscapes, input('---\nWhat landscapes would you like to see?\n\
1.	Ice\n\
2.	Mountain\n\
3.	Forests\n\
4.	River\n\
5.	Lake\n'))

    selected_weathers = parse_list_input(weathers, input('---\nWhat types of weather would you like?\n\
1.	Humid\n\
2.	Dry\n\
3.	Cold\n\
4.	Hot\n\
5.	Temperate\n'))

    selected_seasons = parse_list_input(seasons, input('---\nWhat seasons are you most likely to find your park in?\n\
1.	Spring\n\
2.	Summer\n\
3.	Fall\n\
4.	Winter\n'))
                                                         
    selected_length = parse_list_input(seasons, input("---\nWhat is your ideal length for hiking trails? Please select only one option.\n\
1.	Short\n\
2.	Short-medium\n\
3.	Medium\n\
4.	Medium-Long\n\
5.	Long\n\
6.	I don't care\n"))
                                                         
    selected_popularity = parse_list_input(seasons, input("---\nHow popular do you like your hiking trails to be?. Please select only one option.\n\
1.	Obscure\n\
2.	Little-known\n\
3.	Medium\n\
4.	Well-known\n\
5.	Popular\n\
6.	I don't care\n"))
    return selected_activities, selected_itineraries, selected_learnings, selected_landscapes, selected_weathers, selected_seasons, selected_length, selected_popularity

# 1.2. List assignment - creates list for that maps the user input to the options in the prompts
activities = [
    'birding',
    'hiking',
    'walking',
    'nature-trips',
    'trail running',
    'mountain biking',
    'horseback riding',
    'camping',
    'backpacking',
    'snowshoeing',
    'rock climbing',
    'off road driving', 
]
itineraries = ['history', 'exhibits', 'car', 'water', 'historic']
learnings = ['culture', 'history', 'arts', 'park']
landscapes = ['ice', 'mountain', 'forests', 'river', 'lake']
weathers = ['humid', 'dry', 'cold', 'hot', 'temperate']
seasons = ['spring','summer','fall','winter']
lengths = ['short','short-medium','medium','medium-long','long',' ']
popularities = ['obscure','little-known','medium','well-known','popular']
                                                         
# 2. Read datasets
import pandas as pd
alltrails_df = pd.read_csv('AllTrails data - nationalpark.csv')
parks_df = pd.read_csv('nationalpark.csv')

# 3. Parks recommender portion

# First, filter the parks
def filter_trail(selected_areas):
    def inner(row):
        if 'all' in selected_areas:
            return True
    #for state in selected_areas:
     #   if row['state_name'] in state:
      #      return True
        return False
    return inner
def get_trails_in_area(selected_areas):
    f = filter_trail(selected_areas)
    is_in_area = alltrails_df.apply(f, axis=1)
    return alltrails_df[is_in_area]
def filter_park(trails):
    def inner(row):
        for trail in trails.area_name.unique():
            if row['name'] in trail:
                return True
        return False
    return inner

def get_parks_from_trails(trails):
    f = filter_park(trails)
    is_in_area = parks_df.apply(f, axis=1)
    return parks_df[is_in_area]
# 3.1. Vectorize the filtered datasets to obtain TD-IDF matrices

from sklearn.feature_extraction.text import TfidfVectorizer
# Calling the TfidfVectorizer from the sklearn library to vectorize the three text columns in elite_parks: description, activities, weatherInfo

def vec(column, parks):
    vectorize= TfidfVectorizer(analyzer='word',stop_words= 'english', token_pattern=r'(?u)\b[A-Za-z]+\b')
    response = vectorize.fit_transform(parks[column])
    df_tfidf = pd.DataFrame(data = response.toarray(), index = parks['name'], columns = vectorize.get_feature_names())
    return df_tfidf

# Merge all these TF-IDF matrices and add up all the values
def sum_tfidfs(tfidfs, parks):
    return pd.concat(tfidfs)\
       .groupby('name')\
       .sum().reset_index().set_index(parks['name'])

# 3.2. Based on the matrix, we can recommend national parks that best match the user's interest by ranking the values in the matrices

def recommend(selected, sum_tfidf):
    n = len(selected)
    weights = [1-i/n for i in range(n)]
    df = sum_tfidf.loc[:, sum_tfidf.columns.isin(selected)]
    df.insert(1, 'weighted_avg', (df.dot(weights))/np.sum(weights))
    top_25 = df.loc[:, 'weighted_avg'].sort_values(ascending = False)[0:25]
    return top_25


# Now merge the rankings and rank again based on sum of weighted avg scores
def merge_sum(list_df):
    for i in range(len(list_df) - 1):
        list_df[i+1] = pd.merge(list_df[i], list_df[i+1], on = 'name', how = 'outer')
    merged = list_df[i+1]
    merged_sum = merged.sum(axis = 1).sort_values(ascending = False)[0:25]
    return merged_sum

# Display recommendations to the user
def display_recs(parks, merged_recommendations):
    print("\n---\nYour park match is...\n")
    print('\033[1m' + f'*** {merged_recommendations.index[0]} National Park ***' + '\033[0m\n')
    park_index = parks.name[parks.name == merged_recommendations.index[0]].index.tolist()
    print(parks['description'][park_index].values[0] + '\n')
    print(f"Activities:\n {parks['activities'][park_index].values[0]}"+ '\n')
    print(f"Weather:\n {parks['weatherInfo'][park_index].values[0]}"+ '\n')
    print('Other good options to explore:')
    for park in range(1, 10):
        print(f"{merged_recommendations.index[park]} National Park")

# 4. Trail recommendation
def create_idf(trails_csv):
    import csv
    pd.set_option('display.max_columns', None)
    activities = []
    trails = []
    parks = []
    rankings = []
    lengths = []
    difficulties = []
    popularities = []
    pattern = "(?u)\\b[\\w-]+\\b"
    with open(trails_csv, newline='', encoding = 'utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            activity = row['activities']
            trail = row['name']
            park = row['area_name']
            rank = float(row['avg_rating'])
            length = float(row['length'])
            difficulty = float(row['difficulty_rating'])
            popularity = float(row['popularity'])
            activities.append(activity)
            trails.append(trail)
            parks.append(park)
            rankings.append(rank)
            lengths.append(length)
            difficulties.append(difficulty)
            popularities.append(popularity)

    vectorize = TfidfVectorizer(analyzer='word',stop_words= 'english', token_pattern = pattern)
    response = vectorize.fit_transform(activities)

    df = pd.DataFrame(data = response.toarray(), index = trails, columns = vectorize.get_feature_names())

    df.insert(0, 'Trail', df.index, True)
    df.insert(1, 'Park', parks, True)
    df.insert(2, 'Average Rank', rankings, True)
    df.insert(3, 'Length', lengths, True)
    df.insert(4, 'Difficulty', difficulties, True)
    df.insert(5, 'Popularity', popularities, True)
    df.reset_index(drop = True)
    return df
                                                         
def rank_activity(activities):   
    df = create_idf('trails_data.csv')
    user_interest = activities
    interest_rank = []
    weighting = 1
    ranks = pd.DataFrame()
    for interest in user_interest:
        if interest in df:
            interest_rank.append(df.loc[:,interest] * weighting) 
            weighting -= 1 / len(user_interest)
    ranks = pd.concat(interest_rank, axis = 1)
    ranks['AVG Score'] = ranks.sum(axis = 1) / len(ranks.columns)
    
    ranks.insert(0, 'Trail', df.index, True)
    ranks.insert(1, 'Park', df.Park, True)
    ranks.insert(2, 'Average Rank', df['Average Rank'], True)
    ranks.insert(3, 'Length', df.Length, True)
    ranks.insert(4, 'Difficulty', df.Difficulty, True)
    ranks.insert(5, 'Popularity', df.Popularity, True)
    ranks.reset_index(drop = True)
    
    return ranks.sort_values(by = 'AVG Score', ascending = False)[:1000]
                                                         
def rank_length(rank_acts, length):    
    #short - 0-20, short-medium - 21-40, medium - 41-60, medium-long - 61-80, long - 81-100 percentiles
    top_ten_length = rank_acts
    top_ten_length['length_percentile'] = top_ten_length['Length'].rank(pct = True)
    top_ten_length.sort_values(by = "length_percentile")

    if length == 'short':
        return top_ten_length.sort_values(by = "length_percentile")[:int(rank_acts.shape[0] * .2)]
    elif length == 'short-medium':
        return top_ten_length.sort_values(by = "length_percentile")[int(rank_acts.shape[0] * .2): int(rank_acts.shape[0] * .4)]
    elif length == 'medium':
        return top_ten_length.sort_values(by = "length_percentile")[int(rank_acts.shape[0] * .4): int(rank_acts.shape[0] * .6)]
    elif length == 'medium-long':
        return top_ten_length.sort_values(by = "length_percentile")[int(rank_acts.shape[0] * .6): int(rank_acts.shape[0] * .8)]
    elif length == 'long':
        return top_ten_length.sort_values(by = "length_percentile")[int(rank_acts.shape[0] * .8): int(rank_acts.shape[0])]
    else:
        return top_ten_length.sort_values(by = "length_percentile")

def rank_popularity(rank_acts, popularity):    
    #obscure - 0-20, little-known - 21-40, medium - 41-60, well-known - 61-80, popular - 81-100 percentiles
    top_ten_popularity = rank_acts
    top_ten_popularity['popularity_percentile'] = top_ten_popularity.Popularity.rank(pct = True)
    top_ten_popularity.sort_values(by = "popularity_percentile")

    if popularity == 'obscure':
        return top_ten_popularity.sort_values(by = "popularity_percentile")[:int(rank_acts.shape[0] * .2)]
    elif popularity == 'little-known':
        return top_ten_popularity.sort_values(by = "popularity_percentile")[int(rank_acts.shape[0] * .2): int(rank_acts.shape[0] * .4)]
    elif popularity == 'medium':
        return top_ten_popularity.sort_values(by = "popularity_percentile")[int(rank_acts.shape[0] * .4): int(rank_acts.shape[0] * .6)]
    elif popularity == 'well-known':
        return top_ten_popularity.sort_values(by = "popularity_percentile")[int(rank_acts.shape[0] * .6): int(rank_acts.shape[0] * .8)]
    elif popularity == 'popular':
        return top_ten_popularity.sort_values(by = "popularity_percentile")[int(rank_acts.shape[0] * .8): int(rank_acts.shape[0])]
    else:
        return top_ten_popularity.sort_values(by = "popularity_percentile")
                                                        
def find_intersections(length, popularity):
    result = pd.merge(length, popularity, how = 'inner')
    return result.sort_values(by = 'AVG Score', ascending = False)[:10]

def create_ranking(desired_activity, desired_length, desired_popularity):
    rank_acts = rank_activity(desired_activity)
    #short - 0-20, short-medium - 21-40, medium - 41-60, medium-long - 61-80, long - 81-100 percentiles
    user_length_rank = rank_length(rank_acts, desired_length)
    #obscure - 0-20, little-known - 21-40, medium - 41-60, well-known - 61-80, popular - 81-100 percentiles
    user_popularity_rank = rank_popularity(rank_acts, desired_popularity)
    return find_intersections(user_length_rank, user_popularity_rank)#[['Trail', 'Park']]