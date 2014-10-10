
import argparse

verbose = False


parser = argparse.ArgumentParser(description='Mapping Algorithm using Tabu Search')
parser.add_argument("-m", type=int, help="The lenght of tiles row")
#parser.add_argument("-v", "--verbose", action="store_true")


args = parser.parse_args()
