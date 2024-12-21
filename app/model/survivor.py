from typing import List, Any
from pydantic import BaseModel

class Survivor(BaseModel):
    pclass: int
    sex: int
    age: float
    fare: float
    port: str

    def getData(self) -> List[Any]:
        port = self._map_port()
        return [self.pclass, self.sex, self.age, self.fare, port["C"],port["Q"],port["S"] ]
    
    def _map_port(self) -> dict[str, bool]:
        _port = {"C":0,"Q": 0,"S": 0}
        _port[self.port] = 1
        return _port