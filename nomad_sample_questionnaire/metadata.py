from pydantic import BaseModel
from typing import Literal


class NomadMetadata(BaseModel):
    """
    We are expecting a "nomad" field in the run start document which matches these elements.
    """

    experiment_uid: str
    endstation: Literal["SISSY1", "OAESE"]
