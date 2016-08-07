#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json, requests, random, re
from pprint import pprint

from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.


PAGE_ACCESS_TOKEN = 'EAAQA1ZA0bZBB0BAKHYZA0AIgslS75KYQVheP0eIH6r5JKXZArYl3FWJzAksixxZBpP55BqfSUavhOQ8PhaHcM4kovmJQNTmfdkdQKkjup0wN9u9Yf8PSiB6ydAc9BSex5KjKQqaKWwuXqNOid9eRWwFIZBsFoXinZAVa6z5rwnN7wZDZD'
VERIFY_TOKEN = '8447208288'

quotes_arr = [["Life isn’t about getting and having, it’s about giving and being.", "Kevin Kruse"],
["Whatever the mind of man can conceive and believe, it can achieve.", "Napoleon Hill"],
["Strive not to be a success, but rather to be of value.", "Albert Einstein"],
["Two roads diverged in a wood, and I—I took the one less traveled by, And that has made all the difference.", "Robert Frost"],
["It’s your place in the world; it’s your life. Go on and do all you can with it, and make it the life you want to live.", "Mae Jemison"],
["You may be disappointed if you fail, but you are doomed if you don’t try.", "Beverly Sills"],
["Remember no one can make you feel inferior without your consent.", "Eleanor Roosevelt"],
["Life is what we make it, always has been, always will be.", "Grandma Moses"],
["The question isn’t who is going to let me; it’s who is going to stop me.", "Ayn Rand"],
["When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.", "Henry Ford"],
["It’s not the years in your life that count. It’s the life in your years.", "Abraham Lincoln"],
["Change your thoughts and you change your world.", "Norman Vincent Peale"],
["Either write something worth reading or do something worth writing.", "Benjamin Franklin"],
["Nothing is impossible, the word itself says, “I’m possible!”", "–Audrey Hepburn"],
["The only way to do great work is to love what you do.", "Steve Jobs"],
["If you can dream it, you can achieve it.", "Zig Ziglar"]
]



def return_random_quote():
    random.shuffle(quotes_arr)   # random is imported.
    return quotes_arr[0]    



def quote_search(str_var):
    str_var.lower()
    random.shuffle(quotes_arr)
    for quote_text,quote_author in quotes_arr:
        if str_var in quote_author.lower():
            return quote_text

    return return_random_quote()[0]
'''def quote_search(str_var):
    for quote_text , quote_author in quotes_arr:
        if str_var in quote_author.lower():
            return quote_text
    return return_random_quote()
'''

def post_facebook_message(fbid, recevied_message):
    reply_text = recevied_message + ' :)'

    try:
        user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
        user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
        user_details = requests.get(user_details_url, user_details_params).json() 
        joke_text = 'Yo '+user_details['first_name']+'..! ' + reply_text
        print "In try block"
    except:
        print "In except block"
        joke_text = 'Yo ' + reply_text
    
    #joke_text = quote_search(recevied_message)
    joke_text = return_random_quote()[0] 
    response_text = recevied_message +' :)'


    message_object = {
        "attachment":{
          "type":"image",
          "payload":{
            #"url":"http://thecatapi.com/api/images/get?format=src&type=png"
            "url" : "http://worldversus.com/img/ironman.jpg"
          }
        }
    }

    message_object2 = {
        "text": joke_text
        }
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    response_msg2 = json.dumps({"recipient":{"id":fbid}, "message":{"text":response_text}})
    
    response_msg3 = json.dumps({"recipient":{"id":fbid}, "message": message_object})
    
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    #status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg2)
    
    pprint(status.json())

'''
    #random_quote = return_random_quote()
    #joke_text = return_random_quote()[0] 
    joke_text = quote_search(recevied_message)
    response_text = recevied_message +' :)'

    message_object = {
        "attachment":{
          "type":"image",
          "payload":{
            "url":"https://petersapparel.com/img/shirt.png"
          }
        }
    }
    print "Posting message"               
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    #response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    response_msg2 = json.dumps({"recipient":{"id":fbid}, "message":{"text":response_text}})
    
    response_msg3 = json.dumps({"recipient":{"id":fbid}, "message": message_object})
    
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    #status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg2)
    #status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())
'''

class MyQuoteBotView(generic.View):
    def get(self, request, *args, **kwargs):
        try :
            print "Hello!"
            if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
                print "There!"
                return HttpResponse(self.request.GET['hub.challenge'])
            else:
                return HttpResponse('Error, invalid token')
        except:
            return HttpResponse('No token Provided.')
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)    
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly. 
                    post_facebook_message(message['sender']['id'], message['message']['text'])    
                    print 

        return HttpResponse()    



def index(request):
    print test()
    print quote_search('avassfsdre@')
    return HttpResponse("Hello World" + quote_search('*'))

def test():
    #post_facebook_message('100000401701314','test message')
    post_facebook_message('1366822393332584','test message')





'''


import json, requests, random, re
from pprint import pprint


from django.shortcuts import render

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.

PAGE_ACCESS_TOKEN = 'EAAQA1ZA0bZBB0BAJfRrVXYdjHR0mhH8aDUfFGNBjhynrcCiHmyZCGSE11LxLbRPPadrmLTHNcEZA9ZCXvs4izgaNhXkZBVkWxvZA8CK7vP5RqOmK4k3Ah24DWooWw2o6ZBGHnZCEvms8RXKD5vZBFwQ81ZCFZAT1PnEmvXE8MIHZBHgnLRwZDZD'



def post_facebook_message(fbid, recevied_message):
    # Remove all punctuations, lower case the text and split it based on space
    #clean_message = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message)

    reply_text = ''
    

    if not reply_text:
        reply_text = recevied_message

    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
    user_details = requests.get(user_details_url, user_details_params).json() 
    joke_text = 'Yo '+user_details['first_name']+'..! ' + reply_text
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


class MyQuoteBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '8447208288':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)    
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly. 
                    post_facebook_message(message['sender']['id'], message['message']['text'])    
        return HttpResponse()    


def index(request):
    return HttpResponse("Hello World")


def hello(request):
    return HttpResponse('By Bye world')
    '''



