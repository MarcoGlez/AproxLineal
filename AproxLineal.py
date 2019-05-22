import matplotlib.pyplot as plt
%matplotlib inline
from matplotlib.ticker import MaxNLocator
import scipy.integrate as integrate


# Anexa todos los datos de lista anexables a listaOG"
def anexarLista(listaOG, anexables):
    for k in range(0, len(anexables), 1):
        listaOG.append(anexables[k])


# Regresa una lista nueva con los valores de una lista de tuplas multiplicados por la escala"
def escalarLista(lista, escala):
    nuevaLista = []
    for k in range(0, len(lista), 1):
        x, y = lista[k]
        x *= escala
        y *= escala
        nuevaLista.append((x, y))
    return nuevaLista


# Regresa una nueva lista de dos dimensiones con coordenadas X en la posicion 0 y coordenadas Y en posicion 1
def separarXY(lista):
    listaX = []
    listaY = []
    for k in range(0, len(lista), 1):
        x, y = lista[k]
        listaX.append(x)
        listaY.append(y)
    return listaX, listaY


# Regresa un callable (funcion lineal) a partir de dos puntos dados (tipo de dato: tupla)
def obtenerFuncion(punto1, punto2):
    x1, y1 = punto1
    x2, y2 = punto2
    m = (y2 - y1) / (x2 - x1)
    return lambda x: m * (x - x1) + y1


# Calcula el area bajo una region, requiere una lista de coordenadas (en tuplas) y regresa un float
def calcularArea(lista):
    areaTotal = 0.0
    for k in range(0, len(lista) - 1, 1):
        fx = obtenerFuncion(lista[k], lista[k + 1])
        limI, dontCare = lista[k]
        limS, dontCare1 = lista[k + 1]
        areaSegmento, dontCare2 = integrate.quad(fx, limI, limS)
        areaTotal += areaSegmento
    return areaTotal


"Lista de Puntos Superiores (En metros)"
n = 18
s1 = n  # Salida 1
pSuperior = [(462940.8, 2134324.6), (465606.7, 2139876.1), (470533.4, 2145293.5),
             (473727.8, 2147406.3), (476789.2, 2150843.2), (477324, 2156403.5),
             (479054.4, 2157594), (482517.3, 2161964.3), (487181.6, 2167400.2),
             (488907, 2162357.5), (492493.8, 2156524.8), (494749, 2150830.3),
             (494875.6, 2145273), (499927.9, 2142096.5), (501389.8, 2140111.9),
             (503647, 2134424.7), (503775.3, 2128871.3), (505409.3, 2125437.8)]

"Lista de Puntos Inferiores (En metros)"
m = 17
s2 = m  # Salida 2
pInferior = [(462940.8, 2134324.7), (464312.4, 2128797.3), (468192.7, 2123163.4),
             (468295.4, 2121909.5), (469863.9, 2117832.5), (473638.3, 2113333.3),
             (475422.1, 2111129.2), (478888.1, 2111129.2), (484247.3, 2110804.8),
             (489394.4, 2108703.7), (493597.5, 2106603.5), (494862.4, 2108377.4),
             (499917.6, 2109933.5), (504130.6, 2112014.2), (504455.9, 2117553.8),
             (503519.5, 2123200.4), (505409.3, 2125437.8)]

"Lista Total de Puntos"
pTotal = []
anexarLista(pTotal, pSuperior)
anexarLista(pTotal, pInferior)

"Listas de puntos escalados"
escala = 0.001
pSupEsc = escalarLista(pSuperior, escala)
pInfEsc = escalarLista(pInferior, escala)
pTotalEsc = escalarLista(pTotal, escala)

"Max y Mín de puntos superiores"
xSupMin, ySupMin = min(pSupEsc)
xSupMax, ySupMax = max(pSupEsc)
"Max y Min de puntos inferiores"
xInfMin, yInfMin = min(pInfEsc)
xInfMax, yInfMax = max(pInfEsc)
"Max y Min de total de puntos"
xMax, yMax = max(pTotalEsc)
xMin, yMin = min(pTotalEsc)

"Coordenadas al origen"
x0 = min(xInfMin, xSupMin)
y0 = min(xInfMax, xSupMax)


"Graficas de puntos utilizados"
fig1 = plt.figure(1, figsize=(8, 8))

# Salida 3, total de puntos graficados
pXTotal, pYTotal = separarXY(pTotalEsc)
s3 = fig1.add_subplot(111)
s3.plot(pXTotal, pYTotal, "ko", markeredgecolor="w")
s3.xaxis.set_major_locator(MaxNLocator(integer=True))
s3.yaxis.set_major_locator(MaxNLocator(integer=True))
plt.show()
# Salida 4, linea de puntos superiores graficados
# Salida 5, linea de puntos inferiores graficados
pXSup, pYSup = separarXY(pSupEsc)
pXInf, pYInf = separarXY(pInfEsc)
fig_2, chart = plt.subplots(1, 2, figsize=(14, 7))
chart[0].plot(pXSup, pYSup, color="r")
chart[1].plot(pXInf, pYInf, color="b")
plt.show()
# Salida 6, linea de contorno de total de puntos graficados
plt.plot(pXSup, pYSup, "r", pXInf, pYInf, "b")
plt.show()

"Calculo de areas del area total y de regiones"
areaBloqueSup = (xSupMax * ySupMin) - (xSupMin * ySupMin)
areaSuperior = calcularArea(pSupEsc)
areaRegionSup = areaSuperior - areaBloqueSup  # Salida 7, area de la región superior

areaBloqueInf = (xInfMax * yInfMax) - (xInfMin * yInfMax)
areaInferior = calcularArea(pInfEsc)
areaRegionInf = areaBloqueInf - areaInferior  # Salida 8, area de la región inferior

areaAproximada = areaSuperior - areaInferior  # Salida 9, valor aproximado del área total
areaReal = 1485.0  # Salida 10, valor real del área total
ERP = abs(100 * (areaReal - areaAproximada) / areaReal)  # Salida 11, valor del error relativo porcentual del cálculo

print("""
Valor aproximado del area de la CDMX = %.2f
Valor real del área de la CDMX = %.2f
Error Relativo Porcentual = %.2f"""
      % (areaAproximada, areaReal, ERP))
