# -*- coding: UTF-8 -*-

import sys
import time, datetime
import pandas

def FormBarFrame (TickTuple, TimeFrame):
    # формирует бары из тиков TickTuple заданного таймфрейма TimeFrame (секунды)
    # Формат: Дата-время, Open, Close, Min, Max, движение цены внутри свечи
    # На выходе [0]-бар - самый последний по времени
    Bars = list ()
    for Tick in TickTuple:
        #ValueTick = int(Tick[20])*100000 + int(Tick[22])*10000 + int(Tick[23])*1000 + int(Tick[24])*100 + int(Tick[25])*10 + int(Tick[26])
        ValueTick = float(Tick[20:])
        LenPrice = 0
        LenPriceCount = 0
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
            
        else:
            if Bars[0][0].timestamp() + TimeFrame - 1 < dt.timestamp():
                # для тика нужен новый бар
                secondstart = (dt.isoweekday() - 1) * 86400 + dt.hour * 3600 + dt.minute * 60 + dt.second
                sec_ost = secondstart % TimeFrame
                dt = datetime.datetime.fromtimestamp(dt.timestamp() - sec_ost)
                Bars.insert(0, [dt, ValueTick, ValueTick, ValueTick, ValueTick, 0])
                LenPriceCount = ValueTick
        if ValueTick < Bars[0][2]:
            Bars[0][2] = ValueTick
        if ValueTick > Bars[0][3]:
            Bars[0][3] = ValueTick
    return Bars

def main ():
    if len (sys.argv) == 1:
        print ("файл не задан")
        sys.exit ()

    with open (sys.argv[1], 'rt') as file:
        TicksFile = file.read()
    
    TicksTuple = tuple(TicksFile.split('\n')[:-1])
    
    second = list([TicksTuple[0]])
    bars = ''

    Bars = (FormBarFrame(TicksTuple, 60))

    s = pandas.Series (x[1] for x in Bars)
    print (s)

    exit()

if __name__ == '__main__':
    main()
