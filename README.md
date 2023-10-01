# Tal2k Task Management 

## Prerequisites
> 👉 Have Docker fully installed and running on you machin

> 👉 Ensure that no other container is still running on Docker

> 👉 Ensure that no process is running on the following ports {5085, 27017, 6379, 5050, 5432, 8000}


## How to Build

> 👉 Download the code

> 👉 Go to the project directory
```bash
$ cd django-admin-dashboard-master
```

> 👉 Build and Run the docker containers
```bash
$ docker-compose up -d --build
```
After successfully running the steps listed, you should be able to see the following containers running

![LAUNCHED DOCKER CONTAINERS](https://i.ibb.co/KD06pfb/image.png)

## User Configurations

After waiting for a few seconds for our nginx webserver to complete initialization and start accepting requests, 
proceed to enter the following URL into your browser

>http://localhost:5085/

This should prompt you with the following Login scree which you should fill the default superuser credentials:
- username: admin
- password: 123

![LOGIN SCREEN](https://i.ibb.co/55GsDNQ/image.png)


To add a new user which will be joined to our "Regular User Group", we navigate to Users and click "ADD USER" 
in the top right corner 

![ADDING A USER](https://i.ibb.co/pjN0pQF/image.png)

> WHEN ADDING A NEW USER, MAKE SURE TO CHECK THE STAFF STATUS CHECKBOX AND SELECT "Regular Users" FROM THE GROUPS SECTION
> IN ADDITION TO ADDING A VALID EMAIL ADDRESS FOR TASK NOTIFICATIONS

![USER CONFIGURATION](https://i.ibb.co/xMgx9kc/image.png)

## Creating a new Task
Only superusers are authorized to create a new task, which means that you should be logged into the previously mentioned 
admin user, or any newly created user with the "superuser status" checked in order to assign a task. 

>👉 Navigate to the Tasks section under Task_Management

> 👉 click "ADD TASK" in the top right corner

![CREATING A NEW TASK](https://i.ibb.co/YTMWFZT/image.png)
![FILLING TASK DETAILS](https://i.ibb.co/1MTtnbx/image.png)
![NEW TASK RECORDED](https://i.ibb.co/CWySvs0/image.png)

-Clicking save should record a new task that is only visible by the user selected

-Only superusers have the ability to view and manage all tasks

When saving a task, a celery worker (which is run on a different container) should be launched to send an automated email
notifying the user of his new task

![AUTOMATED EMAIL](https://i.ibb.co/hLzgm1J/image.png)

## Logging in From Regular User Account

>👉 Log in using the credentials of the newly created user and new task assignee

![REGULAR USER VIEW](https://i.ibb.co/zsf0dHD/image.png)

It can be revealed the regular user does not have access to groups and users configurations, nor can they create a 
new task. They can only manage (view, modify, delete) tasks specifically assigned to them

## Mongo DB Logs

The application has been configured to log some Admin dashboard activities to the mongoDB launched in a 
separate container. the logs can be visualized by accessing a mongo compass GUI, and entering the following 
connection string to establish a connection with the mongoDB running within the container

> mongodb://localhost:27017

Then click connect to make the connection.

a database with the name "admin_activity_db" should appear. Accessing this DB will reveal the logs of the activities 
performed on the dashboard and who performed them (i.e. User login, Task creation, deletion or modification etc.)

![MONGO DB LOGGING](https://i.ibb.co/W6WKgC8/image.png)

## Shutting Down the Containers

finally, to shut down all the containers, navigate to the project root folder and run the following command

```bash
$ docker-compose down
```

---
Django Task Manager - Developed and Maintained by **Rami** 
