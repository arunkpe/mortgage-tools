from decimal import *
import math
from datetime import *
import readRates

class LoanInit:
    Name = "LoanInit"
    def __init__(self,Principal,term,IndexType,margin,rate,init_rate_reset,subsequent_rate_reset,
                 init_rate_cap,init_rate_floor,periodic_rate_cap,periodic_rate_floor,
                 life_rate_cap,life_rate_floor,heloc_line_amt,io_term, originationDate):
        self.principal               = Principal
        self.term                    = term
        self.index                   = IndexType
        self.margin                  = margin
        self.init_rate               = rate
        self.init_rate_reset         = init_rate_reset
        self.subsequent_rate_reset   = subsequent_rate_reset                            
        self.init_rate_cap           = init_rate_cap
        self.init_rate_floor         = init_rate_floor
        self.periodic_rate_cap       = periodic_rate_cap
        self.periodic_rate_floor     = periodic_rate_floor
        self.life_rate_cap           = life_rate_cap
        self.life_rate_floor         = life_rate_floor
        self.heloc_line_amt          = heloc_line_amt
        self.io_term                 = io_term
        self.originationDate         = originationDate
        
        #Check for default values
        if init_rate_cap == -9999:
            self.init_rate_cap       = rate
            self.init_rate_floor     = rate
            self.periodic_rate_cap   = rate
            self.periodic_rate_floor = rate
            self.life_rate_cap       = rate
            self.life_rate_floor     = rate
        
        if self.io_term > 0 and self.margin > 0 and self.heloc_line_amt > 0:
            self.product = 'HELOC'
        else:
            self.product = 'FIXED'
        
        
def amortization_table(Loan):
    ''' Prints the amortization table for a loan.

    Prints the amortization table for a loan given
    the principal, the interest rate (as an APR), and
    the term (in months).'''
    # Print headers
    print('Pmt no'.rjust(6), ' ', 'Beg. bal.'.ljust(13), ' ',)
    print('Payment'.ljust(9), ' ', 'Principal'.ljust(9), ' ',)
    print('Interest'.ljust(9), ' ', 'End. bal.'.ljust(13))
    print(''.rjust(6, '-'), ' ', ''.ljust(13, '-'), ' ',)
    print(''.rjust(9, '-'), ' ', ''.ljust(9, '-'), ' ',)
    print(''.rjust(9, '-'), ' ', ''.ljust(13, '-'), ' ')
    
    begBal = Loan.principal
    
    # Print data
    for mth in range(1, Loan.term + 1):
        loanAgeDate = AddMth(mth,Loan.originationDate)
        rate        = getMonthlyRate(loanAgeDate,Loan)
        if   Loan.Product is 'FIXED':    
                payment = pmt(Loan.principal, rate, Loan.term)
                intPmt  = round(begBal * (rate / (12 * 100.0)), 6)
                prinPmt = round(payment-intPmt,2) 
        elif  Loan.Product is 'HELOC' and mth < io_term:
                intPmt  = round(begBal * (rate / (12 * 100.0)), 6)
                if mth < io_term:
                    prinPmt = 0
                else:
                    prinPmt = begBal/(Loan.term-mth)
                payment = round(intPmt+prinPmt,2)                
        endBal  = round(begBal - prinPmt, 2)

        print(str(mth).center(6), ' ',)
        print('{0:,.2f}'.format(begBal).rjust(13), ' ',)
        print('{0:,.2f}'.format(payment).rjust(9), ' ',)
        print('{0:,.2f}'.format(prinPmt).rjust(9), ' ',)
        print('{0:,.2f}'.format(intPmt).rjust(9), ' ',)
        print('{0:,.2f}'.format(endBal).rjust(13))
        print('{0:,.3f}'.format(float(fwdRate[mth][1])).rjust(13))
        print('{0:,.3f}'.format(rate).rjust(13))

        begBal = endBal
    
def pmt(principal, rate, term):
    '''Calculates the payment on a loan.

    Returns the payment amount on a loan given
    the principal, the interest rate (as an APR),
    and the term (in months).'''
    
    ratePerTwelve = rate / (12 * 100.0)
    
    result = principal * (ratePerTwelve / (1 - (1 + ratePerTwelve) ** (-term)))

    # Convert to decimal and round off to two decimal
    # places.
    result = round(result, 2)
    return result

def getMonthlyRate(loanAgeDate,Loan):
    '''Returns the monthly rate for a given loan
    Applies all the appropriate rate caps and floors.'''
    
    #First Read the appropriate rate from the rate files 
    rate = readRates.readRates("PRIME",loanAgeDate)
    print(rate)
   
    while (loanAge < Loan.init_rate_reset):
        rate = Loan.init_rate
    if (loanAge % Loan.subsequent_rate_reset == 0):
        
        rate = round((rate + margin)*8)/8 #the index is lagged by 1 month and all rates are adjusted to nearest 0.125
    else:
        rate = previousRate
        
    #Periodic Rate Adjustments - Apply the floor rate
    if ((loanAge == Loan.init_rate_period)):
        rate = max(rate,Loan.init_rate_floor)
    else:
        rate = max(rate,Loan.periodic_rate_floor)
    #Periodic Rate Adjustments - Apply the cap rate                    
    if ((loanAge == Loan.init_rate_period)):
        rate = min(indexRate,Loan.init_rate_cap)
    else:
        rate = min(indexRate,Loan.periodic_rate_cap)
        
    #Lifetime Rate Adjustments - Apply lifetime cap and floor
    rate = max(rate,Loan.life_rate_floor)
    rate = max(rate,Loan.life_rate_cap)
    
    return rate



#Add Month Function
def AddMth(int_MthsToAdd, date_BaseDate):
    int_TtlMth = date_BaseDate.month + int_MthsToAdd
    int_iYear=math.floor(int_TtlMth/12)  
    int_iMth = int_TtlMth%12
    
    if int_iMth == 0:
        int_iMth=12
        int_iYear=int_iYear-1
    return date((date_BaseDate.year + int_iYear), int_iMth, date_BaseDate.day)
        
#Calcualate the difference in months between two dates
def MthDiff(date_Base, date_ToBeSubstr):
    return(date_Base.year-date_ToBeSubstr.year)*12+(date_Base.month-date_ToBeSubstr.month)

#Calculate the Remaining number of Payments
def Calc_RmngNoOfPmt(date_MaturityDate, date_CurrentDate):
    if date_CurrentDate.day >= date_MaturityDate.day:
        RmngNoOfPmt = MthDiff(date_MaturityDate, date_CurrentDate)
    else:
        RmngNoOfPmt = MthDiff(date_MaturityDate, date_CurrentDate)+1
    return RmngNoOfPmt
    
