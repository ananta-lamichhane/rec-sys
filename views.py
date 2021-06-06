from flask import render_template, Blueprint, request, url_for, send_from_directory
from flask_login import login_required, login_user, logout_user, current_user
from flask_user import roles_required
from werkzeug.utils import redirect
from flask_security.utils import hash_password, verify_password
from sqlalchemy import desc, func, asc

import json
import pandas as pd
import os


from utils.select_survey_items import select_movies_for_survey
from utils.serve_posters import generate_movie_info, load_next_movie

main_bp = Blueprint('main', __name__)  # needs to be here

from database.user_model import User,  Study, Rating, Item, Crossvalidation, Item_Genres, Study_Algorithms, Algorithm, Dataset, user_datastore, Evaluation,ReclistItem, Reclist
from application import db


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    #login_database.session.query(Rating).filter(Rating.user_id == current_user.id).delete()
    #login_database.session.commit()
    return render_template("home.html")


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #take data from form
        token_nr = request.form.get('token_number')
        user_password = request.form.get('password')

        u = User.query.filter_by(token_id=token_nr).first()
        # check if user u already exists
        if u and u.password == user_password:
            login_user(u)
            if u.token_id == 9999 and u.name == 'admin': #if the logged in user is admin go directly to admin page
                return redirect(url_for('main.admin'))
            return redirect(url_for('main.survey'))
        else:
            text = "This user does not exist. Please login with valid credentials."
            return render_template('forbidden.html', text=text)

    return render_template("login.html")


@main_bp.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    no_of_questions=10 ## number of survey questionnaires, we can query it from database later.
    if request.method == "POST":
        dont_know = request.form.get('dont_know')
        print(f'dont know value {dont_know}')
        if request.form.get('formtype') == "2" and int(request.form.get('next_item')) < no_of_questions and dont_know== '0':  ## form is submitting movie ratings.
            imdb_id = request.form.get('imdb_id')
            next_item = request.form.get('next_item')
            #print("next item "+ str(next_item))
           # print("imdb id :  " + imdb_id)
            rating = request.form.get('rating')
            itemid = db.session.query(Item).filter_by(imdb_id=imdb_id).first().id #what item is the imdb id from submission referring to?
            print("----------------------------DATABASE ACTION---------------------------------------------")
            if db.session.query(Rating).filter_by(user_id=current_user.id, item_id=itemid).first(): #if rating associated with this user and this item alredy exists.
                print("Entry already exists: update rating")
                db.session.query(Rating).filter_by(user_id=current_user.id, item_id = itemid).first().rating = rating #then update rating
                db.session.commit()  ## commit to db
            else:
                print("Entry does not exist: create new rating")
                db.session.add(Rating(rating=rating, dataset_id=1, item_id=itemid, user_id=current_user.id))# else create new entry
                db.session.commit()  ## commit to db
            # we can query currently saved rating to current user from database.
            print("Entries in the database are:")
            current_ratings = db.session.query(Rating).filter_by(user_id=current_user.id) ##get all ratings assciated with this user
            for r in current_ratings:
                print("rating: " + str(r.rating) + " movieId: " + str(r.item_id))
            print("----------------------------END DATABASE ACTION---------------------------------------------")


            ## Logic to implement for the next movie
            #It just queries the Items column and returns next Item from the db.
            currnt_movieId = db.session.query(Item).filter_by(imdb_id=imdb_id).first().id
            next_movieId  = db.session.query(Item).order_by(Item.id.asc()).filter(Item.id > currnt_movieId).first().id

            #print("current movie id : " + str(currnt_movieId) + "next imdb id : " + str(next_movieId))
            next_imdbId = db.session.query(Item).filter_by(id=next_movieId).first().imdb_id
            poster_url = generate_movie_info(next_imdbId)

            #print("current imdbid : " + imdb_id + "next imdb id : " + next_imdbId)
            return poster_url  # return the json data as it is so ajax can handle it instead


        # if request.form.get('formtype') == "1":
        #     redirect('/recommendations', code=302)
        # if request.form.get('formtype') == "3":  ## debugging database addition errors.
        #     #login_database.session.query(Rating.)
        #     current_ratings = json.loads(current_user.ratings) ## load the dict with rating entries for current user.
        #     current_ratings[imdb_id] = rating ## add to the dict
        #     current_user.ratings = json.dumps(current_ratings)  ## make json string of the dict
        #     login_database.session.commit() ## commit to db
        #     print("current rating str: " + str(current_user.ratings))
        # if request.form.get('formtype') == "1":
        #     print(current_user.email)
        #     print(current_user.ratings)
        # if request.form.get('formtype') == "3": ## debugging database addition errors.
        #     print("add online users")
        # if request.form.get('formtype') == "1":
        #     redirect('/recommendations', code=302)
        # if request.form.get('formtype') == "3": ## debugging database addition errors.
        #     current_user.ratings = '{}' ## reset the dict
        #     login_database.session.commit()
        #     print(current_user.ratings)

    # test_ids = select_movies_for_survey()
    test_id = 'tt0103859'##seed the first movie to be displayed
    poster_url = generate_movie_info(test_id) #get jason data from omdb
    return render_template("survey.html", poster_url=poster_url)


@main_bp.route('/bye')
@login_required
def bye():
    logout_user()
    return render_template("bye.html")


@main_bp.route('/about')
def about():
    return render_template("about.html")


# @main_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         # if request.form.validate_on_submit():
#         user_email = request.form.get('email')
#         user_name = request.form["name"]
#         user_password = hash_password(request.form.get('password'))  ## password is hashed and salted
#
#         print(user_password)
#
#         ## new model says account instead of email
#         u = User.query.filter_by(account=user_email).first()
#         # check if user u already exists
#         if u:
#             flash("A user with this email already exists. please log in.")
#             return redirect('login')
#         else:
#             login_database.session.add(User(account=user_email, name=user_name, password=user_password))
#             login_database.session.commit()
#
#     return render_template("register.html")


@main_bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    admin_tokenid= db.session.query(User).filter_by(name='admin').first().token_id
    if current_user.token_id == admin_tokenid:## allow access only if admin
        if request.method == 'POST':
            if request.form.get('db-action') == "Add Users":
                last_token_id = db.session.query(func.max(User.token_id))
                print("add users")
                for u in range(2, 52):
                    user_datastore.create_user(token_id=u, name='user' + str(u), password='password', online_user=True)
                    db.session.commit()
            if request.form.get('db-action') == "Populate Database":
                ##open the files
                ratings_file = os.path.realpath('./database/datasets/movielens_small/ratings.csv')
                movies_file = os.path.realpath('./database/datasets/movielens_small/movies.csv')
                links_file = os.path.realpath('./database/datasets/movielens_small/links.csv')
                recoms_file_svd = os.path.realpath('./database/datasets/movielens_small/recom_svd_ds1.csv')
                reclistdf_svd = pd.read_csv(recoms_file_svd, dtype='str')
                recoms_file_knn = os.path.realpath('./database/datasets/movielens_small/recom_knn_ds1.csv')
                reclistdf_knn = pd.read_csv(recoms_file_knn, dtype='str')


                ##load as dataframes
                movies_df = pd.read_csv(movies_file, dtype='str')
                links_df = pd.read_csv(links_file, dtype='str')
                ratings_df = pd.read_csv(ratings_file, dtype='str')
                #user names are numbers going up from 1 to max of the column add them to db
                print('#################### CREATING OFFLINE USERS ##################################')
                for u in range(ratings_df['userId'].astype('int').max() + 1): #find out max userId from the loaded dataset
                    ## add users to database
                    user_datastore.create_user(online_user=False, dataset_id=1) ## dataset Id can be queried from DB later.

                print('#################### ADDING MOVIES ##################################')
                for row in movies_df.itertuples():  ## add all movies to db
                    imdb_id = 'tt' + links_df.loc[links_df['movieId'] == row.movieId]['imdbId'].to_string(index=False)
                    db.session.add(
                        Item(id=row.movieId, name=row.title, imdb_id=imdb_id, dataset_id=1, poster_url="empty"))
                    db.session.commit()
                print('#################### ADDING RATINGS ##################################')
                for row in ratings_df.itertuples():  ## add all the ratings to the db
                    db.session.add(
                        Rating(rating=row.rating, dataset_id=5, item_id=row.movieId, user_id=row.userId))
                    db.session.commit()
                # survey_name = request.form.get('studies')
                survey_name = request.form.get('survey-name')
                print('#################### ADDING SURVEY DETAILS ##################################')
                db.session.add(Study(description="", name=survey_name, dataset_id=1))
                db.session.commit()

                db.session.query(ReclistItem).delete()
                db.session.commit()
                all_movies = Item.query.all()
               # for movie in all_movies:  ##add a reclistitem for all movies in db
                #    login_database.session.add(ReclistItem(item_id=movie.id))
                 #   login_database.session.commit()

                print("-------------------POPULATE RATINGS KNN------------------------")

                for row in reclistdf_knn.itertuples():  # each row corresponds to userid,recom1,recom2,recom3......,recom10
                    current_reclist = db.session.query(Reclist).filter_by(user_id=int(row[0]),
                                                                          algorithm_id=1).first()
                    if not current_reclist:
                        db.session.add(
                            Reclist(user_id=int(row[0]), algorithm_id=1))  # create a reclist for each row of recoms
                        db.session.commit()
                        current_reclist = db.session.query(Reclist).filter_by(user_id=int(row[0]),
                                                                              algorithm_id=1).first()

                    for item in row[2:]:  # skip the first item on row, i.e. the user id.
                        # print(item)
                        current_reclistitem = db.session.query(ReclistItem).filter_by(item_id=int(item),
                                                                                      reclist_id=current_reclist.id).first()
                        #  print("current_reclistitem = " + str(current_reclistitem))
                        if not current_reclistitem:
                            db.session.add(ReclistItem(item_id=int(item), reclist_id=int(row[0])))
                            db.session.commit()

                        # print("-")
                        #  login_database.session.add(ReclistItem(item_id=int(item)))
                        #   login_database.session.commit()
                        else:
                            # print("item")

                            # print("add reclistid=userid to the reclistitem")
                            current_reclistitem.reclist_id = current_reclist.id
                            db.session.commit()
                print("-------------------------------POPULATE RECLIST SVD--------------------------------------")

                for row in reclistdf_svd.itertuples():  # each row corresponds to userid,recom1,recom2,recom3......,recom10
                    current_reclist = db.session.query(Reclist).filter_by(user_id=int(row[0]),
                                                                          algorithm_id=2).first()
                    if not current_reclist:
                        db.session.add(
                            Reclist(user_id=int(row[0]), algorithm_id=2))  # create a reclist for each row of recoms
                        db.session.commit()
                        current_reclist = db.session.query(Reclist).filter_by(user_id=int(row[0]),
                                                                              algorithm_id=2).first()

                    for item in row[2:]:  # skip the first item on row, i.e. the user id.
                        # print(item)
                        current_reclistitem = db.session.query(ReclistItem).filter_by(item_id=int(item),
                                                                                      reclist_id=current_reclist.id).first()
                        #  print("current_reclistitem = " + str(current_reclistitem))
                        if not current_reclistitem:
                            db.session.add(ReclistItem(item_id=int(item), reclist_id=current_reclist.id))
                            db.session.commit()

                        # print("-")
                        #  login_database.session.add(ReclistItem(item_id=int(item)))
                        #   login_database.session.commit()
                        else:
                            # print("item")

                            # print("add reclistid=userid to the reclistitem")
                            current_reclistitem.reclist_id = current_reclist.id
                            db.session.commit()


        print("------------------------------DONE POPULATING DATABASE-----------------------------------")
        return render_template("admin.html")
    text= "Your are not authorized to visit this page. Please log in as administrator."
    return render_template('forbidden.html', text=text) #if not admin deny access




@main_bp.route('/recommendations', methods=['GET', 'POST'])
@login_required
def recommend():

    if request.method == 'POST': # if reating is submited
        serendipity_rating = float(request.form.get('rating'))
        reclist_id = int(request.form.get('reclist_id'))


        '''when an item is selected for recommendation, a reclistitem must be created with it
        many reclistitems will be added a reclist and will be populated with userid and algo id
        after submit form, the rating of recommendation should populate an evaluation with the values.'''

        print("-------------------START DATABASE ENTRY---------------------------------")
        current_evaluation = db.session.query(Evaluation).filter_by(reclist_id=reclist_id, user_id=current_user.id).first()
        if current_evaluation:
            current_evaluation.serendipity= serendipity_rating
            db.session.commit()
        else:
            db.session.add(Evaluation(serendipity=serendipity_rating, reclist_id=reclist_id, user_id=current_user.id))
            db.session.commit()

        print("evaluation of recommendation list no. " + str(reclist_id) + " = " + str(db.session.query(Evaluation).filter_by(reclist_id=reclist_id, user_id=current_user.id).first().serendipity))
        print("--------------------------------END DATABASE ENTRY------------------------------")
    #query database for recommendation lists for a user belonging to a particular user
    reclist_svd = db.session.query(Reclist).filter_by(user_id=402 + current_user.token_id, algorithm_id=2).first()
    reclist_knn = db.session.query(Reclist).filter_by(user_id=402 + current_user.token_id, algorithm_id=1).first()
    print("reclist knn: " + str(reclist_knn.id) + " reclist svd: "+ str(reclist_svd.id))


    #find reclistitems (movies) that belong to each recommendation groups
    reclistitems_svd = db.session.query(ReclistItem).filter_by(reclist_id=reclist_svd.id)
    reclistitems_knn = db.session.query(ReclistItem).filter_by(reclist_id=reclist_knn.id)



    ## recommendations = highest rated movies by the user most similar to the current user, e.g. user no 483
    all_data_svd = [] ## accumulate top recommendations for each algo type here.
    all_data_knn = []
    for recitem in reclistitems_knn:
        imdb_no = db.session.query(Item).filter_by(id=recitem.item_id).first().imdb_id
        if len(all_data_knn) ==5:
            break
        movie_data = generate_movie_info(imdb_no)
        all_data_knn.append(movie_data)
    for recitem in reclistitems_svd:
        imdb_no = db.session.query(Item).filter_by(id=recitem.item_id).first().imdb_id
        if len(all_data_svd) ==5:
            break
        movie_data_svd = generate_movie_info(imdb_no) #caution:generate_poster_url_dict(generates a dict will all data pertaining to the movie)
        all_data_svd.append(movie_data_svd)
    #pass two lists with movie information to html, need to get recids back from html too
    print("Movies suggested by Algorithm 1")
    print("-----------------------------------------------------------------------------")

    for movie in all_data_knn:
        print(movie['title'])
    print("-----------------------------------------------------------------------------")
    print("Movies suggested by Algorithm 2")
    print("-----------------------------------------------------------------------------")

    for movie in all_data_svd:
        print(movie['title'])
    print("-----------------------------------------------------------------------------")

    return render_template('recommendations.html', poster_urls1=all_data_knn, poster_urls2=all_data_svd, reclist_id1=reclist_svd.id, reclist_id2=reclist_knn.id)

# @main_bp.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(main.app.root_path, 'static'), 'static/favicon.ico', mimetype='image/vnd.microsoft.icon')