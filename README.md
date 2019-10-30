A discord bot made using the discord.py and sqlite3 API 

# Cogs/Features #

All commands begin with the prefix '.'.

## matrixcalculation.py
Takes matrices as command parameters and performs operations. Matrices must be inputted as a,b,c|d,e,f|g,h,i where a,b,c denotes the first row, d,e,f denotes the second row and so on. Each '|' separates rows and ',' seperates entries. 

Commands begin with .matrix. Supported commands and their usages are as follows:

**add (matrix1) (matrix2)** 

Adds two matrices

**subtract (matrix1) (matrix2)** 
  
Subtracts two matrices


**scalarmultiply (matrix1) (scalar)** 
  
Takes the product of a matrix and a real numbe


**multiply (matrix1) (matrix2)** 
  
Takes the product of two matrices


**transpose (matrix)** 
  
Swaps the rows and columns of a matrix


**determinant (matrix)** 
  
Computes the determinant of a matrix


**inverse (matrix)** 

Takes the inverse of a matrix 

## messagesearch.py
Logs all messages sent to the server, and fetches all messages since the bot was last online. All messages are stored into a local SQL db using the sqlite3 python API. The last online time is logged by discordbot.py when the program terminates. Utilizes regular expressions to search messages

Commands begin with .search. Supported commands and their usages are as follows:

**email (user)** 
  
Searches the entire channel history for any messages from a mentioned user that contain email addresses. Sends a message containing all of the found email addresses

**phone (user)** 
  
Searches the entire channel history for any messages from a mentioned user that contain phone numbers. Sends a message containing all of the found phone numbers. 
  
## moderation.py 
Allows server administrators to ban and kick users, and remove a specified number of messages. 

Supported commands and their usages are as follows:

**ban (user)** 
  
**kick (user)**

**purge (number of messages)**


## leveling.py 
Simple leveling algorithm. Users gain xp whenever they send a message. All information pertaining to user xp and levels are stored in the local database. 

# Installation #

1. Install Python3 

2. Open cmd and run ```pip install discord.py``` and ```pip install sqlite3```

3. Add your discord bot token and your discord server token to the .env file. Specify the .env filepath if load_dotenv() fails.

4. Add your channel ID to cogs/messagesearch.py 

5. Run discordbot.py


