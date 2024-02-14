# download and uncompress the dataset (drand.db) from https://cdn.lottorace.cloud/drand.rar

from helper import *

attempts = 1999999 # how many rounds to extract (max 1999999)
slice = attempts // 1000 # how often the results are displayed
jackpotlimit = 80
iterations = 5

challenge(attempts,jackpotlimit,slice,iterations)