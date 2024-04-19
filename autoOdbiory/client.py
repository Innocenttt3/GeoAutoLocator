# client.py

class Client:
    def __init__(self, client_id: int, email: str, content: str, name: str):
        self.client_id = client_id
        self.email = email
        self.content = content
        self.name = name

    def __repr__(self):
        return f"Client(id={self.client_id}, email='{self.email}', name='{self.name}', content='{self.content}')"
