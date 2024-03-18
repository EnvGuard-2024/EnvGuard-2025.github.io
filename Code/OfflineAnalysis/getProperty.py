import json
from LTL.getLTL import runLTL
from MTL.getMTL import getRegulation


if __name__ == '__main__':
  # runLTL()
  regulations = getRegulation()
  with open("MTLProperty.json", "w") as json_file:
    json.dump(regulations, json_file)