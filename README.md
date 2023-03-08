# recommendmeal_backend
urls = [
    path('signup',SignUpView),
    path('signin',SignInView),
    path('signout',SignOutView),
    path('userdetails', UserDetails),
    path('csrf_cookie',GetCSRFToken),
    path('authenticated',CheckAuthenticatedView),
    path('recommended',RecommendMealView),
    path('ratemeal',RateMealView),
    path('gethistory',GetHistoryView)
]

!!csrf tokenss and session authentication is used in this project

getcsrftoken: gets csrf token required for signup/ sign_in
isauthenticaed: checks if user is authenticated

signup: registers new users
the data fields required are: method POST
username,email, password1, password2, age, weight, height, sex, lifestyle, tags, diet, disease, allergy

signin: existing users login
required fields: method POST
username, password

signout: signout method POST


recommendmeal:
method POST
required field: time = breakfast, lunch or dinner
gets  "user":user.username,
      "time":data['time'],
      "nutrition format" : "energy(kcal),carbohydrate(gm),fats(gm),protein(gm)",
      "recommended calories": macro_nut[0],
      "recommended carbohydrates(gm) min":macro_nut[1],
      "recommended carbohydrates(gm) max":macro_nut[2],
      "recommended fats(gm) min":macro_nut[3],
      "recommended fats(gm) max":macro_nut[4],
      "recommended protein(gm) min":macro_nut[5],
      "recommended protein(gm) max":macro_nut[6],
      "food":rec_food -> gives name,id,description,nutrition,ingredients,time,diet,type(is is useless)
      
      
      
 ratemeal: POST
 required field: rating, time, food_name.. stored from recommend meal 
 stores the rating and history of user
 
 
 userhistory:
 method POST
 gets back user history for the user in current session:
 date, time, food, rating
 
 
 
 
 userdetails
 method PUT-> updates user details
 method DELETE-> deletes user and its associated profile and data
 method POST-> gets user info
 
 
 
 ------ other functionalities are yet to be added:
 user custom meal, ingredients based recommendation
 
