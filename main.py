# -*- coding: UTF-8 -*-

import sys
import time, datetime
import pandas as pd

from mpl_finance import candlestick_ohlc
import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


def FormBarFrame (TickTuple, TimeFrame):
    # формирует бары из тиков TickTuple заданного таймфрейма TimeFrame (секунды)
    # Формат: Дата-время, Open, Close, Min, Max, Range (движение цены внутри свечи)
    # На выходе [0]-бар - самый последний по времени
    Bars = list ()
    RangeBar = 0
    RangeBarTmp = 0
    # на сколько надо умножить цену, чтоб избавиться от "." и перевести в int
    Multiplier = 10**str.find(TickTuple[0][20:],".")
    for Tick in TickTuple:
        #ValueTick = int(Tick[20])*100000 + int(Tick[22])*10000 + int(Tick[23])*1000 + int(Tick[24])*100 + int(Tick[25])*10 + int(Tick[26])
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
            Bars.append([dt, ValueTick, ValueTick, ValueTick, ValueTick, 0])
            RangeBarTmp = int(ValueTick*Multiplier)
        else:
            if Bars[0][0].timestamp() + TimeFrame - 1 < dt.timestamp():
                # для тика нужен новый бар
                RangeBar = 0
                secondstart = (dt.isoweekday() - 1) * 86400 + dt.hour * 3600 + dt.minute * 60 + dt.second
                sec_ost = secondstart % TimeFrame
                dt = datetime.datetime.fromtimestamp(dt.timestamp() - sec_ost)
                Bars.insert(0, [dt, ValueTick, ValueTick, ValueTick, ValueTick, 0])
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
            file.write("{0} {1} {2} {3} {4} {5}\n".format(str(i[0]), i[1], i[2], i[3], i[4], i[5]))

    # Вывод графика
    fig, ax = plt.subplots()
    # fig.subplots_adjust(bottom=0.2)
    #ax.xaxis.set_major_locator(mondays)
    #ax.xaxis.set_minor_locator(alldays)
    # ax.xaxis.set_major_formatter(weekFormatter)
    # ax.xaxis.set_minor_formatter(dayFormatter)

    # plot_day_summary(ax, quotes, ticksize=3)
    candlestick_ohlc(ax, zip(mdates.date2num([Bars[i][0] for i in range(len(Bars))]),   # Date
                                            [Bars[i][1] for i in range(len(Bars))],     # Open
                                            [Bars[i][4] for i in range(len(Bars))],     # Hight
                                            [Bars[i][3] for i in range(len(Bars))],     # Low
                                            [Bars[i][2] for i in range(len(Bars))]),    # Close
                            width=1.6)
#    candlestick_ohlc(ax, zip(mdates.date2num(["2016-06-20 01:17:00", "2016-06-20 01:18:00", "2016-06-20 01:19:00"]),
#                                                [104.529, 104.494, 104.538],
#                                                [104.533, 104.544, 104.602],
#                                                [104.529, 104.494, 104.535],
#                                                [104.493, 104.493, 104.602]),
#                            width=0.6)


    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45)
    plt.show()


    exit()

if __name__ == '__main__':
    main()
