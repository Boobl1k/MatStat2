import math
from scipy.stats import chi2
import statistics
from matplotlib import pyplot
from pandas import *
from table import createtable

numbers = read_csv('telecom_churn.csv')['Total day calls'].tolist()

count = len(numbers)

print('Минимальное значение - ', min(numbers))
print('Максимальное значение - ', max(numbers))
print('Количество данных - ', len(numbers))
intervalCount = math.floor(1 + 3.322 * math.log10(count))
print('Количсетво интервалов - ', intervalCount)
intervalLength = math.ceil((max(numbers) - min(numbers)) / math.floor(intervalCount))
print('Длина интервала - ', intervalLength)

ni = [[0 for x in range(2)] for y in range(intervalCount)]
currentLeft = min(numbers)
for i in range(intervalCount):
    ni[i][0] = currentLeft
    ni[i][1] = currentLeft + intervalLength
    currentLeft += intervalLength
print('Интервалы:')
for pair in ni:
    print(pair)

countList = []
for i in range(intervalCount):
    x = 0
    for number in numbers:
        if ni[i][1] >= number > ni[i][0]:
            x += 1
    countList.append(x)
print('Сколько попало в интервал:')
print(countList)

middles = [0.0 for y in range(0, intervalCount)]
for i in range(len(middles)):
    middles[i] = (ni[i][0] + ni[i][1]) / 2
print('Середины интервалов:')
print(middles)

xMiddle = 0
for i in range(0, intervalCount):
    xMiddle += (middles[i] * countList[i])
xMiddle = xMiddle / count
print('Выборочная средняя - ', xMiddle)

z2 = [0.0 for y in range(0, intervalCount)]
for i in range(0, intervalCount):
    zmid = (middles[i] - xMiddle) ** 2
    z2[i] = zmid

print(z2)

sigma = 0.0
for i in range(0, intervalCount):
    sigma = sigma + z2[i] * countList[i]
sigma = sigma / count
print('Выборочная дисперсия - ', sigma)

t = createtable()

y = 0
if count <= 20:
    y = count
elif 20 < count <= 50:
    if count % 10 == 0:
        y = count
    elif count % 5 == 0:
        y = count
    else:
        y = count - (count % 5)
elif 50 < count <= 100:
    if count % 10 == 0:
        y = count
    else:
        y = count - (count % 10)
elif 120 >= count > 100:
    y = 120
else:
    y = 0
number = 0
for i in range(0, 29):
    if y == t[i][0]:
        number = i
gammaChoise = int(input('Выберите гамму из списка (1-3)\n1 - 0.95\n2 - 0,99\n3 - 0.999\n')) - 1
gamma = 0.0
if gammaChoise == 1:
    gamma = 0.95
elif gammaChoise == 2:
    gamma = 0.99
else:
    gamma = 0.999

xIntervalMin = xMiddle - (t[number][gammaChoise] * math.sqrt(sigma)) / math.sqrt(count)
xIntervalMax = xMiddle + (t[number][gammaChoise] * math.sqrt(sigma)) / math.sqrt(count)

print(xIntervalMin, '< x <', xIntervalMax)

d = [0 for i in range(intervalCount)]
for i in range(intervalCount):
    d[i] = middles[i] - xMiddle

a = 0

for i in range(intervalCount):
    a += (d[i] * d[i] * d[i] * countList[i] / count)
a /= math.sqrt(sigma) ** 3

df = count - 1
alfa1 = (1 - gamma) / 2
alfa2 = (1 + gamma) / 2
p1 = 1 - alfa1
p2 = 1 - alfa2

intervalSigma1 = (df * sigma) / chi2.ppf(p1, df)
intervalSigma2 = (df * sigma) / chi2.ppf(p2, df)

print(intervalSigma1, ' < сигма < ', intervalSigma2)

median = statistics.median(numbers)
mode = statistics.mode(numbers)
print('Медиана - ', median)
print('Мода - ', mode)

pyplot.hist(numbers, edgecolor='black', bins=intervalCount)
pyplot.title('Гистограмма с ' + str(count) + ' элементами')
pyplot.xlabel('значения')
pyplot.ylabel('частоты')
pyplot.show()

z4 = []
for zi in z2:
    z4.append(zi ** 2)

m4 = 0
for i in range(intervalCount):
    m4 += z4[i] * countList[i]

m4 = m4 / count

ek = m4 / (sigma ** 2) - 3

print('Ek - ', ek)

z3 = []
for i in z2:
    z3.append(i ** 1.5)

m3 = 0
for i in range(0, intervalCount):
    m3 += z3[i] * countList[i]
m3 /= count
a3 = m3 / (sigma ** 1.5)

print('A3 - ', a3)
