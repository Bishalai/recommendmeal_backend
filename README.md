
 ### - [recommendmeal\_backend](#recommendmeal_backend)
- [urls:](#urls)
- [signup:](#signup)
- [signin:](#signin)
- [signout:](#signout)
- [recommendmeal:](#recommendmeal)
- [ratemeal:](#ratemeal)
- [userhistory:](#userhistory)
- [userdetails](#userdetails)
- [epilogue](#epilogue)
 
 
 



## urls:

The urls paths are

| urls       | description                                              |
| ---------- | -------------------------------------------------------- |
| signup     | register user                                            |
| signin     | authenticate user and return jwt token                   |
| signout    | signsout user(need to be done by frontend, remove token) |
| recommend  | generate recommendation                                  |
| ratemeal   | rates the generated meal                                 |
| gethistory | gets history of rated meal of user                       |
| others..   | other urls                                               |
|            |                                                          |

  
 ** jwt token authentication is used in this project **

## signup:  
registers new users

the data fields required are: (method POST)

| key       | values                                                            |
| --------- | ----------------------------------------------------------------- |
| username  | username of user                                                  |
| email     | email                                                             |
| password1 | password                                                          |
| password2 | password rewritten                                                |
| age       | age in int                                                        |
| weight    | weight in float (kg)                                              |
| height    | height in float (cm)                                              |
| sex       | either 'M' or 'F'                                                 |
| lifestyle | sedentary, lightlyactive, moderateactive, veryactive, extraactive |
| tags      | tags to define user like fav foods, ingredients, etc etc          |
| disease   | diseases user have                                                |
| allergy   | ingredients user is allergic to                                   |
| diet      | vegetarian or non-vegetarian                                      |
|           |                                                                   |



## signin:

existing users login

 required fields:  method POST

    username, 
    password

 Response gets

    access and refresh in jwt


## signout: 
signout method POST


## recommendmeal:
method POST

 required field: 

    time = breakfast, lunch or dinner


 Response gets you  

  | key                                  | values                                                            |
  | ------------------------------------ | ----------------------------------------------------------------- |
  | user                                 | username                                                          |
  | nutrition format                     | energy(kcal), carbs(gm), fats(gm)                                 |
  | recommended calories, macronutreints | gets calories and macronutrients  values for user                 |
  | food                                 | recommended food info(name, nutrition values, description, etc..) |
  |                                      |                                                                   |

      
 ## ratemeal: 
 method: POST

 stores the rating and history of user
 
  required field: 
    
    rating, 
    time, 
    food_name.. (these three stored from recommend meal) 
    
 
 
 ## userhistory:
 method POST
 
 gets back user history for the user in current session:
 
 
 ## userdetails

 | Method | Function | 
| :----: | :---: | 
| PUT      | updates user details     | 
| DELETE      | deletes user and its associated profile and data   | 
| POST      |  gets user info    | 


 
 
 
 ## epilogue 
 other functionalities are yet to be added:

 user custom meal, ingredients based recommendation
 
