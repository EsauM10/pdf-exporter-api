from typing import Any, Dict


class StudentModel:
    def __init__(self, name: str, score1: float, score2: float, score3: float, mean: float) -> None:
        self.name   = name
        self.score1 = score1
        self.score2 = score2
        self.score3 = score3
        self.mean   = mean
    
    
    @staticmethod
    def from_dict(data: Dict[str, Any]):
        required_params = ['name', 'score1', 'score2', 'score3', 'mean']
        
        for param in required_params:
            if(not param in data):
                raise Exception(f'Missing param {param}')

        return StudentModel(
            name=str(data['name']),
            score1=float(data['score1']),
            score2=float(data['score2']),
            score3=float(data['score3']),
            mean=float(data['mean'])
        )
    
    