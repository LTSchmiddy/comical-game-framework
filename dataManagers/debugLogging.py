

class Logger:
    def __init__(self, isStack):
        self.msgList = []
        self.isStackMode = isStack

    def log(self, message, object = None):
        self.msgList.append(Message(message, object))

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




class Message:
    def __init__(self, message, object):
        self.object = object
        self.message = message
