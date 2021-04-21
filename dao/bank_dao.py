from abc import abstractmethod, ABC


class BankDAO(ABC):
    @abstractmethod
    def create_user(self, new_user):
        pass

    @abstractmethod
    def get_users(self):
        pass

    @abstractmethod
    def update_user(self):
        pass

    @abstractmethod
    def delete_user(self):
        pass
