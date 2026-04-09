class Message:
    def __init__(self, user_id, channel_id, content):
        self.user_id = user_id
        self.channel_id = channel_id
        self.content = content

class ChatServer:
    def __init__(self):
        self.messages = []
    
    def send_message(self, message):
        self.messages.append(message)

    def stats(self):
        print('Total messages:', len(self.messages))
