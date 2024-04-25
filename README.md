# 431FinalProject

Video Zoom links Below: <br />
[Kaltura link](https://psu.mediaspace.kaltura.com/media/Project+Walkthrough/1_0er49csg) <br />
[Zoom Link](https://psu.zoom.us/rec/share/9Q6dqful8NTrplOTMqHcKamoAilMGmDnkylEDk3UZXPqBharq8sDdX0b-wcFjiZA.XPAaMD5ewmaSuqzF?startTime=1714009512000) <br />
The [video](https://github.com/shivpvtel/431FinalProject/blob/main/Project%20Walkthrough-2.mp4) is also provided in the GitHub Repo but just incase, there are two links above can access the same video. <br />


This Repository has the following:<br />
  1) [Import folder](https://github.com/shivpvtel/431FinalProject/tree/main/imports): make folder that has all the .CSV files which contain the data, as well as python scripts to import the data into PGAdmin4<br />
  2) [Projectcode.py](https://github.com/shivpvtel/431FinalProject/blob/main/projectcode.py) has the implementation for the CLI.<br />
  3) [ProjectFinalSubmission.pdf](https://github.com/shivpvtel/431FinalProject/blob/main/ProjectFinalSubmission.pdf) is the write up for this project.<br />


Steps to use this repository:<br />
  1) Download [PGAdmin4](https://www.pgadmin.org/download/)<br />
  2) Open VScode: Hit cmd+shift+P and then "Python: Select interpreter" and be sure to select "Python 3.12.0 64 bit"<br />
  3) Then in VScode open the terminal and type "Pip3 install psycopg2" and then "Pip3 install sys"<br />
  4) Open up PgAdmin4's Gui and create a database with the default settings shown below:<br />
'''
    Database name = "postgres"
    user = "postgres",
    password = "1234",
    host = "localhost",
    port = "5432"
'''
  5) Navigate back to the terminal in vscode, navigate to the directory you want the file to be located in, and clone this repo<br />
  6) Navigate to the import folder and then run every python script to import the data to the PgAdmin4 database.<br />
  7) Navigate to projectcode.py and run the pyhton script to start using the CLI.<br />
