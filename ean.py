#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Universidad EAN (Bogotá - Colombia)
# Departamento de Sistemas
# Faculta de Ingeniería
#
# Proyecto EAN Python Collections
# @author Luis Cobo (lacobo@universidadean.edu.co)
# Fecha: Mar 09 2026
# Versión: 0.0.1 -> 16 de febrero de 2026 -> Implementación inicial
# Versión: 0.0.2 -> 09 de marzo de 2026 -> Implementación de nodos
# Versión: 0.0.3 -> 14 de marzo de 2026 -> Implementación de pilas
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import math
from datetime import datetime
from math import sqrt, pi

# Definición de elementos genéricos que usaremos a continuación
from typing import TypeVar, Generic

# La clase Nulo: representa un nodo nulo
class Nulo:
    def __init__(self):
        pass

    def __str__(self):
        return "nulo"

    def __repr__(self):
        return "Nulo()"

    def __getattr__(self, nombre: str):
        raise AttributeError(f"El atributo {nombre} no existe en el nodo nulo")

    def __eq__(self, otro: object) -> bool:
        if otro is None:
            raise ValueError("El valor nulo no puede ser comparado con None")
        return isinstance(otro, Nulo)

    def __ne__(self, otro: object) -> bool:
        if otro is None:
            raise ValueError("El valor nulo no puede ser comparado con None")
        return not self.__eq__(otro)

    @property
    def es_nulo(self) -> bool:
        return True

    @property
    def no_es_nulo(self) -> bool:
        return False        

# ----------------------------------------

# Variable global que representa el valor nulo.
nulo = Nulo()

# ------------------------------------------------------------

T = TypeVar('T')

# Los nodos son objetos que permiten almacenar información
# Cada nodo contiene un atributo llamado "información"
# y otro llamado "sig".
class Nodito(Generic[T]):
    def __init__(self, informacion : T):
        self.__informacion = informacion
        self.__siguiente  = nulo
        if informacion is None or informacion == nulo:
            raise ValueError("El valor nulo no puede ser almacenado en un nodo")

    @property
    def es_nulo(self) -> bool:
        return False

    @property
    def no_es_nulo(self) -> bool:
        return True

    @property
    def informacion(self) -> T:
        return self.__informacion

    @informacion.setter
    def informacion(self, valor: T):
        if valor is None or valor == nulo:
            raise ValueError("El valor nulo no puede ser almacenado en un nodo")
        self.__informacion = valor

    @property
    def sig(self) -> 'Nodito | Nulo':
        return self.__siguiente

    @sig.setter
    def sig(self, sig: 'Nodito | Nulo'):
        if sig is None:
            raise ValueError("En este curso nunca usamos None con Noditos. Revise la presentación")
        self.__siguiente = sig

    def __getattr__(self, attr : str):
        raise AttributeError(f"El atributo {attr} no existen en los noditos.\nEn este curso un nodito solo tiene informacion y sig.")

    def __eq__(self, otro: object) -> bool:
        if otro is None:
            raise ValueError("Un nodito no puede ser comparado con None. Uso nulo en su lugar")
        return isinstance(otro, Nodito) and self.informacion == otro.informacion

    def __ne__(self, otro: object) -> bool:
        if otro is None:
            raise ValueError("Un nodito no puede ser comparado con None. Use nulo en su lugar")
        return not self.__eq__(otro)

    def __setattr__(self, attr : str, valor: object):
        if attr == "data" or attr == "value" or attr == "next" or attr == "siguiente" or attr == "valor" or attr == "info" or attr == "dato":
            raise AttributeError(f"El atributo {attr} no existe en los noditos.\nEn este curso un nodito solo tiene informacion y sig.")
        super().__setattr__(attr, valor)

    def __str__(self):
        return f"{str(self.informacion)} -> {str(self.sig)}"


# ---------------------------------------------------------------------
import pandas as pd
from dataclasses import dataclass

@dataclass(frozen=True)
class Persona:
    """
    Clase que representa una persona
    """

    # Atributos de la clase Persona
    cedula: int
    nombre: str
    edad: int
    genero: str
    num_hijos: int
    nivel_educativo: str
    estrato: int
    ingresos: int
    peso: int
    altura: int
    fuma: bool
    usa_lentes: bool
    tiene_casa: bool
    tiene_carro: bool

    # Métodos de la clase persona
    def año_nacimiento(self) -> int:
        return datetime.now().year - self.edad

    def peso_ideal(self) -> float:
        return (self.altura - 100) * 0.9

    def imc(self) -> float:
        return self.peso / (self.altura / 100) ** 2

# ---------------------------------------------
def crear_lista_nodos_personas() -> Nodito[Persona]:
    """
    Permite crear una lista con las personas que están
    en el archivo
    :return: la lista con las personas
    """
    archivo = "https://github.com/luiscobo/poo/raw/refs/heads/main/people.csv"
    df = pd.read_csv(archivo, sep=";", encoding="utf-8")

    cabeza  = nulo
    actual  = nulo

    for index, row in df.iterrows():
        cedula = row["Cedula"]
        nombre = row["Nombres"].upper()
        edad = row["Edad"]
        genero = row["Genero"]
        num_hijos = row["No de hijos"]
        nivel_educativo = row["Nivel Educativo"]
        estrato = row["Estrato Socio"]
        ingresos = row["Ingresos"]
        peso = row["Peso"]
        altura = row["Talla"]
        fuma = row["Fuma"] == "SI"
        usa_lentes = row["Usa Lentes"] == "SI"
        tiene_casa = row["Tiene Casa"] == "SI"
        tiene_carro = row["Tiene Automovil"] == "SI"
        p = Persona(cedula, nombre, edad, genero, num_hijos, nivel_educativo, estrato, ingresos, peso, altura, fuma, usa_lentes, tiene_casa, tiene_carro)
        nodo = Nodito[Persona](p)
        if cabeza is nulo:
            cabeza = nodo
            actual = nodo
        else:
            actual.sig = nodo
            actual = nodo
    return cabeza

# ---------------------------------------------------------------------
def crear_lista_nodos_equipos() -> Nodito:
    """
    Permite crear una lista con los equipos de fútbol que están
    en el archivo
    :return: la cabeza de una lista de nodos con equipos
    """
    archivo = "https://raw.githubusercontent.com/luiscobo/poo/refs/heads/main/LaLiga.csv"
    df = pd.read_csv(archivo, encoding="utf-8")

    cabeza = nulo
    actual = nulo
    
    for index, row in df.iterrows():
        año = int(row["season"][:4])
        nombre = row["club"]
        partidos_ganados_local = int(row["home_win"])
        partidos_ganados_visitante = int(row["away_win"])
        partidos_perdidos_local = int(row["home_loss"])
        partidos_perdidos_visitante = int(row["away_loss"])
        partidos_empatados = int(row["matches_drawn"])
        goles_local = int(row["home_goals"])
        goles_visitante = int(row["away_goals"])
        goles_en_contra = int(row["goals_conceded"])
        e = (año, nombre, partidos_ganados_local, partidos_ganados_visitante,
                         partidos_perdidos_local, partidos_perdidos_visitante,
                         partidos_empatados, goles_local, goles_visitante,
                         goles_en_contra)
        nodo = Nodito(e)
        if cabeza is nulo:
            cabeza = nodo
            actual = nodo
        else:
            actual.sig = nodo
            actual = nodo
        
    return cabeza

# ---------------------------------------------------------------------
@dataclass(frozen=True)
class Departamento:
    """
    Clase que representa la información de un departamento de Colombia
    """
    nombre: str
    cant_municipios: int
    capital: str
    superficie: float
    poblacion: int
    densidad: float
    indice_desarrollo_humano: float
    fecha_creacion: int
    region: str

# ---------------------------------------------------------------------
def crear_lista_nodos_departamentos() -> Nodito[Departamento] | Nulo:
    """
    Permite obtener una lista de departamentos a partir del archivo
    de datos que se encuentra en github
    :return: Una lista con la información de los departamentos
    """
    archivo = "https://raw.githubusercontent.com/luiscobo/poo/refs/heads/main/departamentos2.csv"
    df = pd.read_csv(archivo, encoding="utf-8")
    cabeza = nulo
    actual = nulo
    for index, row in df.iterrows():
        nombre = row["Departamento"]
        municipios = row["Municipios"]
        capital = row["Capital"]
        superficie = row["Superficie"]
        poblacion = row["Población"]
        densidad = row["Densidad"]
        idh = row["IDH6"]
        fecha = row["Fecha de creación"]
        region = row["Región"]
        depto = Departamento(nombre, cant_municipios=municipios, capital=capital, superficie=superficie,
                             poblacion=poblacion, densidad=densidad, indice_desarrollo_humano=idh, fecha_creacion=fecha,
                             region=region)
        nodo = Nodito[Departamento](depto)
        if cabeza is nulo:
            cabeza = nodo
            actual = nodo
        else:
            actual.sig = nodo
            actual = nodo
    return cabeza

# ----------------------------------------------------------------------------------------

def obtener_nodo_pos(cab : Nodito, indice : int) -> Nodito | Nulo:
    """
    Permite obtener el nodo ubicado en una determinada posición
    :param cab: el primer nodo de la lista
    :param indice: la posición que se desea obtener
    :return: el nodo ubicado en la posición especificada por indice
    """
    act = cab
    for i in range(indice):
        act = act.sig
    return act
    
# ----------------------------------------------------------------------------------------

class PilaVacia(Exception):
    """
    Excepción generada cuando la pila está vacía

    Atributos:
        mensaje
    """
    def __init__(self, mensaje: str = "No se puede eliminar un elemento de una lista vacía"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

# -----------------------------------------------------------------------------------------

class Pila(Generic[T]):
    """
    Una pila (stack) es una secuencia de cero o más elementos de un mismo tipo,
    que solamente puede crecer y decrecer por uno de sus extremos. Sigue la
    filosofía LIFO (Last In First Out), donde el último elemento que se ha agregado
    es el primero en salir.
    """

    # Constructor de la clase Pila
    def __init__(self):
        self.__cabeza = nulo

    # Agregar un elemento al tope de la pila
    def añadir(self, elemento: T) -> None:
        nuevo_nodo = Nodito(elemento)
        nuevo_nodo.sig = self.__cabeza
        self.__cabeza = nuevo_nodo

    # Eliminar el elemento del tope de la pila
    def eliminar(self) -> None:
        if self.__cabeza is not nulo:
            self.__cabeza = self.__cabeza.sig
        else:
            raise PilaVacia()

    # Obtener el elemento del tope de la pila
    @property
    def primero(self) -> T:
        if self.__cabeza is not nulo:
            return self.__cabeza.informacion
        else:
            raise PilaVacia("No podemos obtener el primer elemento de una pila vacía")

    # Permite saber si la pila está vacía
    @property
    def esta_vacia(self) -> bool:
        return self.__cabeza is nulo

    # Permite saber si la pila no está vacía
    @property
    def no_esta_vacia(self) -> bool:
        return self.__cabeza is not nulo

    # Crear una copia de la pila
    def copiar(self) -> 'Pila[T]':
        copia = Pila[T]()
        act = self.__cabeza
        act_copia = None
        while act.no_es_nulo:
            nodo = Nodito[T](act.informacion)
            if copia.__cabeza is nulo:
                copia.__cabeza = nodo
                act_copia = nodo
            else:
                act_copia.sig = nodo
                act_copia = nodo
            act = act.sig
        return copia

    # Representación como str de la pila
    def __str__(self):
        act = self.__cabeza
        out = ""
        while act.no_es_nulo:
            out += str(act.informacion) + " -> "
            act = act.sig
        return out if len(out) == 0 else out[:-4]

# -----------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Municipio:
    """
    Esta es la información de un municipio de Colombia
    """
    codigo: int
    nombre: str
    poblacion_urbana: int
    poblacion_rural: int
    departamento: str
    es_capital: bool

    def poblacion_total(self) -> int:
        return self.poblacion_rural + self.poblacion_urbana


# -----------------------------------------------------------------------------------------

def crear_pila_municipios() -> Pila[Municipio]:
    """
    Permite obtener una pila con la información de los municipios de Colombia
    :return: una pila de objetos Municipio
    """
    archivo = "https://raw.githubusercontent.com/luiscobo/poo/refs/heads/main/municipios.csv"
    df = pd.read_csv(archivo, encoding="utf-8")
    pila = Pila[Municipio]()
    for index, row in df.iterrows():
        codigo = int(row["código"])
        nombre = str(row["nombre"]).upper()
        poblacion_urbana = int(row["poblaciónUrbana"])
        poblacion_rural = int(row["poblaciónRural"])
        departamento = str(row["departamento"]).upper()
        es_capital = int(row["esCapital"]) == 1
        m = Municipio(codigo=codigo, nombre=nombre, poblacion_rural=poblacion_rural,
                      poblacion_urbana=poblacion_urbana, departamento=departamento,
                      es_capital=es_capital)
        pila.añadir(m)
    return pila


# -----------------------------------------------------------------------------------------

from enum import StrEnum, auto

class Operacion(StrEnum):
    SUMA = '+'
    RESTA = '-'
    MULTIPLICACION = '*'
    DIVISION = '/'
    MODULO = '%'
    POTENCIA = '^'
    ERROR = auto()

@dataclass(frozen=True)
class Termino:
    """
    Un término es un componente de una expresión
    aritmética. Hay dos tipos de términos: valores
    numéricos y operaciones.
    """
    __es_numero : bool
    __valor_numerico : int
    __operacion : Operacion

    @property
    def es_numero(self) -> bool:
        return self.__es_numero

    @property
    def es_operacion(self) -> bool:
        return not self.__es_numero

    def dar_valor_numerico(self) -> int | None:
        if self.__es_numero:
            return int(self.__valor_numerico)
        return None

    def dar_operacion(self) -> Operacion | None:
        if self.__es_numero:
            return None
        return self.__operacion

    @classmethod
    def crear_termino(cls, expresion: str) -> 'Termino':
        t = expresion
        op = Operacion.ERROR
        vn = 0
        if t == '+':
            op = Operacion.SUMA
        elif t == '-':
            op = Operacion.RESTA
        elif t == '*':
            op = Operacion.MULTIPLICACION
        elif t == '/':
            op = Operacion.DIVISION
        elif t == '^':
            op = Operacion.POTENCIA
        elif t == '%':
            op = Operacion.MODULO
        else:
            vn = int(t)
        return Termino(op == Operacion.ERROR, vn, op)

    def __str__(self):
        if self.__es_numero:
            return f"NUM({self.__valor_numerico})"
        return f"OP({self.__operacion})"



# -----------------------------------------------------------------------------------------

def agregar_termino_al_final(cabeza: Nodito[Termino], t: Termino) -> Nodito[Termino]:
    nodo = Nodito[Termino](t)
    if cabeza.es_nulo:
        cabeza = nodo
    else:
        act = cabeza
        while act.sig.no_es_nulo:
            act = act.sig
        act.sig = nodo
    return cabeza

# -----------------------------------------------------------------------------------------

from io import StringIO
import shlex

def obtener_terminos(expresion: str) -> Nodito[Termino]:
    """
    Esta función toma una expresión y obtiene los
    diferentes tokens que hacen parte de ella
    """
    inp = StringIO(expresion)
    cabeza = nulo
    for elem in list(shlex.shlex(inp)):
        term = Termino.crear_termino(elem)
        cabeza = agregar_termino_al_final(cabeza, term)
    return cabeza

def dividir_expresion(expresion: str) -> Nodito[str]:
    """"
    Esta función divide la expresión en los diferentes
    componentes que hacen parte de ella
    """
    cabeza = nulo
    actual = nulo
    inp = StringIO(expresion)
    for elem in list(shlex.shlex(inp)):
        if cabeza is nulo:
            cabeza = Nodito[str](elem)
            actual = cabeza
        else:
            actual.sig = Nodito[str](elem)
            actual = actual.sig
    return cabeza

# Función externa que agrega una palabra al final de una lista
def agregar_palabra_lista_noditos(cabeza : Nodito[str] | Nulo, palabra : str) -> Nodito[str] | Nulo:
    nodo = Nodito[str](palabra)
    if cabeza.es_nulo:
        cabeza = nodo
    else:
        act = cabeza
        while act.sig.no_es_nulo:
            act = act.sig
        act.sig = nodo
    return cabeza

def crear_lista_nodos_palabras(*palabras : str) -> Nodito[str] | Nulo:
    cabeza = nulo
    for palabra in palabras:
        cabeza = agregar_palabra_lista_noditos(cabeza, palabra)
    return cabeza

def crear_lista_nodos_numeros(*numeros : int) -> Nodito[int] | Nulo:
    cabeza = nulo
    act = cabeza
    for numero in numeros:
        nodo = Nodito[int](numero)
        if cabeza.es_nulo:
            cabeza = nodo
            act = nodo
        else:
            act.sig = nodo
            act = act.sig
    return cabeza

# ----------------------------------------------------------------------------------------
# Un pair es una pareja de valores en Python
# ----------------------------------------------------------------------------------------
@dataclass
class Pair[P, T]:
    first : P
    second : T

    def __getitem__(self, key: int) -> P | T:
        if key == 0:
            return self.first
        elif key == 1:
            return self.second
        else:
            raise IndexError(f"El índice {key} no existe en el pair")

    def __setitem__(self, key: int, value: P | T) -> None:
        if key == 0:
            self.first = value
        elif key == 1:
            self.second = value
        else:
            raise IndexError(f"El índice {key} no existe en el pair")

    def __len__(self) -> int:
        return 2

    def __repr__(self) -> str:
        return f"Pair({self.first}, {self.second})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Pair):
            return self.first == other.first and self.second == other.second
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __contains__(self, item: P | T) -> bool:
        return item in (self.first, self.second)

    def __hash__(self) -> int:
        return hash((self.first, self.second))

    def __getattr__(self, name: str) -> P | T:
        if name == "primero" or name == "suma" or name == "tamaño":
            return self.first
        elif name == "segundo" or name == "contador":
            return self.second
        else:
            raise AttributeError(f"El atributo {name} no existe en el pair")

    def __setattr__(self, name: str, value: P | T) -> None:
        if name == "first" or name == "primero" or name == "suma" or name == "tamaño":
            super().__setattr__("first", value)
        elif name == "second" or name == "segundo" or name == "contador":
            super().__setattr__("second", value)
        else:
            raise AttributeError(f"El atributo {name} no existe en el pair")

# ----------------------------------------------------------------------------------------
# Un vector es una estructura de datos lineal, parecida a un arreglo, pero con
# la capacidad de eliminar y agregar en posiciones específicas de la estructura
# de datos
# ----------------------------------------------------------------------------------------

if __name__ == '__main__':
    print("Hola mundo")
    p = Pair[int, str](10, "Hola")
    print(p.suma)
    print(p.contador)
    p.suma += 1
    p.contador = "diana"
    print(p)
    p.primero = 20
    print(p.first)