# character.py

class Character:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.health = 100
        self.energy = 100
        self.level = 1
        self.xp = 0
        self.skill_points = 0  # Points earned for leveling up that can be used to improve skills
        self.skills = {"Strength": 10, "Agility": 8, "Intelligence": 8}
        self.items = ["Basic Sword", "Health Potion"]
        self.gold = 50  # Currency the player can use for trading

    def gain_xp(self, amount):
        """Gain experience points and level up if enough XP is accumulated."""
        self.xp += amount
        print(f"{self.name} gained {amount} XP! Current XP: {self.xp}/{self.level * 100}")

        # Check if the character can level up
        while self.xp >= self.level * 100:
            self.level_up()

    def level_up(self):
        """Level up the character, increase stats, and provide skill points."""
        self.level += 1
        self.xp -= (self.level - 1) * 100  # Subtract XP needed for the previous level
        self.skill_points += 3  # Award skill points upon leveling up
        self.health = 100  # Fully restore health on level up
        print(f"{self.name} has leveled up to Level {self.level}!")
        print(f"You have gained 3 skill points! Total skill points: {self.skill_points}")

    def increase_skill(self, skill_name):
        """Increase a specific skill using skill points."""
        if self.skill_points > 0:
            if skill_name in self.skills:
                self.skills[skill_name] += 1
                self.skill_points -= 1
                print(
                    f"Increased {skill_name} to {self.skills[skill_name]}. Remaining skill points: {self.skill_points}")
            else:
                print(f"Skill '{skill_name}' not found.")
        else:
            print("No skill points available.")

    def use_item(self, item_name):
        """Use an item from the inventory."""
        if item_name in self.items:
            if item_name == "Health Potion":
                self.health = min(self.health + 50, 100)
                self.items.remove(item_name)
                print(f"{self.name} used a Health Potion. Health restored to {self.health}.")
            else:
                print(f"{item_name} can't be used right now.")
        else:
            print(f"{item_name} not in inventory.")

    def add_item(self, item_name):
        """Add an item to the character's inventory."""
        self.items.append(item_name)
        print(f"{item_name} has been added to your inventory.")

    def show_status(self):
        """Display the character's status."""
        status = (
            f"Name: {self.name}\n"
            f"Species: {self.species}\n"
            f"Level: {self.level}\n"
            f"XP: {self.xp}/{self.level * 100}\n"
            f"Health: {self.health}/100\n"
            f"Energy: {self.energy}/100\n"
            f"Skill Points: {self.skill_points}\n"
            f"Skills: {self.skills}\n"
            f"Items: {self.items}\n"
            f"Gold: {self.gold}"
        )
        print(status)
        return status

    def buy_item(self, item_name, cost):
        """Purchase an item if the player has enough gold."""
        if self.gold >= cost:
            self.gold -= cost
            self.add_item(item_name)
            print(f"You bought {item_name} for {cost} gold. Remaining gold: {self.gold}")
        else:
            print(f"Not enough gold to purchase {item_name}. You need {cost - self.gold} more gold.")

    def sell_item(self, item_name, sell_price):
        """Sell an item from the inventory for gold."""
        if item_name in self.items:
            self.items.remove(item_name)
            self.gold += sell_price
            print(f"Sold {item_name} for {sell_price} gold. Total gold: {self.gold}")
        else:
            print(f"You don't have {item_name} to sell.")

    def rest(self):
        """Rest and restore energy."""
        self.energy = 100
        print(f"{self.name} rested and restored their energy to full (100).")
