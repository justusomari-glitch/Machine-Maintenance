
from pydantic import BaseModel

class MachineInputs(BaseModel):
        machine_age_days: int
        temperature: float
        vibration: float
        pressure: float
        section: str
        component: str
        subcomponent: str