import fileinput, os
from time import strftime

import imp

imp.load_source('common','/Users/patrick/3cixty/codes/3cixtyCommon/commonFunctions.py')
from common import convertXsdDouble

os.chdir('/Users/patrick/3cixty/codes/3cixtyTransport/railModule/') # @patrick CASA Mac setup
print os.getcwd()

def main():

    inFileB = "DATA/underground_dirty" +".ttl"
    outFileB ="DATA/underground" + ".ttl"
    print('Converting xsd:double')
    convertXsdDouble(inFileB, outFileB)

    print ('DONE!')

if __name__ == "__main__":
    main();

