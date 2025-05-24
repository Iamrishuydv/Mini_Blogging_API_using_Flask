# Mini Blog App setup

## First Step:

### Clone this repo.

### git clone https://github.com/Iamrishuydv/Mini_Blogging_API_using_Flask/tree/main/Mini_Blogging_API_using_Flask

### cd Mini_Blogging_API_using_Flask

## Second Step:

### create env by this command - ' python3 -m venv venv '  then activate it  ' source venv/bin/activate '

## Third Step:

### Install required packages by " pip install -r requirements.txt "

## Fourth Step:

### You can see the .env file setup the credentials accordingly

## Fifth Step:

### Before running the app Create the MySQL database 
### CREATE DATABASE mini_blog_db;

## Finally, you can Run the Server
### cmd : "python3 server.py"


# Now you can check the the api in postman and http://localhost:5000/hc to check it's up and running.


# API Endpoints
## User
### POST -- /user/signup

### POST -- /user/login

### POST -- /user/logout

### POST -- /user/request-otp

### POST -- /user/forgot-password

## Post
### POST -- /post/create (Login Required)

### POST -- /post/all

### POST -- /post/get-post

### POST -- /post/update (Login Required)

### DELETE -- /post/delete (Login Required)

## Comment
### POST -- /comment/add

### POST -- /comment/list


# I've attached a xlsx file too for better API documentation.
## You can findv : MM/Mini_Blogging_API_using_Flask/miniBlog_API_Endpoint_Documentation.xlsx
