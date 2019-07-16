from typing import List

from plenum.server.quorums import Quorums


class ConsensusDataProvider:
    """
    This is a 3PC-state shared between Ordering, Checkpoint and ViewChange services.
    TODO: Consider depending on audit ledger
    TODO: Consider adding persistent local storage for 3PC certificates
    TODO: Restore primary name from audit ledger instead of passing through constructor
    """
    def __init__(self, name: str, validators: List[str], primary_name: str):
        self._name = name
        self.set_validators(validators)
        self.view_no = 0
        self.waiting_for_new_view = False
        self.primary_name = primary_name
        self.preprepared = []
        self.prepared = []
        self.checkpoints = []
        self.stable_checkpoint = 0
        self.log_size = 300 # TODO: use config value

    @property
    def name(self) -> str:
        return self._name

    def set_validators(self, validators: List[str]):
        self._validators = validators
        self._quorums = Quorums(len(validators))

    @property
    def validators(self) -> List[str]:
        """
        List of validator nodes aliases
        """
        return self._validators

    @property
    def quorums(self) -> Quorums:
        """
        List of quorums
        """
        return self._quorums

    @property
    def is_primary(self) -> bool:
        return self.primary_name == self.name
