import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import bs4 as bs

data = pd.read_csv('datasets/final_data.csv')
cv=CountVectorizer()
count_matrix = cv.fit_transform(data['comb'])
# creating a similarity score matrix
csimilarity = cosine_similarity(count_matrix)


def rcmd(id):
    id = int(id)
    if id not in data['id'].unique():
        return (
            'Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')
    else:
        i = data.loc[data['id'] == id].index[0]
        lst = list(enumerate(csimilarity[i]))
        lst = sorted(lst, key=lambda x: x[1], reverse=True)
        lst = lst[1:13]  # excluding first item since it is the requested movie itself
        l = {"titles":[],"ids":[]}
        for i in range(len(lst)):
            a = lst[i][0]
            l["titles"].append(str(data['movie_title'][a]))
            l["ids"].append(str(data['id'][a]))
        return l


# converting list of string to list (eg. "["abc","def"]" to ["abc","def"])
def convert_to_list(my_list):
    my_list = my_list.split('","')
    my_list[0] = my_list[0].replace('["', '')
    my_list[-1] = my_list[-1].replace('"]', '')
    return my_list


def get_suggestions():
    data = pd.read_csv('main_data.csv')
    return [x.upper() for x in list(data['movie_title'].str.capitalize())]

#Category wise list
def category(c):
    data = pd.read_csv('main_data.csv')
    data_cat = data[data['genres'].str.lower().str.contains(c.lower()).fillna(False)]
    data_cat = data_cat.sort_values(by=['year'], ascending=False)
    data_cat = data_cat['movie_title'].tolist()[0:12]
    return data_cat


app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    suggestions = get_suggestions()
    return render_template('home.html', suggestions=suggestions)

@app.route("/id_by_title",methods=['POST'])
def id_by_title():
    title=request.form['title'].lower()
    result=str(data[data['movie_title']==title]['id'].iloc[0])
    print(title,result)
    return result


@app.route("/aboutus")
def aboutUs():
    return render_template('about_us.html')

@app.route("/category",methods=["POST"])
def filter_by_category():
    cat = request.form['category']
    gc = category(cat)
    if type(gc)==type('string'):
        return gc
    else:
        c_str="---".join(gc)
        return  c_str

@app.route("/similarity", methods=["POST"])
def similarity():
    movie = request.form['name']
    rc = rcmd(movie)
    if type(rc) == type('string'):
        return rc
    else:
        #m_str = "---".join(rc)
        return jsonify(rc)


@app.route("/recommend", methods=["POST"])
def recommend():
    # getting data from AJAX request
    title = request.form['title']
    cast_ids = request.form['cast_ids']
    cast_names = request.form['cast_names']
    cast_chars = request.form['cast_chars']
    cast_bdays = request.form['cast_bdays']
    cast_bios = request.form['cast_bios']
    cast_places = request.form['cast_places']
    cast_profiles = request.form['cast_profiles']
    imdb_id = request.form['imdb_id']
    poster = request.form['poster']
    genres = request.form['genres']
    overview = request.form['overview']
    vote_average = request.form['rating']
    vote_count = request.form['vote_count']
    release_date = request.form['release_date']
    runtime = request.form['runtime']
    status = request.form['status']
    rec_movies = request.form['rec_movies']
    rec_posters = request.form['rec_posters']

    # get movie suggestions for auto complete
    suggestions = get_suggestions()

    # call the convert_to_list function for every string that needs to be converted to list
    rec_movies = convert_to_list(rec_movies)
    rec_posters = convert_to_list(rec_posters)
    cast_names = convert_to_list(cast_names)
    cast_chars = convert_to_list(cast_chars)
    cast_profiles = convert_to_list(cast_profiles)
    cast_bdays = convert_to_list(cast_bdays)
    cast_bios = convert_to_list(cast_bios)
    cast_places = convert_to_list(cast_places)

    # convert string to list (eg. "[1,2,3]" to [1,2,3])
    cast_ids = cast_ids.split(',')
    cast_ids[0] = cast_ids[0].replace("[", "")
    cast_ids[-1] = cast_ids[-1].replace("]", "")

    # rendering the string to python string
    for i in range(len(cast_bios)):
        cast_bios[i] = cast_bios[i].replace(r'\n', '\n').replace(r'\"', '\"')

    # combining multiple lists as a dictionary which can be passed to the html file so that it can be processed easily and the order of information will be preserved
    movie_cards = {rec_posters[i]: rec_movies[i] for i in range(len(rec_posters))}

    casts = {cast_names[i]: [cast_ids[i], cast_chars[i], cast_profiles[i]] for i in range(len(cast_profiles))}

    cast_details = {cast_names[i]: [cast_ids[i], cast_profiles[i], cast_bdays[i], cast_places[i], cast_bios[i]] for i in
                    range(len(cast_places))}
    
    return render_template('recommend.html', title=title, poster=poster, overview=overview, vote_average=vote_average,
                           vote_count=vote_count, release_date=release_date, runtime=runtime, status=status,
                           genres=genres,
                           movie_cards=movie_cards, casts=casts, cast_details=cast_details)

@app.route("/display_category",methods=["POST"])
def display_category():
    cat_movies = request.form['cat_movies']
    cat_posters = request.form['cat_posters']

    category = request.form['category']

    cat_movies = convert_to_list(cat_movies)
    cat_posters = convert_to_list(cat_posters)

    movie_cards = {cat_posters[i]: cat_movies[i] for i in range(len(cat_posters))}

    return render_template('category.html', category=category, movie_cards=movie_cards)

if __name__ == '__main__':
    app.run(port=5002, debug=True)