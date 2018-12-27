# SalsaTrainer Telegram Bot

Telegram bot designed to practice Salsa steps. Its job consist into reading text files (located in '/data' directory) containing a list of Salsa steps, and group it by category. Each single file represents a category. Later the bot offers to the user a menu of categories, once one is chosen, the bot delivers a message every n seconds, with a randomly selected step from the desired category. The goal for the dancer is to hear the step name and put it into practice.

To use the bot in combination with an Android device, a tiny script has been developed to catch Telegram notifications and read it aloud using the text-to-speech built-in Android capability.

In the following sections the input file format is shown, as well as the Tasker instructions to recreate the intended behavior.


## Input file format:

    ::Category_name
    Step_name1
    Step_name2
    Step_name3


## Tasker script

The Tasker side of this utility is conform by a **profile** in charge of monitoring the Telegram activity, and a **task** triggered by it, which extracts the info from the incoming notifications and says it aloud. Here is the description of each one:

**ReadAloud - profile**:

* Event: Notification [ Owner Application:Telegram Title:* ]
* Enter: SayAloud

**SayAloud - task**:

* A1: Variable Split [ Name:%NTITLE Splitter:': ' Delete Base:Off ] 
* A2: Flash [ Text:%NTITLE2 Long:Off ] 
* A3: Say [ Text:%NTITLE2 Continue Task Immediately:Off ] 



## Bot commands:

* /start - starts the trainer
* /stop - stop message delivery by the trainer


## Bot description:

Use /start to begin with the training or /stop to end with it
