

---
In the WorkTimeTracking people can be project owners or project members.

To be a Project Owner:
1. register and become a user. ```/auth/register```
2. login. ```POST /auth/login```
3. define a project (or how many you want), and you will be the owner.
4. invite people (whether they are our users or not) to work on your project by entering their emails.

To be a member in a project:
1. you should receive an invitation code through your email from PO.
2. register and become a user.
3. login.
4. enter your invitation code and you will become a member

To start working on a task and track the time:
select project and task and hit the start btn!
```POST /api/start```

to stop working:
```PUT /api/stop```
---

a celery worker will run every day 1:00 AM and will calculate working hours
on tasks and projects for the last day and will save the results
in two related tables ```ProjectDailyReporting``` and ```TaskDailyReporting``` 
to avoid heavy database queries in production.

Reporting APIs (still not implemented) will use this two tables

---

Super User Credentials:
```
user = admin
pass = admin1234
```



