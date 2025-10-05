import random
from datetime import datetime

partidas = {}

def iniciar_partida(jugador, tablero):
    posicion = 1
    lanzamientos = 0
    kraken_count = 0
    max_pos = 1
    perder_turno = False

    print(f"Comienza la partida de {jugador[0]}\n")

    while posicion < 30:
        if perder_turno:
            print("Pierdes este turno por un cañonazo.\n")
            perder_turno = False
            continue

        input("Presiona ENTER para lanzar el dado...")
        tirada = dado()
        lanzamientos += 1
        posicion += tirada

        if posicion > 30:
            posicion = 30

        if 5 <= posicion <= 10:
            print("¡Caíste en una trampa de arena! Retrocedes 2 casillas\n")
            posicion -= 2
        elif 11 <= posicion <= 18:
            print("¡Un cañonazo! Perderás el siguiente turno.\n")
            perder_turno = True
        elif 19 <= posicion <= 24:
            print("¡Encontraste un cofre de oro! Avanzas 4 casillas extra\n")
            posicion += 4
            if posicion > 30:
                posicion = 30
        elif 25 <= posicion <= 29:
            kraken_count += 1
            print_calavera()
            if tirada % 2 == 1:
                print("¡El Kraken te derrotó! Partida perdida.\n")
                resultado = "Derrota"
                break
            else:
                print("¡El Kraken te envió de vuelta al inicio!\n")
                posicion = 1

        if posicion > max_pos:
            max_pos = posicion

        print(f"Estás en la casilla {posicion}.\n")
    else:
        print(f"¡Felicidades {jugador[0]}! , llegaste al tesoro\n")
        print_barco()
        resultado = "Victoria"

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    partidas[fecha] = {
        "jugador": jugador[0],
        "edad": jugador[1],
        "lanzamientos": lanzamientos,
        "resultado": resultado,
        "max_pos": max_pos,
        "kraken_count": kraken_count
    }

def mostrar_instrucciones():
    print_pirata()
    print("""
BIENVENIDO AL JUEGO DEL TESORO PIRATA!!!
El objetivo es llegar al casillero 30 para ganar el tesoro.
Pero cuidado, habrán obstáculos en el camino.

Obstáculos y Eventos:
""")
    print(f"{'Obstáculo/Evento':<18}{'Rango de Casilleros':<22}{'Efecto'}")
    print("-" * 70)
    print(f"{'Trampa de Arena':<18}{'5 - 10':<22}{'Retrocede 2 casilleros.'}")
    print(f"{'Cañonazo':<18}{'11 - 18':<22}{'Pierde un turno.'}")
    print(f"{'Cofre de Oro':<18}{'19 - 24':<22}{'Avanza 4 casilleros extra.'}")
    print(f"{'Kraken':<18}{'25 - 29':<22}{'Dado impar = pierde / Dado par = inicio.'}\n")

def registrar_jugador():
    while True:
        nombre = input("Ingrese su nombre: ")
        if len(nombre) > 16:
            print("El nombre no puede tener más de 16 caracteres")
            continue
        while True:
            try:
                edad = int(input("Ingrese su edad: "))
                if edad < 0:
                    print("La edad no puede ser negativa")
                    continue
                break
            except ValueError:
                print("Edad inválida, debe ser un número entero")

        return nombre, edad

def dado():
    val = random.randint(1,6)
    print(f"Sacaste un... : {val}!")
    return val

def generar_tablero():
    tab = ["Casilla segura"] * 31
    for i in range(31):
        if 5 <= i <= 10:
            tab[i] = "Trampa de Arena"
        elif 11 <= i <= 18:
            tab[i] = "Cañonazo"
        elif 19 <= i <= 24:
            tab[i] = "Cofre de Oro"
        elif 25 <= i <= 29:
            tab[i] = "Kraken"
        elif i == 30:
            tab[i] = "Tesoro"
    return tab

def ver_estad():
    if len(partidas) == 0:
        print("No hay partidas registradas aún\n")
        return

    total = 0
    vict = 0
    der = 0
    prom = 0
    max_pos = 0
    total_kraken = 0

    for p in partidas:
        partida = partidas[p]
        total += 1
        if partida["resultado"] == "Victoria":
            vict += 1
        else:
            der += 1
        prom += partida["lanzamientos"]
        if partida["max_pos"] > max_pos:
            max_pos = partida["max_pos"]
        total_kraken += partida["kraken_count"]

    prom = prom / total

    print("Estadísticas generales:")
    print(f"Total de partidas: {total}")
    print(f"Victorias: {vict}")
    print(f"Derrotas: {der}")
    print(f"Promedio de lanzamientos: {prom}")
    print(f"Mayor número de casillas avanzadas en una partida: {max_pos}")
    print(f"Cantidad total de veces que salió el Kraken: {total_kraken}\n")

def ver_estad_jug():
    if len(partidas) == 0:
        print("No hay partidas registradas aún\n")
        return

    jugador_nom = input("Ingrese el nombre del jugador: ")
    print(f"\nEstadísticas de {jugador_nom}:")

    for p in partidas:
        partida = partidas[p]
        if partida["jugador"] == jugador_nom:
            print(f"Fecha y hora: {p}")
            print(f"Lanzamientos: {partida['lanzamientos']}")
            print(f"Resultado: {partida['resultado']}")
            print(f"Máxima casilla alcanzada: {partida['max_pos']}")
            print(f"Veces que apareció Kraken: {partida['kraken_count']}\n")

def print_pirata():
    print(r"""                                                                                
 -#+.                                      +#.   
.#+##-.              ....               .##.##.  
.+-#. -+.        -##########-.        .#######   
 .#+++  .+.   .################.    -########.   
.  .#.#+  .#.-##################- -#####+##.     
     .###+. -#########################+++.       
       .--#+##########################+          
         .+#########################-            
           .######################+              
           .+ +#######   ...#... +.              
            -+ +#####      .#.  ##+              
            .#+       #+    -  +##+.             
   -#############    .##.    +####-############+.
   -#-.#++#-##-## -#+    -#+.++##+.         .- +.
   -+#.+#.+######+.+- .+ .#.++  ##---------..-+. 
   .....---######---..-#. #.+##-  -+.--......    
       -+########- .----.-. .#+.#- .++#.         
      -###-###+. -+        -+  .#+#+##-#.        
   .+#######++     .+####+.     .#+###+###.      
 .+#######+ ..                   -..+######+-    
  -++###-.                           .+##-++.    
    +#.                    .           .+#.      
""")

def print_calavera():
    print(r"""
     ______
  .-        -.
 /            \
|,  .-.  .-.  ,|
| )(_o/  \o_)( |
|/     /\     \|
(_     ^^     _)
 \__|IIIIII|__/
  | \IIIIII/ |
  \          /
   `--------`
""")

def print_barco():
    print(r"""
          
+++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++
++++++++++++%**#+++++++++++++++@@@#*+++++++++
++++++++++##+++++%*++++++++++++@%#%#+++++++++
++++++++++%+++++++#*++++++*#*#%@@%%#+++++++++
++++++++++++++++++++++++++%+++++++#*+++++++++
++++++++++++++++++++++++++%#####*+#+**+++++++
++++++++++++++++++++++++**++*#%%@@@%%++++++++
++++++++++++++++++++++++%++*@@@#++*%#++++++++
+++++++++++++++++++++++*#++*%@%*++#+#++++++++
++++++++++++++++++++++++%++*%@%*++#+#++++++++
++++++++++++++++++++*@#+#%%%%#*+++#%%#*++++++
++++++*######*++++++++@@@@%*+%++*%@%*#*++++++
+++++##*#+++++@+++++++@@@%%@@@@@@@@@@@%++++++
+++++#%%@#%%@#@+++++++*@@@#@@%@@@@@@@#+++++++
+++**%##%*****@*++++*###%%@@@@@@@@@@@*+++**++
+++++++++++++++++++++++++++++++++++++++++++++
++*@%#**+++***#%@@%%**++++**#%@@%%#***#%@@*++
++++++*######*+++++*######*++++++**##*+++++++
+++*+++++++++++***+++++++++++***++++++++**+++
+++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++
        
          """)


def menu():
    jugador = None
    tablero = None

    while True:
        print("--- MENÚ DEL JUEGO ---")
        print("1. Ver instrucciones")
        print("2. Registrar jugador")
        print("3. Registrar nuevo juego")
        print("4. Iniciar juego")
        print("5. Mostrar estadísticas generales")
        print("6. Mostrar estadísticas por jugador")
        print("7. Salir\n")

        opcion = int(input("Elige una opción: "))
        print()

        if opcion == 1:
            mostrar_instrucciones()
        elif opcion == 2:
            jugador = registrar_jugador()
            print()
        elif opcion == 3:
            tablero = generar_tablero()
            print("Tablero generado con éxito!\n")
        elif opcion == 4:
            if jugador and tablero:
                iniciar_partida(jugador, tablero)
            else:
                print("Primero registra un jugador y genera un tablero\n")
        elif opcion == 5:
            ver_estad()
        elif opcion == 6:
            ver_estad_jug()
        elif opcion == 7:
            print("Gracias por jugar a El Tesoro Pirata ¡Hasta la próxima!")
            break

menu()
