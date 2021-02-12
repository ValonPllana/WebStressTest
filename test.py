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
def body_received(body):
    global req_done
    req_done += 1
def request_done(response):
    global req_made
    deferred = treq.json_content(response)
    req_made += 1
    deferred.addCallback(body_received)
    deferred.addErrback(lambda x: None)  # ignore errors
    return deferred


def request():
    deferred = treq.request('GET','https://rronp-weather-app.herokuapp.com/')

    deferred.addCallback(request_done)
    return deferred

def requests_generator():
    global req_generated

    yield None

while True:
    deferred = request()
    req_generated += 1
    # do not yield deferred here so cooperator won't pause until
    # response is received


