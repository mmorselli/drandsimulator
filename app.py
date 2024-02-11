import time
from helper import *

attempts = 10000
slice = attempts // 10
jackpotlimit = 80


start_time = time.time()

challenge(attempts,jackpotlimit,slice)

end_time = time.time()
execution_time = end_time - start_time
print(f"executed in: {execution_time} seconds")