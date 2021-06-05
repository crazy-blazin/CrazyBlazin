from weakref import KeyedRef
import matplotlib.pyplot as plt
import numpy as np

# a = {}
# try:
#     a['rww'] += 1
# except KeyError as msg:
#     print(KeyError)




for l in range(0, 5):
    price = [53]
    for i in range(1, 100000):
        price.append(0.01 + price[-1] + np.random.normal(0,1))
        # if price[-1] <= 0:
        #     price[-1] = 1


    plt.plot(price)
plt.show()