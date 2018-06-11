import sys
import time

import qt5reactor
from PyQt5.QtCore import QCoreApplication
from twisted.internet.defer import inlineCallbacks, Deferred

@inlineCallbacks
def test(nums):
    print(nums)
    time.sleep(2)
    yield 3

@inlineCallbacks
def my_callbacks():
    from twisted.internet import reactor
    print("first callback")
    result = yield 1
    print("second callback got {} ".format(result))
    d = Deferred()
    d.addCallback(test)
    reactor.callLater(1,d.callback,123)
    result = yield d
    print("third callback got {result}".format(result=result))
    d = Deferred()
    reactor.callLater(5,d.errback,Exception(3))
    try:
        yield d
    except Exception as e:
        result = e


    print("fourth calll back got {result}".format(result = result))






if __name__ == '__main__':
    print("" in "")
