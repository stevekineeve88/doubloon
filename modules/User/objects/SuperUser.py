from modules.User.objects.User import User


class SuperUser(User):
    def __init__(self):
        super().__init__()

    def to_dict(self):
        return {
            "id": self.get_id(),
            "user_status": self.get_user_status().to_dict(),
            "uuid": self.get_uuid(),
            "username": self.get_username(),
            "first_name": self.get_first_name(),
            "last_name": self.get_last_name(),
            "email": self.get_email(),
            "phone": self.get_phone(),
            "created_date": self.get_created_date()
        }
