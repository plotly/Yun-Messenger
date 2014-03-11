from YunMessenger import Console

console = Console.Console()

def messageHandler1(msg):
    print 'Handler 1! ', msg

def messageHandler2(msg):
    print 'Handler 2! ', msg

console.onMessage['subscriber_1'] = messageHandler1
console.onMessage['subscriber_2'] = messageHandler2

console.run()
