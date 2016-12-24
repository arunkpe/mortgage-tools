#!/usr/bin/env python
import sys
from datetime import *
from Amortization import *
import readRates
import math 

sys.path.append("C:\\Users\\Arun\\Desktop\\Amort")

##LoanInit(self,Principal,term,IndexType,margin,rate,init_rate_reset,subsequent_rate_reset,
##                 init_rate_cap,init_rate_floor,periodic_rate_cap,periodic_rate_floor,
##                 life_rate_cap,life_rate_floor,heloc_line_amt,io_term,
##                 originationDate)


origDate=date(2012,6,1)
originationDate = origDate.strftime("%m/%d/%Y")
origDateStr = (datetime.strptime(originationDate,"%m/%d/%Y"))
mth = origDateStr.month
#add month function
def AddMth(int_MthsToAdd, date_BaseDate):
    int_TtlMth = date_BaseDate.month + int_MthsToAdd
    int_iYear=math.floor(int_TtlMth/12)  
    int_iMth = int_TtlMth%12

    if int_iMth == 0:
        int_iMth=12
        int_iYear=int_iYear-1

print(origDateStr)
print(mth)
print(AddMth(12,origDateStr))

Loan = LoanInit(150000,300,"Prime",2.25,4,1,1,-9999,-9999,-9999,-9999,-9999,-9999,195000,120,origDateStr)

amortization_table(Loan)
