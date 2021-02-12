from twisted.internet import reactor, task
from twisted.web.client import HTTPConnectionPool
import treq

req_generated = 0
req_made = 0
req_done = 0
cooperator = task.Cooperator()
pool = HTTPConnectionPool(reactor)


def counter():
    '''This function gets called once a second and prints the progress at one
    second intervals.
    '''
    print("Requests: {} generated; {} made; {} done".format(
    req_generated, req_made, req_done))
# reset the counters and reschedule ourselves
req_generated = req_made = req_done = 0
reactor.callLater(1, counter)
