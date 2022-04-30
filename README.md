# ArecanutFarmInformatics
This code base is the GitHub repository for the project Arecanut Farm Informatics created for the graduate course CSCE 606 - Software Engineering. Setup the project by following the instructions mentioned below:

## Prerequisite
Verify whether you have installed python by checking its version. To check python version:
  
> python -V  

Make sure you have installed pip:
> python-pip 

## Cloning The Project:

* Clone the project code using the following git command and then switch to the cloned project folder:

       HTTPS: git clone https://github.com/feraskhemakhem/ArecanutFarmInformatics.git 
       OR if using Github CLI: gh repo clone feraskhemakhem/ArecanutFarmInformatics
       
       cd ArecanutFarmInformatics/AgriHelp

* Install dependencies, (use sudo if required)    

       pip install -r requirements.txt
       
* A .env file must be added to the AgriHelp subfolder. A .env file with all the necessary secrets is ecrypted in the secrets folder. Move the decrypted file to the AgriHelp/ folder to ensure that the database can be accessed for all functionality.

## Running the Project Locally

* Start application hosting it locally:

       python app.py
       OR
       python -m flask run
       
Common error faced while running locally is "Flask ImportError: No Module Named Flask" for which you can create a virtual env by following steps mentioned below:
      virtualenv flask
      
      cd flask
      
      source bin/activate
      
Now you should see (flask) on the left of the command line. Then proceed to install flask:

      pip install flask

* In the browser go to:

       http://localhost:5000          

You'd be able to see the landing page of the ArecanutFarmInformatics website from where you can proceed to login or register yourself prior to logging in to check out the available functionalities.

## Database Connection and Heroku Deployment

### Heroku Deployment
* In order to deploy to Heroku, first a Heroku app must be created and connected to the codebase. Under the settings tab, add config vars for each key in the .env file of the secret folder (the key is the name, the value is the secret).
      
 * Finally, deploy the code from the main branch to ensure that it works. The procfile should include both dynos needed to run. In order for the clock dyno to run on time, we must run a clock process to start the cronjob. This will enable scheduling of email notifications. Running the following command in Heroku CLI will enable this:

       heroku ps:scale clock=1
       
At this point, everything should be running as intended.

### Database Connection
* Please note that direct connection to the database is NOT required to deploy the project, and is only required if one wishes to look into the tables of the database.

* The database is written in MySQL, hosted on an Amazon RDS DB instance. To directly access the database, we use MySQL Workbench. For details on connecting to our database with MySQL Workbench, please refer to this resource: https://aws.amazon.com/premiumsupport/knowledge-center/connect-rds-mysql-workbench/. The parameters needed are all included in the .env of the secret folder.

* The database's name is _FarmInformatics_, with the following table names:
    * _Users_, used to store user login data
    * _Tanks_, used to store information about water tanks
    * _Rainfall_, used to store information about rainfall on given timeframes
    * _Plots_, used to store information about the plot(s) of land the user keeps track of
