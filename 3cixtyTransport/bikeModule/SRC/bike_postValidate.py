import fileinput
from time import strftime
import imp, os

imp.load_source('common','/Users/patrick/3cixty/codes/3cixtyTransport/commonModule/transportCommon.py')
from common import convertXsdDouble

os.chdir('/Users/patrick/3cixty/codes/3cixtyTransport/bikeModule/') # @patrick CASA Mac setup
print os.getcwd()

inFileB = "DATA/tfl_bikes_dirty.ttl"
outFileB = "DATA/tfl_bikes.ttl"

print('Converting xsd:double')
convertXsdDouble(inFileB, outFileB)

print ('DONE!')


