import numpy as np
import matplotlib.pyplot as plt
import pandas


def percentage(percent, whole):  # считаем % от общего
    return (percent / whole) * 100.0


def makePercentageList(beginningList):  # Создаём лист процентов из листа значений
    newList = []
    sumOfAList = sum(beginningList)
    for i in range(len(beginningList)):
        newList.append(round(percentage(beginningList[i], sumOfAList), 2))
    return newList


def showPieGraph(listToShow, nameList, title):  # Отрисовываем круговой граф
    fig1, ax1 = plt.subplots()
    plt.title(title)
    ax1.pie(listToShow, labels=nameList, autopct='%.1f', radius=0.8, pctdistance=0.7)
    centre_circle = plt.Circle((0, 0), 0.65, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    ax1.axis('equal')
    plt.tight_layout()
    plt.show()


def showGraph(xAxis, yAxis, xTitle, yTitle, title='График', width=0.8):  # Отрисовываем гистограмму
    plt.figure(figsize=(10.5, 6))
    plt.title(title)
    plt.xlabel(xTitle)
    plt.ylabel(yTitle)
    plt.bar(xAxis, yAxis, width=width)
    plt.show()


region = pandas.read_excel(r'Dataset.xlsx', skiprows=5)  # Читаем датасет
region.replace([np.NAN, ' '], 0, inplace=True)  # Немного нормализуем
districts = region[['район' in name for name in list(region['Name'])]]  # Отдельный фрейм для районов
region = region[['сельсовет' not in name and 'район' not in name for name in list(region['Name'])]]
# Фрейм без муниципальных укрупнений
districts['Name'] = districts['Name'].apply(lambda x: x.split(' район')[0])  # Слегка обрезаем имена для районов
populationPercents = makePercentageList(list(districts['Population']))   # Процент населения
shopsPercent = makePercentageList(list(districts['ShopsAll']))  # Процент магазинов
coefficient = [i / j for i, j in zip(populationPercents, shopsPercent)]  # Высчитываем коэффициент
condition = (region['Delivery'] == 0) & (region['ShopsGoods'] == 0) & (region['BoutiqueGoods'] == 0)
# Общее условие отсутсвия продуктовых торговых точек
needsDelivery = region[condition & (region['Population'] <= 100) & (region['Population'] > 0)]
needsBoutique = region[condition & (region['Population'] > 100) & (region['Population'] < 500)]
needsShop = region[condition & (region['Population'] > 500)]
boutiqueDensityByDistricts = districts['BoutiqueAll'] / districts['Population']  # Небольшое исследование плотности


showPieGraph(districts['Population'], districts['Name'], 'Процент населения по районам от общего')
showPieGraph(districts['BoutiqueAll'], districts['Name'], 'Процент киосков по районам от общего')
showPieGraph(districts['ShopsAll'], districts['Name'], 'Процент магазинов по районам от общего')
showGraph(districts['Name'].apply(lambda x: x[:3]), coefficient,
          'Районы', 'Отношение кол-ва населения к магазинам', title=f'Среднее: {round(np.mean(coefficient), 2)}')
showGraph(districts['Name'].apply(lambda x: x[:3]), districts['ShopsAll'], 'Районы', 'Магазины')
showGraph(districts['Name'].apply(lambda x: x[:3]), districts['BoutiqueAll'], 'Районы', 'Киоски')
showGraph(districts['Name'].apply(lambda x: x[:3]), boutiqueDensityByDistricts, 'Районы', 'Плотность',
          title=f'Среднее: {round(np.mean(boutiqueDensityByDistricts), 4)}')
showGraph([0, len(needsShop), len(needsBoutique), len(needsDelivery)],
          ['', 'В магазинах', 'В киосках', 'В приезжающих'], 'Количество нуждающихся поселков', 'Тип', width=15)

