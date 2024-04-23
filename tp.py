import random
import matplotlib.pyplot as plt
from collections import deque

class Renard:
    def __init__(self):
        self.age = 0
        self.faim = 0
        self.vivant = True

    def manger(self):
        self.faim = 0

    def vieillir(self):
        self.age += 1
        self.faim += 1
        if self.faim > 1 or self.age > 6:
            self.vivant = False

    def peut_se_reproduire(self):
        return self.age % 12 == 0 and self.vivant

class Lapin:
    def __init__(self, sexe):
        self.age = 0
        self.sexe = sexe
        self.faim = 0
        self.vivant = True

    def manger(self):
        self.faim = 0

    def vieillir(self):
        self.age += 1
        self.faim += 1
        if self.age > 6 or (self.age > 4 and self.faim > 1):
            self.vivant = False
            
    def peut_se_reproduire(self):
        return self.age >= 1 and self.vivant

class Carotte:
    def __init__(self):
        self.mature = False

    def grandir(self):
        self.mature = True

class Jardin:
    def __init__(self, nb_carottes_init=200):
        self.lapins = [Lapin('M'), Lapin('F')]
        self.carottes = deque([Carotte() for _ in range(nb_carottes_init)])
        self.renards = []
        self.semaines = 0

    def semer_carottes(self, nb_carottes=200):
        self.carottes.extend([Carotte() for _ in range(nb_carottes)])

    def nourrir_lapins(self):
        for lapin in self.lapins:
            if lapin.vivant and self.carottes:
                carotte = self.carottes.popleft()
                if carotte.mature:
                    lapin.manger()

    def nourrir_renards(self):
        for renard in self.renards:
            if renard.vivant and len(self.lapins) > 0:
                lapin_a_manger = min(1, len(self.lapins))
                for _ in range(lapin_a_manger):
                    lapin = random.choice(self.lapins)
                    self.lapins.remove(lapin)
                renard.manger()

    def vieillir_lapins(self):
        for lapin in self.lapins:
            lapin.vieillir()

    def vieillir_renards(self):
        for renard in self.renards:
            renard.vieillir()

    def reproduire_lapins(self):
        if len([lapin for lapin in self.lapins if lapin.peut_se_reproduire() and lapin.sexe == 'M']) > 0 and \
        len([lapin for lapin in self.lapins if lapin.peut_se_reproduire() and lapin.sexe == 'F']) > 0:
            self.lapins.extend([Lapin(random.choice(['M', 'F'])) for _ in range(random.randint(1, 6))])

    def reproduire_renards(self):
        if len(self.renards) > 1:
            self.renards.extend([Renard() for _ in range(random.randint(1, 3))])

    def passer_semaine(self):
        self.nourrir_lapins()
        self.vieillir_lapins()
        self.reproduire_lapins()
        self.lapins = [lapin for lapin in self.lapins if lapin.vivant]
        for carotte in self.carottes:
            carotte.grandir()

        # Ajouter un renard après un mois
        if self.semaines % 12 == 0:
            self.renards.append(Renard())

        # Nourrir et vieillir les renards si ils existent
        if self.renards:
            self.nourrir_renards()
            self.vieillir_renards()
            self.renards = [renard for renard in self.renards if renard.vivant]

        # Reproduction des renards
        if self.semaines % 12 == 0:
            self.reproduire_renards()

        self.semaines += 1

    def population_lapins(self):
        return len(self.lapins)

    def population_carottes(self):
        return len(self.carottes)

    def population_renards(self):
        return len(self.renards)

# Simulation
jardin = Jardin()
pop_lapins = []
pop_carottes = []
pop_renards = []

for semaine, _ in enumerate(range(6*52)):
    if semaine % 52 == 0:
        jardin.semer_carottes()
    jardin.passer_semaine()
    pop_lapins.append(jardin.population_lapins())
    pop_carottes.append(jardin.population_carottes())
    pop_renards.append(jardin.population_renards())

# Tracer les populations
plt.plot(pop_lapins, label='Lapins')
plt.plot(pop_carottes, label='Carottes')
plt.plot(pop_renards, label='Renards')
plt.title("Évolution des populations de lapins, de carottes et de renards dans le jardin")
plt.xlabel("Semaines")
plt.ylabel("Population")
plt.legend()
plt.show()
