from . import LoadComputers
from ..models import Server


class LoadWorkstations(LoadComputers):
    model = Server
