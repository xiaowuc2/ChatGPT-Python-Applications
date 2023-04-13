# Importing libraries
import imaplib
import email
import yaml
import openai


# user dfined : variables
# how_many = int(input()) # how many unseen mails you want to check
# maxtoken = int(input()) # what is the maximum number of charecters you want in your blog
# what_to_ask = input() # what do you want to ask chatgpt to do 
# num_target = int(input()) # number of targeted emails
# list_mail = []
# for i in range(num_target):
#     i = input()
#     list_mail.append(i)


# how many mails you want to see (default values)
how_many = 2
maxtoken = 200
#what_to_ask = "Generate a blog on:"

# Reading private yml file
with open("pass.yml") as f:
    content = f.read()
    
# from credentials.yml import user name and password
my_credentials = yaml.load(content, Loader=yaml.FullLoader)
user, password = my_credentials["user"], my_credentials["password"]
openai.api_key = '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' #my_credentials["api"] 

# Login to the email server
server = "imap.gmail.com"
my_mail = imaplib.IMAP4_SSL(server)
my_mail.login(user, password)
my_mail.select('inbox')


# search : unread emails
status, data = my_mail.search(None, 'FROM', 'rohitmandal814566@gmail.com')


mail_id_list = data[0].split()  #IDs of all emails that we want to fetch 

msgs = [] # empty list to capture all messages
#Iterate through messages and extract data into the msgs list
for num in mail_id_list:
    typ, data = my_mail.fetch(num, '(RFC822)') #RFC822 returns whole message (BODY fetches just body)
    msgs.append(data)

count = 0
for msg in msgs[::-1]:
    if count == how_many :
        break
    count += 1
    for response_part in msg:
        if type(response_part) is tuple:
            my_msg=email.message_from_bytes((response_part[1]))
            print("_________________________________________")
            #print ("subj:", my_msg['subject'])
            #print ("from:", my_msg['from'])
            #print ("body:")
            
            for part in my_msg.walk():  
                #print(part.get_content_type())
                if part.get_content_type() == 'text/plain':
                    print (part.get_payload())

                    snippet = part.get_payload()
                    # prompt = f"{what_to_ask} {str(snippet)}:
                    prompt = f"Generate a blog on: {str(snippet)}"

                    # calling api
                    response = openai.Completion.create(
                        engine="davinci-instruct-beta-v3",
                        prompt=prompt,
                        max_tokens=maxtoken,
                        temperature = 0.7,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0
                    )
                    
                    #printing the response
                    generated_text = response['choices'][0]['text']
                    print(generated_text)
