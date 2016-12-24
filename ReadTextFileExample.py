#!/usr/bin/env python
rateFile      = open("C:\\Documents and Settings\\nbkm79e\\Desktop\\PythonSamples\\PrimeRate.txt","r")
dateRate      = [line.split() for line in rateFile]
rateFile.close()
print(float(dateRate[1][1])+2.25)