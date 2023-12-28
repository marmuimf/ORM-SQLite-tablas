#Crear una nueva propiedad para el objeto, q debe contener una colección de objetos o algo diferente a un simple dato escalar. 
#Mostrar cómo has logrado persistir esa info o estructura de datos en SQL, probablemente creando tablas relacionadas.

#ORM OBJECT RELATIONAL MAPPING
#prog basado en objetos
#y guardar su info en un json
#una de las propiedades de "persona" es una coleccion de propiedades de otros elementos (array)

#guardar un inventario de objetos donde los obj son recogibles
#en el min 24 desereda y borra clase entidad
#guardar de forma relacional la info en objetos

#https://youtu.be/gELQzF-Z2YQ

import tkinter as tk
import random 
import math
import json
import sqlite3


# Declaración de variables globales
personas = []
numeropersonas = 5

class Recogible():
    def __init__(self):
        self.posx = random.randint(0,700)#cada vez que ejecute, el personaje saldra por un lado diferente
        self.posy = random.randint(0,700)
        self.color = random.choice(["pink", "violet", "purple"])
    def serializar(self):
        recogible_serializado = {
            "posx":self.posx,
            "posy":self.posy,
            "color":self.color
            }
        return recogible_serializado
    
class Recogible2():
    def __init__(self):
        self.radio = 30
        self.direccion = random.randint(0,360)
    def serializar(self):
        recogible2_serializado = {
            "radio":self.radio,
            "direccion":self.direccion
            }
        
        return recogible2_serializado

class Persona():
    def __init__(self):
        #propiedades de persona
        self.posx = random.randint(0,700)
        self.posy = random.randint(0,700)
        self.color = random.choice(["pink", "violet", "purple"])
        self.radio = 30
        self.direccion = random.randint(0,360)#propiedad de direccion
        
        self.entidad = ""
        self.energia = 100
        self.descanso = 100
        self.entidadenergia = ""
        self.entidaddescanso = ""
        self.inventario = [] #es una lista
        self.inventario2 = [] 
        
        
        #cada "persona" tendra 5 elementos en el inventario
        for i in range(0,5):
            self.inventario.append(Recogible())

        for i in range(0,5):
            self.inventario2.append(Recogible2())
    
    def dibuja(self): #metodo
        self.entidad = lienzo.create_oval(
            self.posx-self.radio/2,
            self.posy-self.radio/2,
            self.posx+self.radio/2,
            self.posy+self.radio/2,
            fill=self.color)
        self.entidadenergia = lienzo.create_rectangle(
            self.posx-self.radio/2,
            self.posy-self.radio/2-14,#2-10
            self.posx+self.radio/2,
            self.posy-self.radio/2-8,
            fill="green"
            )
        self.entidaddescanso = lienzo.create_rectangle(
            self.posx-self.radio/2,
            self.posy-self.radio/2-22,
            self.posx+self.radio/2,
            self.posy-self.radio/2-16, #2-14
            fill="blue"
            )
    def mueve(self):
        if self.energia > 0:
            self.energia -= 0.1
        if self.descanso > 0:
            self.descanso -= 0.1
        self.colisiona() #llamo a colisiona
        lienzo.move(
            self.entidad, #muevo entidad pixeles
            math.cos(self.direccion),
            math.sin(self.direccion))
        
        #coordenadas de las barras
        anchuradescanso = (self.descanso/100)*self.radio
        lienzo.coords(
            self.entidaddescanso,
            self.posx - self.radio/2,
            self.posy - self.radio/2 - 22,
            self.posx - self.radio/2 + anchuradescanso,
            self.posy - self.radio/2 - 16
        )
        anchuraenergia = (self.energia/100)*self.radio
        lienzo.coords(
            self.entidadenergia,
            self.posx - self.radio/2,
            self.posy - self.radio/2 - 14,
            self.posx - self.radio/2 + anchuraenergia,
            self.posy - self.radio/2 - 8
        )
        #actualizo posiciones
        self.posx += math.cos(self.direccion)
        self.posy += math.sin(self.direccion)

    def colisiona(self):#para que reboten
        if self.posx < 0 or self.posx > 700 or self.posy < 0 or self.posy > 700:
            self.direccion += math.pi
    
    #la clase se serializa a si misma
    def serializar(self):
        persona_serializada = {
            "posx":self.posx,
            "posy":self.posy,
            "radio":self.radio,
            "direccion":self.direccion,
            "color":self.color,
            "energia":self.energia,
            "descanso":self.descanso,
            "inventario":[item.serializar() for item in self.inventario]
            # "inventariocolor":[item.serializar() for item in self.inventariocolor]
            }
        return persona_serializada
            
def guardarPersonas():
    try:
        # Guardo los personajes en JSON
        print("guardo a los jugadores en json")
        print("------------------------------")
        personas_serializadas = [persona.serializar() for persona in personas]
        with open("jugadores.json", "w") as archivo:
            json.dump(personas_serializadas, archivo, indent=4)

        # Guardo los personajes en SQL
        with sqlite3.connect("jugadores.sqlite3") as conexion:
            cursor = conexion.cursor()

            # RECOGIBLES
            delete_recogibles_query = 'DELETE FROM recogibles'
            cursor.execute(delete_recogibles_query)
            print("Query para vaciar recogibles:", delete_recogibles_query)

            # JUGADORES
            delete_jugadores_query = 'DELETE FROM jugadores'
            cursor.execute(delete_jugadores_query)
            print("Query para vaciar jugadores:", delete_jugadores_query)

            for persona in personas:
                cursor.execute('''
                    INSERT INTO jugadores
                    VALUES (
                        NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                ''', (
                    persona.posx, persona.posy, persona.radio, persona.direccion,
                    persona.color, persona.entidad, persona.energia, persona.descanso,
                    persona.entidadenergia, persona.entidaddescanso
                ))

                # Obtener el id del jugador recién insertado
                persona.entidad = cursor.lastrowid

                # GUARDAR EN LA TABLA DE RECOGIBLES
                for recogible in persona.inventario:
                    cursor.execute('''
                        INSERT INTO recogibles VALUES (
                            NULL, ?, ?, ?, ?
                        )
                    ''', (
                        persona.entidad, recogible.posx, recogible.posy, recogible.color
                    ))

                for recogible2 in persona.inventario2:
                    cursor.execute('''
                        INSERT INTO recogible2 VALUES (
                            NULL, ?, ?, ?
                        )
                    ''', (
                        persona.entidad, recogible2.radio, recogible2.direccion
                    ))

            conexion.commit()

    except sqlite3.Error as error:
        print("Error:", error)


    
# Creo una ventana
raiz = tk.Tk()

#En la ventana creo un lienzo
lienzo = tk.Canvas(raiz,width=700,height=700)
lienzo.pack()

#Boton de guardar
boton = tk.Button(raiz,text="Guarda",command=guardarPersonas)
boton.pack()

# cargar/leer datos desde SQL
try:
    conexion = sqlite3.connect("jugadores.sqlite3")
    cursor = conexion.cursor()

    cursor.execute('''
            SELECT *
            FROM jugadores
            
            ''')
    while True:
        fila = cursor.fetchone()
        if fila is None:
            break
        #print(fila)
        persona = Persona()
        persona.posx = fila[1] #array de personajes
        persona.posy = fila[2]
        persona.radio = fila[3]
        persona.direccion = fila[4]
        persona.color = fila[5]
        persona.entidad = fila[6]
        persona.energia = fila[7]
        persona.descanso = fila[8]
        persona.entidadenergia = fila[9]
        persona.entidaddescanso = fila[10]
        
        cursor3 = conexion.cursor()
        nuevapeticion = '''
            SELECT *
            FROM recogibles
            WHERE persona = '''+persona.entidad+'''
            '''
        #print(nuevapeticion)
        cursor3.execute(nuevapeticion)
        while True:
            fila2 = cursor.fetchone()
            if fila2 is None:
                break
            nuevorecogible = Recogible()
            nuevorecogible.posx = fila2[2]
            nuevorecogible.posy = fila2[3]
            nuevorecogible.color = fila2[4]
            persona.inventario.append(nuevorecogible)
            #pass
           
        personas.append(persona)
    conexion.close()
    #print(personas)
except sqlite3.Error as error:
    print("error al leer base de datos",error)

#En la colección introduzco instancias de personas en el caso de que no existan
#print(len(personas))
if len(personas) == 0: #si no hay personas
    numeropersonas = 10 #crea 5
    for i in range(0,numeropersonas): #desde 0 hasta nr perosnas
        personas.append(Persona())

# Pinto cada una de las personas en la colección
for persona in personas:
    persona.dibuja()
    
# Creo un bucle repetitivo
def bucle():
    # muevo cada persona en la colección
    for persona in personas:
        persona.mueve()
    raiz.after(10,bucle)#cada 10 milisegundos ejecuto bucle
    
#Ejecuto el bucle
bucle()

raiz.mainloop()