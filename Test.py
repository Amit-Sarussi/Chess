from MoveDepthCalculator import MoveDepthCalculator
import time

tic = time.perf_counter()
MoveDepthCalculator(depth=3)
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")

# tic = time.perf_counter()
# MoveDepthCalculator(depth=4)
# toc = time.perf_counter()
# print(f"Time: {toc - tic:0.4f} seconds")
