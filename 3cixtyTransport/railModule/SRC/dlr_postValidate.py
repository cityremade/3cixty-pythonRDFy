import fileinput, os
from time import strftime

import imp

imp.load_source('common','/Users/patrick/3cixty/codes/3cixtyCommon/commonFunctions.py')
from common import convertXsdDouble

os.chdir('/Users/patrick/3cixty/codes/3cixtyTransport/railModule/') # @patrick CASA Mac setup
print os.getcwd()

def main():
    pathf = "./"
    inFileB = pathf + "DATA/dlr_dirty" +".ttl"
    outFileB = pathf + "DATA/dlr" + ".ttl"

    print('Converting xsd:double')
    convertXsdDouble(inFileB, outFileB)

    print ('DONE!')

if __name__ == "__main__":
    main();

