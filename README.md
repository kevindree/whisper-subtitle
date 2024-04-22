# About whisper-subtitle
This is a open source subtitle generation web app based on the OpenAi Whisper AI model. 
Using gradio for the userinterface.

## Installation
I used python 3.10, before install , make sure python has been installed on your system. Then you can use the following command to download and install it.
```
# clone the Repository first.
git clone https://github.com/kevindree/whisper-subtitle

# enter whisper-subtitle folder
cd whisper-subtitle

# install dependensies which was mentioned in requirements.txt file
pip install -r requirements.txt -U
```
if you have not installed ffmpeg, use the following command to install ffmpeg as well. please choose the corresponding command according to your operating system.
```
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```
Then you can start the application by running command in the whisper-subtitle folder
````
python app-ui.py
````
you will see some output like "Running on local URL:  http://127.0.0.1:7860" under this command. copy that url from your output message, and open it in your browser. you will be able to see the screen.
