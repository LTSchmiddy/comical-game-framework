

class Handler:
    def __init__(self, isStack):
        self.msgList = []
        self.isStackMode = isStack

    def notify(self, message, time=120, header=None):
        self.msgList.append(Notification(message, time, header))
        # print "NOTIFICATION:", message

    def pullFirst(self):
        return self.msgList.pop(0)

    def pullLast(self):
        return self.msgList.pop()

    def pullNext(self):
        if self.isStackMode:
            return self.pullLast()
        return self.pullFirst()

    def hasQueued(self):
        if len(self.msgList) > 0:
            return True
        return False




class Notification:
    def __init__(self, message, time, header=None):

        self.header = header
        self.message = message
        self.time = time
