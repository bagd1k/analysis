import matplotlib.pyplot as plt
import numpy as np
import pandas


def percentage(percent, whole):  # считаем % от общего
    return (percent / whole) * 100.0


def zipAndSort(keys, values):
    x = dict(zip(keys, values))
    return {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}


def makePercentageList(beginningList):  # Создаём лист процентов из листа значений
    sumOfAList = sum(beginningList)
    return list(map(lambda x: round(percentage(x, sumOfAList), 2), beginningList))


def showPieGraph(listToShow, nameList, title):  # Отрисовываем круговой граф
    fig1, ax1 = plt.subplots()
    dictionary = zipAndSort(nameList, listToShow)
    ax1.pie(dictionary.values(), labels=dictionary.keys(), autopct='%.1f', radius=0.8, pctdistance=0.7)
    centre_circle = plt.Circle((0, 0), 0.65, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    ax1.axis('equal')
    plt.tight_layout()
    plt.show()


def showGraph(xAxis, yAxis, xTitle, yTitle, title='График', width=0.8, size=28, height=15, showBarLabel=True,
              needsSort=True):
    # Отрисовываем диаграмму
    plt.figure(figsize=(size, height))
    plt.title(title)
    plt.xlabel(xTitle)
    plt.ylabel(yTitle)
    if needsSort:
        dictionary = zipAndSort(xAxis, yAxis)
        bar = plt.bar(dictionary.keys(), list(map(lambda x: round(x, 2) if type(x) != str else x, dictionary.values())),
                      width=width)
    else:
        bar = plt.bar(xAxis, yAxis, width=width)
    if showBarLabel:
        plt.bar_label(bar)
    plt.show()


region = pandas.read_excel(r'Dataset.xlsx', skiprows=5)  # Читаем датасет
region.replace([np.NAN, ' '], 0, inplace=True)  # Немного нормализуем
districts = region[['район' in name for name in list(region['Name'])]]  # Отдельный фрейм для районов
region = region[['сельсовет' not in name and 'район' not in name for name in list(region['Name'])]]
# Фрейм без муниципальных укрупнений
districts['Name'] = districts['Name'].apply(lambda x: x.split(' район')[0])  # Слегка обрезаем имена для районов
populationPercents = makePercentageList(list(districts['Population']))  # Процент населения
shopsPercent = makePercentageList(list(districts['ShopsAll']))  # Процент магазинов
boutiquesPercent = makePercentageList(list(districts['BoutiqueAll']))  # Процент киосков
coefficientShops = [i / j for i, j in zip(shopsPercent, populationPercents)]  # Высчитываем коэффициент для магазинов
coefficientBoutiques = [i / j for i, j in zip(boutiquesPercent, populationPercents)]  # И для киосков
condition = (region['Delivery'] == 0) & (region['ShopsGoods'] == 0) & (region['BoutiqueGoods'] == 0)
# Общее условие отсутсвия продуктовых торговых точек
needsDelivery = region[condition & (region['Population'] <= 100) & (region['Population'] > 0)]
needsBoutique = region[condition & (region['Population'] > 100) & (region['Population'] < 500)]
needsShop = region[condition & (region['Population'] > 500)]
boutiqueDensityByDistricts = districts['Population'] / districts['BoutiqueAll']  # Небольшое исследование плотности
shopDensityByDistricts = districts['Population'] / districts['ShopsAll']

showPieGraph(districts['Population'], districts['Name'],
             'Процент населения по районам от общего (без г. Липецка и Ельца)')
showPieGraph(districts['BoutiqueAll'], districts['Name'],
             'Процент киосков по районам от общего (без г. Липецка и Ельца)')
showPieGraph(districts['ShopsAll'], districts['Name'],
             'Процент магазинов по районам от общего (без г. Липецка и Ельца)')
showGraph(districts['Name'], coefficientShops,
          'Районы', 'Коэффициент процентного отношения магазинов к населению',
          title=f'Среднее: {round(np.mean(coefficientShops), 2)}')
showGraph(districts['Name'], coefficientBoutiques,
          'Районы', 'Коэффициент процентного отношения кисоков к населению',
          title=f'Среднее: {round(np.mean(coefficientBoutiques), 2)}')
showGraph(districts['Name'], boutiqueDensityByDistricts, 'Районы', 'Плотность киосков',
          title=f'Среднее: {round(np.mean(boutiqueDensityByDistricts))}')
showGraph(districts['Name'], shopDensityByDistricts, 'Районы', 'Плотность магазинов',
          title=f'Среднее: {round(np.mean(shopDensityByDistricts))}')
showGraph([0, len(needsShop), len(needsBoutique), len(needsDelivery)],
          ['', 'В магазинах', 'В киосках', 'В приезжающих'], '', 'Тип',
          title='Количество нуждающихся населённых пунктов', width=15, size=11, height=6,
          showBarLabel=False, needsSort=False)
