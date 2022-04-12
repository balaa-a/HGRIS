from packages.model.Model import Model
from packages.Import import *
from packages.tool.Utils import IMAGETOOL
from packages.hand.HandSystemCopy import HandSystem

def main():
    # MODEL=Model("./checkpoints/best.pt")
    HANDSYSTEM=HandSystem()
    HANDSYSTEM.start(None)


if __name__=="__main__": 
    main()