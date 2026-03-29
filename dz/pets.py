class Pet:
    __name: str
    __weight: float
    __age: int
    __energy: int
    __hunger: int
    __days_in_hotel: int

    def __init__(self, name: str, weight: float, age: int, energy: int, hunger: int, days_in_hotel: int) -> None:
        self.__name = name
        self.__weight = weight
        self.__age = age
        self.__energy = energy
        self.__hunger = hunger
        self.__days_in_hotel = days_in_hotel

    def __str__(self):
        return f"{self.__name}: age={self.__age}, weight={self.__weight}kg, energy={self.__energy}, hunger={self.__hunger}, days={self.__days_in_hotel}"

    def get_name(self) -> str:
        return self.__name

    def get_age(self) -> int:
        return self.__age

    def get_weight(self) -> float:
        return self.__weight

    def get_energy(self) -> int:
        return self.__energy

    def get_hunger(self) -> int:
        return self.__hunger

    def get_days_in_hotel(self) -> int:
        return self.__days_in_hotel

    def print_info(self) -> None:
        print(str(self))

    def feed(self, food_amount: int) -> None:
        self.__hunger -= food_amount
        if self.__hunger < 0:
            self.__hunger = 0

    def get_daily_price(self) -> int:
        base_price = 50
        age_factor = self.__age * 2
        weight_factor = int(self.__weight * 1.5)
        energy_factor = int(self.__energy * 0.5)
        hunger_factor = int(self.__hunger * 0.3)
        return base_price + age_factor + weight_factor + energy_factor + hunger_factor

    def get_total_price(self) -> int:
        daily = self.get_daily_price()
        return daily * self.__days_in_hotel


class Dog(Pet):
    def __init__(self,
                 name: str,
                 weight: float,
                 age: int,
                 energy: int,
                 hunger: int,
                 days_in_hotel: int,
                 breed: str,
                 trained: bool):
        super().__init__(name, weight, age, energy, hunger, days_in_hotel)
        self.__breed = breed
        self.__trained = bool(trained)

    def get_breed(self) -> str:
        return self.__breed

    def is_trained(self) -> bool:
        return self.__trained

    def print_info(self) -> None:
        super().print_info()
        print(f"Breed: {self.__breed}, Trained: {self.__trained}")

    def feed(self) -> None:
        super().feed(25)
        self._Pet__energy += 10
        if self._Pet__energy > 100:
            self._Pet__energy = 100
        print(f"{self.get_name()} покормлен. Hunger: {self.get_hunger()}, Energy: {self.get_energy()}")

    def play(self) -> None:
        cost = 5 if self.__trained else 10
        cur = self._Pet__energy
        if cur < cost:
            print(f"{self.get_name()} устал(а) и не может играть. Energy: {cur}")
            return
        self._Pet__energy = cur - cost
        self._Pet__hunger += 10
        if self._Pet__hunger > 100:
            self._Pet__hunger = 100
        print(f"{self.get_name()} играет. Energy: {self.get_energy()}, Hunger: {self.get_hunger()}")

    def get_daily_price(self) -> int:
        w = self.get_weight()
        price = 700
        if w > 50:
            price += 500
        elif w > 30:
            price += 200
        return int(price)


class Cat(Pet):
    def __init__(self,
                 name: str,
                 weight: float,
                 age: int,
                 energy: int,
                 hunger: int,
                 days_in_hotel: int,
                 indoor: bool,
                 favorite_spot: str):
        super().__init__(name, weight, age, energy, hunger, days_in_hotel)
        self.__indoor = bool(indoor)
        self.__favorite_spot = favorite_spot if favorite_spot.strip() else "unknown"

    def print_info(self) -> None:
        super().print_info()
        print(f"Indoor: {self.__indoor}, Favorite spot: {self.__favorite_spot}")

    def feed(self) -> None:
        super().feed(20)
        self._Pet__energy += 5
        if self._Pet__energy > 100:
            self._Pet__energy = 100
        print(f"{self.get_name()} покормлена. Hunger: {self.get_hunger()}, Energy: {self.get_energy()}")

    def play(self) -> None:
        if self._Pet__energy < 20:
            print(f"{self.get_name()} капризничает и не хочет играть. Energy: {self.get_energy()}")
            return
        self._Pet__energy -= 8
        if self._Pet__energy < 0:
            self._Pet__energy = 0
        self._Pet__hunger += 8
        if self._Pet__hunger > 100:
            self._Pet__hunger = 100
        print(f"{self.get_name()} поиграла с мячиком. Energy: {self.get_energy()}, Hunger: {self.get_hunger()}")

    def get_daily_price(self) -> int:
        return 500


class Parrot(Pet):
    def __init__(self,
                 name: str,
                 weight: float,
                 age: int,
                 energy: int,
                 hunger: int,
                 days_in_hotel: int,
                 can_talk: bool,
                 vocabulary_size: int):
        super().__init__(name, weight, age, energy, hunger, days_in_hotel)
        self.__can_talk = bool(can_talk)
        self.__vocabulary_size = max(0, int(vocabulary_size))

    def print_info(self) -> None:
        super().print_info()
        print(f"Can talk: {self.__can_talk}, Vocabulary size: {self.__vocabulary_size}")

    def feed(self) -> None:
        super().feed(15)
        self._Pet__energy += 8
        if self._Pet__energy > 100:
            self._Pet__energy = 100
        print(f"{self.get_name()} покормлен(а). Hunger: {self.get_hunger()}, Energy: {self.get_energy()}")

    def play(self) -> None:
        if self._Pet__energy < 10:
            print(f"{self.get_name()} устал(а) и не играет. Energy: {self.get_energy()}")
            return
        self._Pet__energy -= 6
        if self._Pet__energy < 0:
            self._Pet__energy = 0
        self._Pet__hunger += 6
        if self._Pet__hunger > 100:
            self._Pet__hunger = 100
        if self.__can_talk and self.__vocabulary_size > 0:
            print(f"{self.get_name()} играет и говорит: 'Привет!'")
        else:
            print(f"{self.get_name()} играет и издаёт звуки.")
        print(f"Energy: {self.get_energy()}, Hunger: {self.get_hunger()}")

    def get_daily_price(self) -> int:
        price = 600
        if self.__can_talk:
            price += 100 + (self.__vocabulary_size // 10) * 10
        return int(price)