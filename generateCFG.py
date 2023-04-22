import sys
from utils import buildCFG

if __name__ == "__main__":
    source = sys.argv[1]

    cfgs = buildCFG(source)

    for cfg in cfgs:
        print("\n[+] Function: ", cfg[0])
        print(cfg[1].printer())
