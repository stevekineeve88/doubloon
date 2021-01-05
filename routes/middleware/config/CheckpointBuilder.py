from routes.middleware.config.checkpoints.Checkpoint import Checkpoint


class CheckpointBuilder:
    def __init__(self, checkpoints: list):
        self.__checkpoints = checkpoints

    def passes(self):
        checkpoint: Checkpoint
        for checkpoint in self.__checkpoints:
            if checkpoint.passes():
                return True
        return False

    def passes_all(self):
        checkpoint: Checkpoint
        for checkpoint in self.__checkpoints:
            if not checkpoint.passes():
                return False
        return True
