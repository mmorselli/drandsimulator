# download and uncompress the dataset (drand.db) from https://cdn.lottorace.cloud/drand.rar

from helper import *

attempts = 2000000
slice = attempts // 1000 # how often the results are displayed
jackpotlimit = 80
iterations = 5

challenge(attempts,jackpotlimit,slice,iterations)