import Console

def sub1(msg):
    print 'sub1: ', msg

def sub2(msg):
    print 'sub1: ', msg

c = Console()
c.onMessage['subscriber_1'] = sub1
c.onMessage['subscriber_2'] = sub2

c.run()