from crud import Crud
from repository.client_repository import ClientRepository


class Client(Crud):
    def __init__(self):
        self.repository = ClientRepository()
        self.menu('Client')
        self.repository.close_connection()

    def show(self):
        print('show')

    def add(self):
        print('add')

    def edit(self):
        print('edit')

    def delete(self):
        print('delete')
