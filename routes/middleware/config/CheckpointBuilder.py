from routes.middleware.config.checkpoints.Checkpoint import Checkpoint


class CheckpointBuilder:
    """ Class for building checkpoints for middleware
    """

    def __init__(self, checkpoints: list):
        """ Constructor for CheckpointBuilder
        Args:
            (list) checkpoints: List of checkpoints
        """
        self.__checkpoints = checkpoints

    def passes(self) -> bool:
        """ Check if one checkpoint passes
        Returns:
            bool
        """
        checkpoint: Checkpoint
        for checkpoint in self.__checkpoints:
            if checkpoint.passes():
                return True
        return False

    def passes_all(self) -> bool:
        """ Check if all checkpoints pass
        Returns:
            bool
        """
        checkpoint: Checkpoint
        for checkpoint in self.__checkpoints:
            if not checkpoint.passes():
                return False
        return True
