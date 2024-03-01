<h1 align="center">Points manager</h1>

Backend for points system

<hr/>

Register
![background](https://github.com/TiagoOliverDev/backend_pontos/blob/main/images/register.png)

Login
![background](https://github.com/TiagoOliverDev/backend_pontos/blob/main/images/login.png)

Collaborated created
![background](https://github.com/TiagoOliverDev/backend_pontos/blob/main/images/colaboradorCreated.png)

List all Collaborators
![background](https://github.com/TiagoOliverDev/backend_pontos/blob/main/images/list_all_colaborator.png)

Type points
![background](https://github.com/TiagoOliverDev/backend_pontos/blob/main/images/typesPontos.png)

Register points
![background](https://github.com/TiagoOliverDev/backend_pontos/blob/main/images/registerPoint.png)


<hr/>

# Features 

- Admin user registration
- Registration and listing of sectors
- Registration and listing of collaborators
- Options to clock in at different times (entry, lunch, return and end of work)
- History (under development)
- Dashboard (under development)

<hr/>

# Technology

I used the following technologies:

- Python >= 3.10.11
- Flask
- Blueprint
- PyJWT
- psycopg2
- cryptography
- bcrypt

<hr/>

# Steps for run project

## Step 1: Clone the repository

- Choose a folder in your local machine where you want this repository to be copied

- Clone this [repository](git@github.com:TiagoOliverDev/backend_pontos.git) to your local machine 
- ```
  git clone git@github.com:TiagoOliverDev/backend_pontos.git
  ```

- Navigate to `cd backend_pontos`  directory.

- To install all the app dependencies on the command line run
- ```
 python -m venv nome_da_env

 nome_da_env/Scripts/activate

 pip install -r requirements.txt

  ``` 

## Step 2: 

After that, go to .env and set the bank credentials and choose to run production or development


## Step 3: Run the project

Open folder project and open a terminal and run the following command:

```bash
python server.py



## OBS: 

I had the idea of ​​creating a type of dashboard for the admin user to monitor who is on pause, working but I didn't have time to continue.

I also had the idea of ​​creating the History menu where the user can download their points history and the admin user can download the history of all users but I didn't have time to finish it either.

The project is cool but not complete, but I tried to follow a good code and architecture standard.


```


<hr/>


## Author

:man: **Tiago Oliveira**

- [GitHub](https://github.com/TiagoOliverDev/)
- [LinkedIn](https://www.linkedin.com/in/tiago-oliveira-49a2a6205/)

## 🤝 Contributing
- Contributions, issues, and feature requests are welcome!
- Feel free to check the [issues page](https://github.com/TiagoOliverDev/backend_pontos/issues).

# Show your support
Give a ⭐ if you like this project!
