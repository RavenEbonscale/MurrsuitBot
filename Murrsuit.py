import base64
import praw, os, re
import requests as rq
from threading import Thread



class Murrsuit_Boter:
    def __init__(self, subs):
        self.reddit = praw.Reddit(
            username='Purple_scale_boi',
            password='Usps@5day',
            client_id='LqxEeoiHdpajQg',
            client_secret='3fc7-8qG1HBlBmzfKd1MqAnk9vU',
            user_agent='MurrsuitDowloader  by u/Purple_scale_boi'

        )
        self.img_exts = re.compile("\/*.(jpg|jpeg|png|gif)$")
        self.subs = subs

    def CreateThreadObjects(self):
        '''
        Creates Thread Objects for each subreddit passed into the class
        Then Starts Them
        '''
        threads = []
        for sub in self.subs:
            threads.append(Thread(target=self.SubThread, args=(sub,), name=sub))
            print(f"Thread for {sub} Created")
        for thread in threads:
            thread.start()
            print(f"Thread for {thread.name} starting :3")

    def SubThread(self, sub: str):
        '''

        :param sub: str
        :return:
        '''
        subreddit = self.reddit.subreddit(sub)
        for submission in subreddit.stream.submissions():
            self.Dowload(submission, sub)

    def Dowload(self, submission, sub):
        if not os.path.exists(str(sub)):
            os.mkdir(str(sub))

        url = submission.url

        IsMatch = len(self.img_exts.findall(url)) > 0
        if IsMatch:
            print(f"Dowloading {url}")
            image_data = rq.get(url, stream=True).content
            fExt = self.img_exts.findall(url)[0]
            bytes = url.encode('ascii')
            base64_bytes = base64.b64encode(bytes)
            base64_message = base64_bytes.decode('ascii')

            filename = os.path.join(str(sub), str(base64_message) + str("." + fExt))
            with open(filename, 'wb+') as f:
                f.write(image_data)
                print(f.name)

    def Start(self):
        '''
        Launch The Bot
        Creates multiple Threads :3
        '''
        print("-----------Starting Bot--------------------")
        self.CreateThreadObjects()
