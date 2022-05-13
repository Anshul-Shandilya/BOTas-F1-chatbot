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

## **Conversation flows**

Currently supported API calls to retrieve race information are:
1. latest race result
2. latest qualify result
3. current season schedule

Other supported queries by the bot:
1. You can ask for a joke (it's going to tell you an F1 joke)
2. You can ask for it to submit a feedback form that is uploaded to the database
3. Bot can engage in small talk

* Conversation flow to directly ask for race result:
In this flow, you can ask for anything instead of race result (like qualify or schedule). 
```
Your input ->  Hi

                                        Bot -> Hey! How are you?

Your input ->  Im fine, how are you?

                                        Bot -> Thanks for asking, I'm fine. What can I do for you?

Your input ->  Can you get me the latest race result?

                                        Bot -> Here's the latest race result:
                                            Race 5, season 2022, took place at miami, at Miami International Autodrome circuit
                                            Standings:
                                            Position 1, points obtained : 26 - Driver: Max Verstappen, Number: 33, driving for Red Bull.
                                            Position 2, points obtained : 18 - Driver: Charles Leclerc, Number: 16, driving for Ferrari.
                                            Position 3, points obtained : 15 - Driver: Carlos Sainz, Number: 55, driving for Ferrari.
                                            __________________________________
                                            Is there something else I can help you with?

Your input ->  Nope

                                        Bot -> Cool! Let me know.

Your input ->  Sure, bye

                                        Bot -> Bye bye
``` 

**One more feature that is highlited here is that the bot will ask appropriate questions based on the user input.**
In the flow below, you can see in the first reply, the bot asks the user "Holla! How you doin?". If your input is something like "Im fine" i.e. without a follow up question, then the bot replies with something like "Great! What can I do for you?" (This is described in the flow below). However if your input to the question "Hi! How are you doing?" includes a question, like "I'm fine, how are you?" (as shown in the flow above), then the bot will reply with something like "Thanks for asking, I'm fine. What can I do for you?".

* Conversation flow for small talk 1: If the user doesn't know what the chatbot does, the user can ask the bot directly. You can also ask to retrieve information afterwards. 
```
Your input ->  Hi

                                        Bot -> Holla! How you doin?

Your input ->  in fine

                                        Bot -> Great! What can I do for you?

Your input ->  not sure, what can you do for me?

                                        Bot -> You can ask me about Formula 1 stuff. For example you can ask me to get the latest race results.

Your input ->  Cool

                                        Bot -> Okie dokie
```

* Conversation flow for small talk 2: User can ask for jokes, and play around with the bot. If you complain to the bot that the jokes aren't funny, then it will respond appropriately. 
```
Your input ->  Hi

                                        Bot -> Holla! How you doin?

Your input ->  Im fine how are you

                                        Bot -> I'm great, thanks for asking! What can I do for you today?

Your input ->  I feel sad

                                        Bot -> This ought to cheer you up!:
                                            Image: https://i.imgur.com/XHZH8SW.jpeg
                                            Did that help you?

Your input ->  Yes

                                        Bot -> I'm glad!!!

Your input ->  That wasn't enough. Can yoiu tell me a joke too?

                                        Bot -> Here's a joke for you.\n\n
                                            Why is the white bishop piece in chess the fastest? Because it's on F1.

Your input ->  It's not funny

                                        Bot -> I know right? My creator chose them. (But they are all terrible tbh..... don't tell him I said that!)

Your input ->  who are you btw?

                                        Bot -> My name is BOTas (get it?). I can retrieve information about Formula 1.

Your input ->  are you human?

                                        Bot -> I BOTas (get it?), a bot powered by Rasa.
```
Conversation Flow to provide feedback: This will upload the given feedback to the database using SQL in the actions server.

**One of the flaws of my implemented feedback form is instead of enabliung text inpout for forms, I have defined first name and last name along with the feedvback in the nlu file which makes it so only defined feedback and names are taken as input.**
```
Your input ->  Can I provide feedback?
                                        Bot -> Your first name?
Your input ->  Anshul
                                        Bot -> Your last name?
Your input ->  Kumar
                                        Bot -> Your feedback?
Your input ->  good
                                        Bot -> Name: Anshul Kumar
                                            Feedback: good.
                                            Thank you for your feedback! I have submitted your form.
```
## **Open/current issues with the chatbot**

* 

## **Links**

* Presentation slides
* Requirements.txt
