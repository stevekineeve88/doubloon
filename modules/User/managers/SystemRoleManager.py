from modules.User.repositories.SystemRoleRepo import SystemRoleRepo
from modules.Util.DataList import DataList


class SystemRoleManager:
    def __init__(self, **kwargs):
        self.system_role_repo: SystemRoleRepo = kwargs.get("system_role_repo") or SystemRoleRepo()
        self.system_roles = None

    def get_all(self) -> DataList:
        if self.system_roles is not None:
            return self.system_roles
        result = self.system_role_repo.load_all()
        if not result.get_status():
            raise Exception("Could not load system roles")
        self.system_roles = DataList(result.get_data())
        return self.system_roles
