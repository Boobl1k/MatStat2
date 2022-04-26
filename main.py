import math
from scipy.stats import chi2
import statistics
from matplotlib import pyplot
from pandas import *
from table import createtable

numbers = read_csv('telecom_churn.csv')['Total day calls'].tolist()

count = len(numbers)

print('Количество данных - ', len(numbers))
print('Минимальное значение - ', min(numbers))
print('Максимальное значение - ', max(numbers))
intervalCount = math.floor(1 + 3.322 * math.log10(count))
print('Количсетво интервалов - ', intervalCount)
intervalLength = math.ceil((max(numbers) - min(numbers)) / math.floor(intervalCount))
print('Длина интервала - ', intervalLength)

intervals = []
currentLeft = min(numbers)
for i in range(intervalCount):
    intervals.append([currentLeft, currentLeft + intervalLength])
    currentLeft += intervalLength
print('Интервалы:')
for pair in intervals:
    print(pair)

middles = []
for i in range(intervalCount):
    middles.append((intervals[i][0] + intervals[i][1]) / 2)
print('Середины интервалов:')
print(middles)

countList = []
for i in range(intervalCount):
    x = 0
    for number in numbers:
        if intervals[i][0] < number <= intervals[i][1]:
            x += 1
    countList.append(x)
print('Сколько попало в интервал:')
print(countList)

xMiddle = 0
for i in range(0, intervalCount):
    xMiddle += middles[i] * countList[i]
xMiddle /= count
print('Выборочная средняя - ', xMiddle)

z2 = []
for middle in middles:
    z2.append((middle - xMiddle) ** 2)

sigma = 0.0
for i in range(intervalCount):
    sigma += z2[i] * countList[i]
sigma /= count
print('Выборочная дисперсия - ', sigma)

y = 0
if count <= 20:
    y = count
elif count <= 50:
    y = count - (count % 5)
elif count <= 100:
    y = count - (count % 10)
elif count <= 120:
    y = 120
else:
    y = 0

number = 0
t = createtable()
for i in range(29):
    if y == t[i][0]:
        number = i
gammaChoice = int(input('Выберите гамму из списка (1-3)\n1 - 0.95\n2 - 0,99\n3 - 0.999\n')) - 1

gamma = 0.0
if gammaChoice == 1:
    gamma = 0.95
elif gammaChoice == 2:
    gamma = 0.99
else:
    gamma = 0.999

xIntervalMin = xMiddle - (t[number][gammaChoice] * math.sqrt(sigma)) / math.sqrt(count)
xIntervalMax = xMiddle + (t[number][gammaChoice] * math.sqrt(sigma)) / math.sqrt(count)

print(xIntervalMin, '< x <', xIntervalMax)

d = []
for i in range(intervalCount):
    d.append(middles[i] - xMiddle)

a = 0
for i in range(intervalCount):
    a += d[i] ** 3 * countList[i] / count
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
m4 /= count

ek = m4 / (sigma ** 2) - 3

print('Ek - ', ek)

z3 = []
for z2i in z2:
    z3.append(z2i ** 1.5)

m3 = 0
for i in range(intervalCount):
    m3 += z3[i] * countList[i]
m3 /= count
a3 = m3 / (sigma ** 1.5)

print('A3 - ', a3)
