import matplotlib.pyplot as plt
import numpy as np




price = [53]
for i in range(1, 10000):
    price.append(0.002 + price[-1] + np.random.normal(0,1))
    if price[-1] <= 0:
        price[-1] = 1


plt.plot(price)
plt.show()