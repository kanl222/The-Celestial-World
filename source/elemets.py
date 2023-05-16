class Damage:
    def __init__(self, amount:int, dmg_type:str,effect=None):
        self.amount = amount
        self.dmg_type = dmg_type
        self.effect = effect
    
    def apply_damage(self, target):
        target.health -= self.amount
        if self.effect:
            self.effect.update_start_time()
            target.effects.add_effect(self.effect)

