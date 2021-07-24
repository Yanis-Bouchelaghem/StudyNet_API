# The Studynet API
This is a RESTful API developed for the android mobile application **Studynet**. The app can be found [Here](https://github.com/itsAbdou/Studynet "Studynet app").
## Description
This Django Rest Framework backend is developed to process and manage data related to the organization of online university education.

It offers three types of users :
* Teachers
* Students
* Administrators

A permission system ensures that each user has access to endpoints related to their function only.

This project requires the PostgreSQL data base engine, as it uses PostgreSQL specific fields.
## Endpoints
The API offers many endpoints to enable the mobile app to read and insert relevant information.

The base link to the API is : https://study-net-api.herokuapp.com/api/

An exhaustive list of all available endpoints can be found in an [exported postman collection](https://github.com/AlphaSh0w/StudyNet_API/blob/Develop/StudyNet.postman_collection.json).

Here are a few endpoint examples :

* **api/students/**

This endpoint allows the creation of a student account, it expects a `POST` request containing the following information:
```JSON
{
    "user": {
        "email": "dummyemail@me.com",
        "password": "dummypassword",
        "first_name": "dummyfirst",
        "last_name": "dummylast"
    },
    "registration_number": "123456789",
    "group": 1,
    "section": "ISIL B L3"
}
```
In case all of the information is correct, the backend will create the student account and return the following result :
```JSON
{
    "user": {
        "id": 54,
        "email": "dummyemail@me.com",
        "first_name": "dummyfirst",
        "last_name": "dummylast",
        "date_joined": "2021-06-24T22:58:47.245491+01:00"
    },
    "section": {
        "code": "ISIL B L3",
        "number_of_groups": 3,
        "specialty": "ISIL",
        "modules": [
            "COMPIL",
            "GL 3",
            "WEBDEV",
            "ANGLAIS",
            "BDD",
            "SI"
        ]
    },
    "group": 1,
    "registration_number": "123456789",
    "token": "aa376a45172111...dummyToken"
}
```
The returned information contains details about the assigned section (the code, the modules taught etc...), it also contais a `token` that uniquely identifies this user.

The `token` is to be sent with any subsequent request to gain the permissions of the type of the requesting user.

* **api/sessions/?section=SECTION_NAME**

This endpoint returns information about the sessions concerning sections, it expects a `GET` request, the request should contain the `token` in the autorization header.

the url can optionally contain a parameter called `section` that specifies the code of a section that the sessions should be filtered on, if no section is provided, all existing sessions are returned.

 Example result :
 ```JSON
 [
    {
        "id": 38,
        "teacher_name": "dummyName1",
        "teacher_email": "dummyemail1@me.com",
        "module": "GL 3",
        "module_type": "DIRECTED",
        "section": "ISIL B L3",
        "concerned_groups": [
            1,
            2,
            3
        ],
        "day": 2,
        "start_time": "08:00:00",
        "end_time": "09:30:00",
        "meeting_link": "dummy meeting link 1",
        "meeting_number": "849 325 565",
        "meeting_password": "3FXp8JqMCY3",
        "comment": "",
        "assignment": 52
    },
    {
        "id": 27,
        "teacher_name": "dummyName2",
        "teacher_email": "dummyemail1@me.com",
        "module": "COMPIL 2",
        "module_type": "LECTURE",
        "section": "ACAD A L3",
        "concerned_groups": [
            2
        ],
        "day": 6,
        "start_time": "08:00:00",
        "end_time": "10:00:00",
        "meeting_link": "Dummy meeting link 2",
        "meeting_number": "",
        "meeting_password": "",
        "comment": "DummyComment",
        "assignment": 42
    },
    ...
 ```
 Each session contains information about its teacher, the concerned section and groups, the schedule and the day (ranging from `1` for saturday to `6` for thursday) and other relevant information specified by the teacher.

## Installation process
### Installing dependencies
This project depends on packages, the dependencies are specified in the `requirements.txt` file in the root folder.

To install all dependencies : in the root directory,  run :
```
pip install -r requirements.txt
```
### running migrations
Inside of the `Studynet/` folder, you will find a `.env example` file, it contains an example of the `.env` file that will contain important environment variable, it needs to be created in that same folder.

Make sure the database credentials are properly configured in the `.env` file you just created.

To make the migrations :
```
python manage.py makemigrations
```
To run the migrations :
```
python manage.py migrate
```
### Applying Fixtures
The server requires some initial data to be loaded in the database before use.

run :
```
python manage.py loaddata groups.json
```
### Running the server
The server is now ready to start, simply run :
```
python manage.py runserver
```
Congratulations! the server is now up and running.