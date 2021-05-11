
import nltk
import random
import string
import re
import string, unicodedata
from nltk.corpus import wordnet as wn
import wikipedia as wk
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
import warnings
warnings.filterwarnings("ignore")
nltk.download('punkt') 
nltk.download('wordnet')

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
import mysql.connector as MySQLdb
db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="Mysql@88",database='mydb')

#So the data preprocessing part is over now let's define welcome notes or greetings that means if a user provides is a greeting message, the chatbot shall respond with a greeting as well based on keyword matching.
def SERVICEDEL(res):
     cursor=db.cursor()
     mobileno=res[11];
   
     insert_stmt = (
      "DELETE FROM Subscribertable "
      "WHERE Mobileno = %s"
      )
     adr = (mobileno)

     try:
   # Executing the SQL command
      cursor.execute(insert_stmt,(adr,))
      db.commit()
     except:
    # Rolling back in case of error
      db.rollback()
     print("Data deleted")
   # Closing the connection
def SERVICEADD(res):
     cursor=db.cursor()
     group=res[9];
     mobileno=res[11];
     insert_stmt = (
        "INSERT INTO Subscribertable (Groupname,Mobileno)"
        "VALUES(%s, %s)"
       )
     data = (group,mobileno)

     try:
   # Executing the SQL command
      cursor.execute(insert_stmt, data)
      db.commit()
     except:
    # Rolling back in case of error
      db.rollback()
     print("Data inserted")
# Closing the connection
    # db.close()
def GRPCREATE(res):
     cursor=db.cursor()
     group=res[7];
     status=res[8];
     insert_stmt = (
        "INSERT INTO Grouptable (Groupname,status)"
        "VALUES(%s, %s)"
       )
     data=(group,status)
     try:
   # Executing the SQL command
      cursor.execute(insert_stmt,data)
      db.commit()
     except:
    # Rolling back in case of error
      db.rollback()
     print("Data inserted")
# Closing the connection
    # db.close()
def GRPDELETE(res):
     cursor=db.cursor()
     group=res[7];

     insert_stmt = (
      "DELETE FROM Grouptable "
      "WHERE Groupname = %s"
      )
     adr = (group)
     try:
   # Executing the SQL command
      cursor.execute(insert_stmt,(adr,))
      db.commit()
     except:
    # Rolling back in case of error
      db.rollback()
     print("Group Deleted")
# Closing the connection
    # db.close()
def GRPSTATUS(res):
     cursor=db.cursor()
     group=res[7];

     insert_stmt = (
      "SELECT status FROM Grouptable "
      "WHERE Groupname = %s"
      )
     adr =(group)
     try:
      cursor.execute(insert_stmt,(adr,))
      records = cursor.fetchall()
      print("Printing status")
      for row in records:
           print(row)
      db.commit()
     except:
    # Rolling back in case of error
      
      db.rollback()
     print("Group Status")
# Closing the connection
    # db.close()
    
def SUBSCRIBE(res):
     cursor=db.cursor()
     group=res[9];
     mobileno=res[7];
     insert_stmt = (
        "INSERT INTO Subscribertable (Groupname,Mobileno)"
        "VALUES(%s, %s)"
       )
     data = (group,mobileno)

     try:
   # Executing the SQL command
      cursor.execute(insert_stmt, data)
      db.commit()
     except:
    # Rolling back in case of error
      db.rollback()
     print("Data inserted")
def UNSUBSCRIBE(res):
     cursor=db.cursor()
     mobileno=res[7];
   
     insert_stmt = (
      "DELETE FROM Subscribertable "
      "WHERE Mobileno = %s"
      )
     adr = (mobileno)
     try:
   # Executing the SQL command
      cursor.execute(insert_stmt,(adr,))
      db.commit()
     except:
    # Rolling back in case of error
      db.rollback()
     print("Data deleted")
   # Closing the connection
def service2():
    print("Chatterbot :\n",end="")
    print("please send URL")
    URLrequest=input()
   
    if("http://<IP Address>/chatbotservice?COMMAND=" in URLrequest):
     print("right")
     res = re.findall(r'\w+',URLrequest)
     if(res[5]=='SERVICEADD'):
         SERVICEADD(res)
     if(res[5]=="SERVICEDEL"):
         SERVICEDEL(res)
     if(res[5]=="GRPCREATE"):
         GRPCREATE(res)
     if(res[5]=="GRPDELETE"):
         GRPDELETE(res)
     if(res[5]=="GRPSTATUS"):
         GRPSTATUS(res)
     if(res[5]=="SUBSCRIBE"):
         SUBSCRIBE(res)
     if(res[5]=="UNSUBSCRIBE"):
         UNSUBSCRIBE(res)
    else:
        print("Please Enter Correct URL Request")
    
#Generate chatbot response


#To generate a response from our chatbot for input questions, the concept of document similarity will be used. As I have already discussed the TFidf vectorizer is used to convert a collection of raw documents to a matrix of TF-IDF features and to find the similarity between words entered by the user and the words in the dataset we will use cosine similarit

#e define a function generateResponse() which searches the user’s input words and returns one of several possible responses. If it doesn’t find the input matching any of the keywords then instead of giving just an error message you can ask your chatbot to search Wikipedia for you. Just type “tell me about any_keyword”. Now if it doesn't find anything in Wikipedia the chatbot will generate a message “No content has been found”.
def searchresult(search):
    with open("MARS_Redis_disconnect_logs.txt", 'r') as read_obj:
        flag=0
        for line in read_obj:
          if (search in line)and (flag==0):
            flag=1
            print("Please enter group name")
            group=input()
            cursor=db.cursor()
            insert = (
                "SELECT * FROM Subscribertable "
                "WHERE Groupname = %s"
               )
            adr =(group)
            cursor.execute(insert,(adr,))
          
            records = cursor.fetchall()
           
            print("Total number of rows in table: ", cursor.rowcount)
            print("\nPrinting each row")
            db.commit()
            for row in records:
             print("Mobileno = ", row[2])
            print("MySQL connection is closed")
           
            

welcome_input = ("hello", "hi", "greetings", "sup", "what's up","hey",)
welcome_response = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
def welcome(user_response):
    for word in user_response.split():
        if word.lower() in welcome_input:
            return random.choice(welcome_response)

exit_list = ['exit', 'see you later','bye', 'quit', 'break']
flag=True
print("My name is Chatterbot and I'm a chabot. If you want to exit, type Bye!")
while(flag==True):
    print("User : ", end="")
    user_response = input()
    user_response=user_response.lower()
    if(user_response not in exit_list):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("Chatterbot :\n You are welcome..")
        else:
            if(welcome(user_response)!=None):
                 print("Chatterbot : \n"+welcome(user_response))
                 
            else:
                print("Chatterbot :\n",end="")
                print("please tell me your requset")
                print(""" 1.Search or add a string\n 2. SUB,UNSUB, SERVICE, GROUP """)
                print("Please enter 1 or 2")
                print("User : ", end="")
                request=int(input())
                if request==2:
                    service2()
                elif request==1:
                    print("Enter search string or log")
                    search=input()
                    searchresult(search)
                   # sent_tokens.remove(search)
                else:
                      print("please choose any one requset")
    else:
        flag=False
        print("Chatterbot: Chat with you later !")
        break


 


 






