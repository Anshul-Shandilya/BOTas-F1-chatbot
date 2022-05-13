# BOTas-F1-chatbot
Chatbot made using Rasa for Formula 1 information

## **Rasa Version Used**
```
pc:/PROJECT$ rasa --version
Rasa Version      :         3.1.0
Minimum Compatible Version: 3.0.0
Rasa SDK Version  :         3.1.1
Rasa X Version    :         None
Python Version    :         3.8.10
```

## **Instructions to run**

The following process works on linux, mac or windows as a local project. **(For windows, WSL used)**

1. First create a virtual environment in your choice of directory using the following command and activate it: 
```
python -m venv venv         # Create virtual env.
source venv/bin/activate    # Activate virtual env.
```

2. If rasa is not installed, then install rasa using:
```
python -m pip install rasa  # This will install latest version of rasa
```

3. If you don't have a rasa project already, then you can create an initial one using the below command.
You can choose any directory you like while creating the project. 
You only need the basic project setup as training will take time.  
```
python -m rasa init         # Will create an initial rasa project
```
4. You can then replace the files from this repo (in [source](Source) folder) to your local project. Make sure you are using rasa 3.1.0 or above. Ensure that all files are properly placed in the respective folders in the local project. You can simply cut-paste the files from source to your project's root folder.

5. Next step is to train the rasa model using the new files. Make sure you are in the virtual environment. This can be done using the following command:
```
rasa train                  # This will train the model
```

6. To make API calls which are defined in actions.py file in the [actions](Source/actions) folder, you need to run a parallel terminal with the same virtual environment running. Use the same process as defined in step 1 above. Then to run the action file, use the following command:
```
rasa run actions            # This will run the actions server
```

7. We are now close to run the chatbot. Since the action server is up and the model has been trained, we can simply use the following command to run the chatbot.
```
rasa shell                  # This will run an interactive terminal for you to interact with the chatbot.
```

8. There you have it. You can now interact with the chatbot as you please!

## **Conversation flows that you can use**


## **Open/current issues with the chatbot**


## **Links**

* Presentation slides
* Requirements.txt
