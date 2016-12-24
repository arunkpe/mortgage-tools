import csv
import linecache

f = open(r'Z:\TDR\Forecast\2012_04Plus08\FMPrismRuns\April_27_Rerun_forPreModPmt\PostMod_NPV_Business_MarME_FM_v47_Unsmear.txt', 'rb')

def tail( f, window=20 ):
    lines= ['']*window
    count= 0
    for l in f:
        lines[count%window]= l
        count += 1
    print(lines[count%window:], lines[:count%window])
    
tail(f,20)
