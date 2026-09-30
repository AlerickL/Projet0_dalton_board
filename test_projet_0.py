import numpy as np
import time as t

class GaltonTable:
    def __init__(self,height:int):
        self.__height:int = height
        self.__collision_cheville:list[int] = [0 for _ in range(int(self.__height*(self.__height+1)/2))]

    def __modify_peg(self,a:int,b:int,value:int) -> None:
        self.__collision_cheville[int((a*(a+1)/2)+b)] += value

    def __str__(self) -> str:
        return f"{self.__collision_cheville}"

    @staticmethod
    def __def_func_proba(p:float) -> callable:
        """Définir une fonction pour la proba

        Args:
            p (float): la proba

        Returns:
            _type_: fonction
        """
        return lambda t : t<=p

    @staticmethod
    def __create_table(nber_ball:int,proba_law:callable) -> np.ndarray:
        """Créer la table qui détermine chaque bille vat à gauche (0) ou à droite (1)

        Args:
            nber_bin (int): _description_
            proba_law (callable): _description_

        Returns:
            _type_: _description_
        """
        table_stat = np.random.uniform(0,1,nber_ball)
        return np.astype(proba_law(table_stat),int) # Avec solution de William (pour la fonction a utiliser spécifiquement)


    def __modify_pegs(self,table:np.ndarray,nber_addition:int) -> None:          # Pas sûr que se soit optimisé.
        """Modifi la table de galton pour indiquer le peg à été touché ou non

        Args:                       
            table (np.ndarray): _description_
            nber_addition (int): Le cardinal du nombre d'addition (combientième)
            galton (GaltonTable): _description_
        """
        #table.sort()
        #print(table[table==0].size)
        # for i in range(len(table)):                       ############# 3.5 secondes pour 300 000 bins, croissance linéaire
        #     galton.modify_peg(nber_addition,table[i],galton.find_peg(nber_addition,table[i])+1)

        for i in range(nber_addition+1):                      ############# 0.04 secondes ! Beaucoup plus rapide ! croissance linéaire
            self.__modify_peg(nber_addition,i,table[table==i].size)

    def simulate_fall(self, nber_ball:int, proba:float|int = 0.5) -> list[int]:
        """Simule une chute

        Args:
            height (_type_): hauteur de la table de galton (on considère les sacs)
            nber_bin (_type_): le nombre de bin
            galton (_type_): _description_
            proba_law (_type_):fonction lois proba

        Returns:
            _type_: la table de galton
        """
        proba_law = GaltonTable.__def_func_proba(proba)
        self.__modify_peg(0,0,nber_ball)
        table:np.ndarray = GaltonTable.__create_table(nber_ball,proba_law)
        self.__modify_pegs(table,1)
        for i in range(2,self.__height):
            table += GaltonTable.__create_table(nber_ball,proba_law)
            self.__modify_pegs(table,i)
        return self.__collision_cheville


# a = create_table(10,lambda t : t>=0.5)
# print(a)
# c = GaltonTable(3)
# find_nber(a,2,c)
# print(c)

########### EXEMPLE : print(simulate_fall(2,500000,GaltonTable(2),lambda t : t>=0.5))
deb = t.perf_counter()
h = 100
p = 0.5
g = GaltonTable(h)               ################# AUTRE EXEMPLE, plusieurs lancés 
print(g.simulate_fall(10000,p))
#print(g.simulate_fall(1000,p))
#print(simulate_fall(5,5000,g,lambda t : t>=0.2))
print(t.perf_counter()-deb)


