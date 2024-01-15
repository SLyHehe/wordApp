import json
import requests
from pushbullet import Pushbullet
import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import sys

# variables
pb = Pushbullet('')

# setup logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)
log.addHandler(console_handler)


def dictionary():

    validWord = False
    while validWord == False:

        word = requests.get('https://random-word-api.herokuapp.com/word?number=1')
        wordDict = json.loads(word.text)
        cleanWord = wordDict[0]

        definition = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/' + str(cleanWord))
        definitionDict = json.loads(definition.text)
        

        if 'title' not in definitionDict:
            validWord = True 
            logging.debug('Word is valid: ' + cleanWord)
        else:
            logging.debug('Word is not valid: ' + cleanWord)

    cleanDefinition = definitionDict[0]['meanings'][0]['definitions'][0]['definition']

    if 'example' in definitionDict[0]['meanings'][0]['definitions'][0]:
        example = definitionDict[0]['meanings'][0]['definitions'][0]['example']
    else:
        example = 'Example not found'

    logging.debug("Example: " + example)
    

    if 'origin' in definitionDict[0]:
        origin = definitionDict[0]['origin']
    else:
        origin = 'Origin Not Found'

    logging.debug("Origin: " + origin)
    
    pb.push_note("Today's word is " + cleanWord.capitalize(),  "Definition: " +
                 cleanDefinition.capitalize() +
                 "\nExample: " + example.capitalize() +
                 "\nOrigin: " + origin.capitalize())
    
def main():

    # setup the scheduler
    Scheduler = BlockingScheduler(timezone=pytz.timezone('Pacific/Auckland'))
    Scheduler.add_job(dictionary, 'cron', hour="*", minute="*")
    # start the jobs
    Scheduler.start()

if __name__ == '__main__':
    main()




            

    


   
