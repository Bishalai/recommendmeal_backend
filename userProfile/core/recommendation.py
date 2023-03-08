import os
import re
import datetime 
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity



#DATAPATH = os.path.join(BASE_DIR, 'recommendation/datasets/custom/')
#--------some essential variables
DATAPATH = "C:/Users/Gaumati Khan/Downloads/minor/cool/userProfile/core/"
TODAY = datetime.date.today().strftime('%d/%m/%Y')
##users id which is passed 
##these dats are handled by the other developers
USER_NAME="bishal"
TIME = "breakfast"
RATING = 3

 ####--- read from csv files

def load_req_data(filename, data_path=DATAPATH):
    csv_path=os.path.join(data_path, filename)
    return pd.read_csv(csv_path, encoding='cp1252')


#foods = pd.read_csv("datasets/custom/food.csv", encoding='cp1252')
#users = pd.read_csv("datasets/custom/user_info.csv", encoding="cp1252")
foods = load_req_data("food.csv")
users = load_req_data("user_info.csv")
past_data = load_req_data("user_data.csv")


##-------functions required are stored here-------------------------------------------
##oads the csv file to the given variable as a pandas object
##oads the csv file to the given variable as a pandas object

def load_data_to_csv(filename, dataframe, data_path=DATAPATH):
    csv_path=os.path.join(data_path, filename)
    dataframe.to_csv(csv_path, mode = 'a',encoding='cp1252', index = False, header=False)
    return


def write_data_to_csv(filename, dataframe, data_path=DATAPATH):
    csv_path=os.path.join(data_path, filename)
    dataframe.to_csv(csv_path ,encoding='cp1252', index = False)
    return

##combines the values of the given columns
def combine_features(row):
    return row['name'] + " " + row['description'] + " " + row['ingredients'] + " " + row['diet']

##gets the name of the food from its index
##gets the name of the food from its index
def get_index_from_name(name):
    return foods[foods.name == name].index.values[0]

##gets the name of the food from its index
##gets the name of the food from its index
def get_name_from_index(index):
    return foods[foods.index==index]['name'].values[0]


##displays the food with its nutritional value in the index inputted(absolute index of the data)
def display_food(i):
    nutrition = foods[foods.index == i]['nutrition'].values[0]
    nut = list(map(float,nutrition.split(',')))
   
    print(f"{get_name_from_index(i)}: Energy = {nut[0]} KCal, \
Carbohydrate = {nut[1]} gm, Fats = {nut[2]} gm, Protein = {nut[3]} gm ")

#function to compare the value of the ith indexed row's column to the given string
def compare_with_foodvalue(i,column,string ):
    return foods[foods.index == i][column].values[0]==string

def user_datframe(user_name, date, time, food, rating):
    return pd.DataFrame(
        {
            'username':[user_name],
            'date':[date],
            'time':[time],
            'food':[food],
            'rating':[rating]
        }
    )

def food_dataframe(user_name, name, description, nutrition, ingredient, time, diet, type_food):
    return pd.DataFrame(
        {
            'username': [user_name], ##id of the user that creates the food
            'date': [date], ##must be in format %d%m%Y 
            'description': [description], ##force use to input a minimum of 5 words
            'nutrition':[nutrition], ##nutrition obtained from the calculate_macronutrients() function
            'ingredient':[ingredient], ##!!!!ingredients of the food, remove all the spaces in the string
            'time':[time], ##time=breakfast,lunch,dinner
            'diet':[diet], ##type of diet == vegetarian or non-vegetarian
            'type':[type_food]    ##type= staple or curry or alone
        }
    )

def user_dataframe(username,name,age,weight,height,sex,lifestyle,tags,diet,disease,allergy):
    return pd.DataFrame(
        {
            'username':[username],
            'name':[name],
            'age':[age],
            'weight':[weight],
            'height':[height],
            'sex':[sex],
            'lifestyle':[lifestyle],
            'tags':[tags],
            'diet':[diet],
            'disease':[disease],
            'allergy':[allergy]
        }
    )
    



##function to calculate the macronutrients of the list of ingredients
##obtained ingredient lits is a list of list with name of ingredient, wt in gms

##the obtained_ingredient list is obtained from the user along with the foods
# the customized food is stored in other datas, here we are only calculating the nutrients value
def calculate_macronutrients(obtained_ingredients_list):
    ##get our dats stored of ingredients
    ingredients_list = load_req_data("ingredients_list.csv")
    ingredients_list.fillna(0)
    ##energy, carb, fat, protein 
    macro_nut = [0,0,0,0]
    for item in obtained_ingredients_list:
        ing_value = ingredients_list.loc[ingredients_list['ingredient']==item[0]]
        ing_value['protein']=ing_value['protein'].astype(float)
        ing_value['energy']=ing_value['energy'].astype(float)
        macro_nut[0]=macro_nut[0]+(ing_value['energy'].values[0]*(item[1]/100))
        macro_nut[1]=macro_nut[1]+(ing_value['carbohydrate'].values[0]*(item[1]/100))
        macro_nut[2]=macro_nut[2]+(ing_value['fat'].values[0]*(item[1]/100))
        macro_nut[3]=macro_nut[3]+(ing_value['protein'].values[0]*(item[1]/100))
    return macro_nut



def calculate_user_macronutrients( user_name = USER_NAME):
    ##get the wt, age, height and lifestyle:
    ##select a row of user's data from user database
    current_user = users.loc[users['username']==user_name]
    ##calories energy, carbohydrate, fats, protein the macros have a low and upper range
    ##using hams benedict equation
    ##for male and female
    if(current_user['sex'].values[0]=='M'):
        bmr = 66.5 + (13.75*current_user['weight'].values[0]) + (5.003*current_user['height'].values[0]) - (6.75*current_user['age'].values[0])
    elif (current_user['sex'].values[0]=='F'):
        bmr = 655.1 + (9.53*current_user['weight'].values[0]) + (1.850*current_user['height'].values[0]) - (4.676*current_user['age'].values[0])
    else:
        bmr = 2000

    #for type of lifestyle
    # ###type of lifetyle:
    # sedentary=1.2
    # lightlyactive=1.375
    # moderateactive=1.55
    # veryactive=1.725
    # extraactive1.9

    if current_user['lifestyle'].values[0]=='sedentary':
        alpha = 1.2
    elif current_user['lifestyle'].values[0]=='lightlyactive':
        alpha = 1.375
    elif current_user['lifestyle'].values[0]=='moderateactive':
        alpha = 1.55
    elif current_user['lifestyle'].values[0]=='veryactive':
        alpha = 1.725
    elif current_user['lifestyle'].values[0]=='extraactive':
        alpha = 1.9

    ##calories energy, carbohydrate, fats, protein the macros have a low and upper range
    current_user_calories = alpha*bmr
    current_user_macro=[current_user_calories]
    ##adding carbs 45-60% in gms
    current_user_macro.append((current_user_calories*.45)/4)
    current_user_macro.append((current_user_calories*.60)/4)
    ##adding fat 20-35% in gms
    current_user_macro.append((current_user_calories*.20)/9)
    current_user_macro.append((current_user_calories*.35)/9)
    ##adding protein 10-35% in gms
    current_user_macro.append((current_user_calories*.10)/4)
    current_user_macro.append((current_user_calories*.35)/4)

    for i in range(len(current_user_macro)):
        current_user_macro[i] = round(current_user_macro[i],3)

    return current_user_macro

##check veg function, takes sorted similar foods' list and removes foods based on user's diet
def check_veg(sorted_similar_foods, user_name=USER_NAME):
    ##-- now filter out the ones that are veg or non veg, allergies and disease
    if users[users['username']==user_name]['diet'].values[0] == "vegetarian":
        for food in sorted_similar_foods[:]:
            if foods[foods.index == food[0]]['diet'].values[0]=="non-vegetarian":
                #print(get_name_from_index(food[0]), "is removed")
                sorted_similar_foods.remove(food)
    return sorted_similar_foods


##check for ingrediients to be excluded as in allergy or diaseases
def check_allergy(sorted_similar_foods, user_name = USER_NAME):
    ## this must be tailored for user// change after disease database added
    ##get our dataset where we have the diseases and their ingredients to avoid
    diseases=load_req_data('disease_list.csv')
    # we dont want to deal with nans
    diseases.fillna('placeholder',inplace=True)
    ##get the data of current user
    current_user = users.loc[users['username']==user_name]
    current_user.fillna('placeholder',inplace = True)
    ##first take allergic ingredients
    excluded = current_user['allergy'].values[0]
    #map them into list of string, maybe one or more
    excluded = list(map(str,excluded.split(',')))
    ##do similar things with the diseases user have
    user_disease = current_user['disease'].values[0]
    print(user_disease)
    dis = list(map(str,user_disease.split(',')))
    ##for items in dis we get their respective ingredients
    for item in dis:
        if item!="placeholder":
            #get ingredients and map them into list and combine with our allergies data
            tmp_disease = diseases[diseases['disease']==item]['excluded_ingredients'].values[0]
            tmp_disease = list(map(str,tmp_disease.split(',')))
            excluded = excluded + tmp_disease
            ## we have our ingredients to exclude// even if we get 'placeholder' value it is alright since placeholder
    ##is not an ingredient so it doesnt matter and wont be excluded
    exclude_ingredients = excluded
    # ##check for disease or allergy in ingredients
    for food in sorted_similar_foods[:]:
        ##make a list of string of the ingredients of food
        ingredients = (foods[foods.index == food[0]]['ingredients'].values[0])
        ingred = list(map(str,ingredients.split(',')))
        #print(ingred)
        ##check if the list of ingredients in food contains the ingredients user must avoid
        for item in exclude_ingredients: ##here we use the list of ingredients user should not eat
            if(item in ingred):
                #print(get_name_from_index(food[0])," is removed")
                sorted_similar_foods.remove(food)
                break
    return sorted_similar_foods


def check_time(sorted_similar_foods, time = TIME):
    #print("-----------------------------\nremoving based on time")
    ##check for the food time i.e. foods associated with lunch is only taken during lunch
    for food in sorted_similar_foods[:]:
        time_food = (foods[foods.index == food[0]]['time'].values[0])
        time_food_list = list(map(str,time_food.split(',')))
        if time not in time_food_list:
            #print(get_name_from_index(food[0])," is removed")
            sorted_similar_foods.remove(food)
    return sorted_similar_foods


def remove_recently_recommended(sorted_similar_foods,past_data, user_name=USER_NAME):
    ##filter out last five previously recommended
    ##convert date from database to datetime object
    past_data['date']=pd.to_datetime(past_data['date'], dayfirst=True)
    ##sort based on date and user_id
    past_data.sort_values(['date','username'], inplace=True)
    ##get the datas for the current user
    past_data = past_data.loc[past_data['username'] == user_name]
    ##get the 5 most recent datas
    past_data = past_data.tail(5)
    ##now check if the recommended are in the list 
    for item in sorted_similar_foods[:]:
        if get_name_from_index(item[0]) in past_data['food'].values:
            #print(get_name_from_index(item[0]),"is removed")
            sorted_similar_foods.remove(item)
    #get name from index i [0] == past_data['food'].values
    return sorted_similar_foods


def display_final_recommendation(sorted_similar_foods):
    print("---------------------------\n Final top recommendation")
    ##show the final result
    ##nutrition calculation part left
        ###checking or doing calculation of nutrition is left
  
    display_food(sorted_similar_foods[0][0])
    rec_food=get_name_from_index(sorted_similar_foods[0][0])
    ##if the top rec food is a staple food then recommend the highest similar curry
    if compare_with_foodvalue(sorted_similar_foods[0][0], 'type', 'staple'):
        for item in sorted_similar_foods:
            if compare_with_foodvalue(item[0], 'type', 'curry'):
                display_food(item[0])
                rec_foods = rec_food + ',' + get_name_from_index(item[0])
                break
    elif compare_with_foodvalue(sorted_similar_foods[0][0], 'type', 'curry'):
        ####same wise if top recommended is a curry then recommend a companion staple food
        for item in sorted_similar_foods:
            if compare_with_foodvalue(item[0], 'type', 'staple'):
                display_food(item[0])
                rec_foods = rec_food + ',' + get_name_from_index(item[0])
                break


def merge_dict(d1,d2):
    ds = [d1, d2]
    d = {}
    for k in d1.keys():
        d[k] = tuple(d[k] for d in ds)
    return d


def get_final_rec(sorted_similar_foods):
    d1 = foods.loc[foods.index==sorted_similar_foods[0][0]]
    d1 = d1.to_dict('list')
    d2={}
    ##if the top rec food is a staple food then recommend the highest similar curry
    if compare_with_foodvalue(sorted_similar_foods[0][0], 'type', 'staple'):
        for item in sorted_similar_foods:
            if compare_with_foodvalue(item[0], 'type', 'curry'):
                d2 = foods.loc[foods.index==item[0]]
                d2 = d2.to_dict('list')
                break
    elif compare_with_foodvalue(sorted_similar_foods[0][0], 'type', 'curry'):
        ####same wise if top recommended is a curry then recommend a companion staple food
        for item in sorted_similar_foods:
            if compare_with_foodvalue(item[0], 'type', 'staple'):
                d2 = foods.loc[foods.index==item[0]]
                d2 = d2.to_dict('list')
                break
    if d2!={}:
        d = merge_dict(d1, d2)
    else:
        d = d1
    return d        

def update_userdata(rec_food,time=TIME, rating=RATING, user_name = USER_NAME):
    past_data = load_req_data("user_data.csv")
    past_data['date']=pd.to_datetime(past_data['date'], dayfirst=True)
    ##sort based on date and user_id
    past_data.sort_values(['date'], inplace=True)
    ##get the datas for the current user
    past_data = past_data.loc[past_data['username'] == user_name]
    ##get the 3 most recent datas
    past_data = past_data.tail(3)
    if len(past_data)>3:
        for item in past_data:
            if past_data['date'].values[0] == TODAY and past_data['time'].values[0]==time:
                #print(get_name_from_index(item[0]),"is removed")
                return
            else:
        
                ##user data: user_id, date, time, food, ratings
                # rec_food = get_name_from_index(sorted_similar_foods[0][0])
                updated = user_datframe(user_name, TODAY, time, rec_food, rating)
                load_data_to_csv('user_data.csv', updated)
                return
    
    else:
        # rec_food = get_name_from_index(sorted_similar_foods[0][0])
        updated = user_datframe(user_name, TODAY, time, rec_food, rating)
        load_data_to_csv('user_data.csv', updated)
        return


def remove_duplicates(filename):
    df = load_req_data(filename)
    # Notes:
    # - the `subset=None` means that every column is used 
    #    to determine if two rows are different; to change that specify
    #    the columns as an array
    # - the `inplace=True` means that the data structure is changed and
    #   the duplicate rows are gone  
    df.drop_duplicates(subset=['username','date','time'], inplace=True)

    # Write the results to a file
    csv_path=os.path.join(DATAPATH, filename)
    df.to_csv(csv_path,encoding='cp1252', index=False)


def remove_duplicate_users(filename):
    df = load_req_data(filename)
    # Notes:
    # - the `subset=None` means that every column is used 
    #    to determine if two rows are different; to change that specify
    #    the columns as an array
    # - the `inplace=True` means that the data structure is changed and
    #   the duplicate rows are gone  
    df.drop_duplicates(subset=['username'], inplace=True)

    # Write the results to a file
    csv_path=os.path.join(DATAPATH, filename)
    df.to_csv(csv_path,encoding='cp1252', index=False)

#----------------------------------------------------------------------------------------
#end of functions section
##------------------------------------------------------------------------------------

##main dfunction
def recommendmeal(time=TIME, rating=RATING, username = USER_NAME):

    print("User is: ", users.loc[users['username']==username]['name'].values[0])

    ##----select our tags and features

    food_features = ['name','description','ingredients','diet']
    user_features = ['tags'] ##the tags must have as many words as possible to describe 
                                #user acurately and must be upated regularly

    ##----combine features into a new dataframe
    features = foods.apply(combine_features, axis = 1)
    user_tag = users['tags'].loc[users['username']==username]

    ##add user tags to the end of list of features
    newfeatures = pd.concat([features, user_tag], ignore_index=True)

    ###-----count matrix
    cv = CountVectorizer(stop_words='english')
    count_matrix = cv.fit_transform(newfeatures)

    ###----compute cosine similarity
    cosine_sim = cosine_similarity(count_matrix)

    ###similar foods in descending order
    ##take the user's similar data
    similar_foods = list(enumerate(cosine_sim[-1]))

    ##remove the last value since it is 1 i.e. value of user which wont be found in food.csv
    similar_foods.remove(similar_foods[-1])
    ##sort the list in descending order i.e. from most simlar to least similar

    sorted_similar_foods = sorted(similar_foods,key=lambda x:x[1],reverse = True)

    ##show top 5 most recommended
    # print("first batch of recommended without any constraints")
    # for i in range(0,6):
    #    print(get_name_from_index(sorted_similar_foods[i][0]))

    ##removing non veg items for veg users
    sorted_similar_foods = check_veg(sorted_similar_foods,  user_name=username)

    ##remove foods that contain ingredients that isnot suitable for user
    sorted_similar_foods = check_allergy(sorted_similar_foods, user_name=username)

    ##remove foods not suitable for the current time i.e. breakfast, lunch, dinner
    sorted_similar_foods = check_time(sorted_similar_foods, time = time)

    ##remove 5 recently recommended foods
    sorted_similar_foods = remove_recently_recommended(sorted_similar_foods, past_data, user_name=username)

    ##display the top recommended
    ##if it is curry, also search the most recommended staple food
    ##of it is staple, also search the most recommended curry food
    display_final_recommendation(sorted_similar_foods)

    # ##user data: user_id, date, time, food, ratings
    # rec_food = get_name_from_index(sorted_similar_foods[0][0])
    # updated = user_datframe(user_id, TODAY, time, rec_food, rating)
    # #!!!!!! use this function below if you want to update to csv the current user data
  
    #load_data_to_csv('user_data.csv', updated)

    #update_userdata(sorted_similar_foods = sorted_similar_foods, user_id= user_id, rating=rating, time=time)
    
    d = get_final_rec(sorted_similar_foods)
    return d

def give_rating(rec_food, user_name=USER_NAME, time=TIME, rating=RATING):
    rec_food = ''.join(rec_food)
    update_userdata(rec_food=rec_food, user_name= user_name, rating=rating, time=time)
    remove_duplicates('user_data.csv')

    


#recommendmeal()

# ###use the function to calculate macronutrition
# obtained_ingredients_list = [['Amaranth seed', 25],['Paneer', 20],['Curd', 40]]
# macro_nut = calculate_macronutrients(obtained_ingredients_list)
# print(f"{obtained_ingredients_list} has macro nutrients:")
# print(f"Energy: {macro_nut[0]}Kcal, Carbohydrates: {macro_nut[1]}gm, Fats: {macro_nut[2]}gm, Protein: {macro_nut[3]}gm")


# ##calculate recommended user macro nutrients:
# ##get the info of macronutrients for the current user using function
# current_user_macro = calculate_user_macronutrients()

# ##print the macronutrients values
# print("For the user:",users[users['user_id']==USER_ID]['name'].values[0].capitalize()," The macronutrients:")
# print(f"Energy:{current_user_macro[0]} Kcal")
# print(f"Carbohydrates:{current_user_macro[1]} to {current_user_macro[2]} gms")
# print(f"Fats:{current_user_macro[3]} to {current_user_macro[4]} gms")
# print(f"Proteins:{current_user_macro[5]} to {current_user_macro[6]} gms")



# ####this is a basic version so far a lot more things need to added and organised which will be done tomorrow
'''
list of things to be added
-nutrition calculation(tougher than I thought)!!!!!(didnt go as thought...but DONE!!)
-dynamic upgarding of tags(add words to tag as time passes by)!!!!(someone do it!)
-improved database!
-let the users add their own foods with ingredients whose nutrition is calculated by the fucntion above
-record history of users in their personal database!!! (DONE!)
-using history remove the recently recommended dishes(must improve catalogue of dishes for this)!!!!(DONE)
-think of a scaling alternative as this doesnt scale well for big datas!!<><>(later!)
-encryption of user's sensitive info!!!(someone do it!)
-make a diseases database that contains ingredients not to use!!!!(DONE, needs improvement)
DISCARDED!(someone handle it)
-implement these code in their functions!!<><><>
-implement in class if possible, otherwise not necessary!<><><>
'''

##[energy(Cal), carbohydrate(gm),fats(gm),protein(gm)]
# nutrition = foods[foods.index == 2]['nutrition'].values[0]
# nut = list(map(float,nutrition.split(',')))
# print(type(nut))