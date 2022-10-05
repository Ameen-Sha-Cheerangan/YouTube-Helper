# Playlist-Length-Checker
plc.py

Pre-Requisites 

Can be run only in linux and mac machines.
User must create his own API_KEY which can be created from the site : https://console.cloud.google.com/apis/dashboard?pli=1&project=youtube-api-362521 for free.

He can paste it in the script accordingly or the recommended technique would be to do the following:

sudo gedit ~/.bash_profile.

which would open a file and copy the following line into it and save and close the file.

export YouTube_API="Your own API_KEY in double quotes"

Then open up a terminal and type the following command : 

source ~/.bash_profile

	

How to setup the script
	
Open up a terminal and clone the file :

git clone https://github.com/Ameen-Sha-Cheerangan/Playlist-Length-Checker.git

Change the directory :

cd Playlist-Length-Checker/

Run the following commands to set the virtual environment:

python3 -m venv virtual_env

source virtual_env/bin/activate

pip install -r requirements.txt 

	
How to run each time everytime you want to check the length of playlist
	
Open up a terminal

Change the directory :

cd Playlist-Length-Checker/

Type the following command : 

python3 plc.py

!!!Paste URL of any of the video inside the playlist to find the total duration of the playlist!!!
	
