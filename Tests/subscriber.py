from Linino import Console

def subscriberHandler1(msg):
    print 'subscriberHandler1: ', msg

def subscriberHandler2(msg):
    print 'subscriberHandler2: ', msg

def brokenSubscriber(msg):
    1/0

c = Console.Console()
c.onMessage['subscriber1'] = subscriberHandler1
c.onMessage['subscriber2'] = subscriberHandler2
c.onMessage['brokenSubscriber'] = brokenSubscriber

c.run()