from veryfi.client_base import Client as ClientBase

from veryfi.a_docs import ADocs
from veryfi.bank_statements import BankStatements
from veryfi.bussines_cards import BussinesCards
from veryfi.checks import Checks
from veryfi.documents import Documents
from veryfi.w2s import W2s
from veryfi.w8s import W8s
from veryfi.w9s import W9s


class Client(ClientBase, ADocs, BankStatements, BussinesCards, Checks, Documents, W2s, W8s, W9s):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        username: str,
        api_key: str,
        base_url: str = ClientBase.BASE_URL,
        api_version: str = ClientBase.API_VERSION,
        timeout: int = ClientBase.API_TIMEOUT,
    ):
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            api_key=api_key,
            base_url=base_url,
            api_version=api_version,
            timeout=timeout,
        )
        ADocs.__init__(self, super())
        BankStatements.__init__(self, super())
        BussinesCards.__init__(self, super())
        Checks.__init__(self, super())
        Documents.__init__(self, super())
        W2s.__init__(self, super())
        W8s.__init__(self, super())
        W9s.__init__(self, super())
