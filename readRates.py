#!/usr/bin/env python

def readRates(indexReturn,startDate):
    rateFile = open('macroeconforward.txt','r')
    headerline= rateFile.readline()
    rateIndexList = headerline.split('\t')
    rateIndex=1
    for rateIndexName in rateIndexList:
        if rateIndexName == 'LIBOR1MonRate':
            lib1m_idx = rateIndex
        elif rateIndexName == 'LIBOR3MonRate':
            lib3m_idx = rateIndex
        elif rateIndexName == 'LIBOR6MonRate':
            lib6m_idx = rateIndex
        elif rateIndexName == 'LIBOR12MonRate':
            lib12m_idx = rateIndex
        elif rateIndexName == 'PrimeRate':
            prime_idx = rateIndex
        elif rateIndexName == 'TreasAvg':
            mta_idx =rateIndex
        elif rateIndexName == 'CMT1YearRate':
            cmt12m_idx = rateIndex
        else:
            pass
        rateIndex=rateIndex+1
    
    lib1m   =   dict()
    lib3m   =   dict()
    lib6m   =   dict()
    lib12m  =   dict()
    prime   =   dict()
    mta     =   dict()
    cmt12m  =   dict()
    
    while True:
        line = rateFile.readline()
        if len(line) == 0:
            print ('EOD')
            break
        dataList = line.split('\t')
        
        columnIndex=1
        for data in dataList:
            if columnIndex==1:
                actdate=data
            elif columnIndex == lib1m_idx:
                lib1m[actdate]=data
            elif columnIndex == lib3m_idx:
                lib3m[actdate]=data
            elif columnIndex == lib6m_idx:
                lib6m[actdate]=data
            elif columnIndex == lib12m_idx:
                lib12m[actdate]=data
            elif columnIndex == prime_idx:
                prime[actdate]=data
            elif columnIndex == mta_idx:
                mta[actdate]=data
            elif columnIndex == cmt12m_idx:
                cmt12m[actdate]=data   
            columnIndex=columnIndex+1
    
    if   indexReturn == 'PRIME':
            return prime[startDate]
    elif indexReturn == 'LIBOR12':
            return lib12m[startDate]
        
        
