import  threading
from queue import Queue

from Spider import spider

from domain import *
from main import *

PROJECT_NAME='My web crawler'
HOMEPAGE='https://www.quora.com/'
DOMAIN_NAME=get_domain_name(HOMEPAGE)
QUEUE_FILE=PROJECT_NAME+ '/queue.txt'
CRAWLED_FILE=PROJECT_NAME+ '/crawled.txt'
NUMBER_OF_THREADS=8



def create_workers():
    for _ in  range(NUMBER_OF_THREADS):
        t=threading.Thread(target=work)
        t.daemon=True
        t.start()


def work():
    while True:
        url=queue.get()
        spider.crawl_page(threading.current_thread().name,url)
        queue.task_done()

queue=Queue()
spider(PROJECT_NAME,HOMEPAGE,DOMAIN_NAME)


def crawl():
    queued_links=file_to_set(QUEUE_FILE)
    if len(queued_links) >0:
        print(str(len(queued_links)) + 'links in queue')
        create_jobs()


def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)

    queue.join()
    crawl()



# Done
create_workers()
crawl()
