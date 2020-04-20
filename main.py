# -*- coding: UTF-8 -*-

import sys
import time, datetime
import pandas as pd

from PyQt5.QtChart import QCandlestickSeries, QChart, QChartView, QCandlestickSet
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QPointF
from PyQt5 import QtChart as qc

def FormBarFrame (TickTuple, TimeFrame):
    # формирует бары из тиков TickTuple заданного таймфрейма TimeFrame (секунды)
    # Формат: Дата-время, Open, Close, Min, Max, Range (движение цены внутри свечи), Valueme (тиковый объем)
    # На выходе [0]-бар - самый последний по времени
    Bars = list ()
    RangeBar = 0
    RangeBarTmp = 0
    # на сколько надо умножить цену, чтоб избавиться от "." и перевести в int
    Multiplier = 10**(len(TickTuple[0][20:]) - str.find(TickTuple[0][20:],".") - 1)
    Valume = 1
    for Tick in TickTuple:
        try:
            ValueTick = float(Tick[20:])
            t_struct = time.strptime(Tick[:19], "%Y.%m.%d %H:%M:%S")
            dt = datetime.datetime.fromtimestamp(time.mktime(t_struct))

            if len(Bars) == 0:
                # секунд с начала недели
                secondstart = (dt.isoweekday() - 1) * 86400 + dt.hour * 3600 + dt.minute * 60 + dt.second
                # секунд с начала бара
                sec_ost = secondstart % TimeFrame
                # время соответсвует началу бара
                dt = datetime.datetime.fromtimestamp(dt.timestamp() - sec_ost)
                Bars.append([dt, ValueTick, ValueTick, ValueTick, ValueTick, 0, Valume])
                RangeBarTmp = int(ValueTick*Multiplier)
            else:
                if Bars[0][0].timestamp() + TimeFrame - 1 < dt.timestamp():
                    # для тика нужен новый бар
                    RangeBar = 0
                    secondstart = (dt.isoweekday() - 1) * 86400 + dt.hour * 3600 + dt.minute * 60 + dt.second
                    sec_ost = secondstart % TimeFrame
                    dt = datetime.datetime.fromtimestamp(dt.timestamp() - sec_ost)
                    Valume = 1
                    Bars.insert(0, [dt, ValueTick, ValueTick, ValueTick, ValueTick, 0, Valume])
                    RangeBarTmp = int(ValueTick*Multiplier)
                else:
                    if ValueTick < Bars[0][3]:
                        Bars[0][3] = ValueTick
                    if ValueTick > Bars[0][4]:
                        Bars[0][4] = ValueTick
                    Bars[0][2] = ValueTick
                    RangeBar = RangeBar + abs(RangeBarTmp - int(ValueTick*Multiplier))
                    RangeBarTmp = int(ValueTick*Multiplier)
                    Bars[0][5] = RangeBar
                    Valume = Valume + 1
                    Bars[0][6] = Valume
        except:
            print("Except")
            pass
    return Bars

def main ():
    if len (sys.argv) < 3:
        print ("файл не задан")
        sys.exit ()

    with open (sys.argv[1], 'rt') as file:
        TicksFile = file.read()
    
    TicksTuple = tuple(TicksFile.split('\n')[:-1])
    
    Bars = (FormBarFrame(TicksTuple, 60))
    with open(sys.argv[1][:-4] + '_' + sys.argv[2] + '.bars', 'wt') as file:
        for i in reversed(Bars):
            file.write("{0} {1} {2} {3} {4} {5} {6}\n".format(str(i[0]), i[1], i[2], i[3], i[4], i[5], i[6]))

    # Вывод графика
    app = QApplication(sys.argv)
    series = QCandlestickSeries()
    series.setDecreasingColor(Qt.red)
    series.setIncreasingColor(Qt.green)

    #ma5 = qc.QLineSeries()  # 5-days average data line
    tm = []  # stores str type data

    # in a loop,  series and ma5 append corresponding data
    #for num, o, h, l, c in Bars:
    for i in range(len(Bars)):
        series.append(QCandlestickSet(Bars[i][1], Bars[i][4], Bars[i][3], Bars[i][2]))
        #ma5.append(QPointF(num, m))
        tm.append(str(Bars[i][0]))

    chart = QChart()

    chart.addSeries(series)  # candle
    #chart.addSeries(ma5)  # ma5 line

    chart.setAnimationOptions(QChart.SeriesAnimations)
    chart.createDefaultAxes()
    chart.legend().hide()

    chart.axisX(series).setCategories(tm)
    #chart.axisX(ma5).setVisible(False)

    chartview = QChartView(chart)
    ui = QMainWindow()
    ui.setGeometry(50, 50, 500, 300)
    ui.setCentralWidget(chartview)
    ui.show()


    sys.exit(app.exec_())
    #exit()

if __name__ == '__main__':
    main()
