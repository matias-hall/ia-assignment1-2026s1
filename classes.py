#task class
class task:
    def __init__(self, ID: str, estTime: int, difficulty: int, deadline: int, requiredSkill: str):
        self.ID = ID
        self.estTime = estTime
        self.difficulty = difficulty
        self.deadline = deadline
        self.requiredSkill = requiredSkill

    def __repr__(self):
        return f"task(ID={self.ID}, estTime={self.estTime}, difficulty={self.difficulty}, deadline={self.deadline}, requiredSkill={self.requiredSkill})"

#employee class
class employee:
    def __init__(self, ID: str, availableHours: int, skillLevel: int, skills: list = []):
        self.ID = ID
        self.availableHours = availableHours
        self.skillLevel = skillLevel
        self.skills = skills

    def __repr__(self):
        return f"employee(ID={self.ID}, availableHours={self.availableHours}, skillLevel={self.skillLevel}, skills={self.skills})"