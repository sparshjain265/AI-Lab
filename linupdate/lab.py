import numpy as np
import random
import math
import matplotlib.pyplot as plt

t = 1000
eta = np.random.choice([-1, 1], t)
theta = np.zeros(t)
T = np.arange(1, t+1,1)
for i in range(t):
   theta[i] = sum(eta[0:i])

Tinv = []
for i in T:
   Tinv.append(1/i)

sqTinv = []
for i in Tinv:
   sqTinv.append(math.sqrt(i))

nsqTinv = []
for i in Tinv:
   nsqTinv.append(-1*math.sqrt(i))

plt.plot(T, eta, label = "eta")
plt.plot(T, theta, label = "theta")
plt.plot(T, Tinv, label = "Tinv")
plt.plot(T, sqTinv, label = "sqTinv")
plt.plot(T, nsqTinv, label = "-sqTinv")
plt.legend()
plt.show()


alpha = np.copy(Tinv)
theta[0] = 0
for i in range(1, t):
    theta[i] = theta[i-1] + alpha[i] * (eta[i] - theta[i-1])
plt.plot(T, theta, label = "theta")
plt.plot(T, Tinv, label = "Tinv")
plt.plot(T, sqTinv, label = "sqTinv")
plt.plot(T, nsqTinv, label = "-sqTinv")
plt.legend()
plt.show()


theta0 = np.copy(theta)
theta1 = np.copy(theta)
theta100 = np.copy(theta)
alpha0 = np.copy(alpha)
alpha1 = np.copy(alpha)
alpha100 = np.copy(alpha)

for i in T:
    alpha1[i-1] = 1/(i+1)
    alpha100[i-1] = 1/(i+100)

for i in range(1, t):
    theta1[i] = theta1[i-1] + alpha1[i] * (eta[i] - theta1[i-1])
    theta100[i] = theta100[i-1] + alpha100[i] * (eta[i] - theta100[i-1])

plt.plot(T, Tinv, label = "Tinv")
plt.plot(T, sqTinv, label = "sqTinv")
plt.plot(T, nsqTinv, label = "-sqTinv")

f, p = plt.subplots(1, 3, sharey=True)
p[0].plot(T, theta0, label = "theta0")
p[1].plot(T, theta1, label = "theta1")
p[2].plot(T, theta100, label = "theta100")
f.legend()
plt.show()



alpha = [2, 1, 0.1, 0.01]
theta = np.zeros((len(alpha), t))
f, p = plt.subplots(len(alpha), 1, sharex=True, sharey=True)
for i in range(len(alpha)):
   for j in range(1, t):
      theta[i][j] = theta[i][j-1] + alpha[i] * (eta[j] - theta[i][j-1])
   p[i].plot(T, theta[i], label = "theta" + str(i))
f.legend()
plt.show()



alpha = np.copy(Tinv)
theta = np.zeros(t)
for i in range(1, t):
    theta[i] = theta[i-1] + alpha[i] * (1 + eta[i] - theta[i-1])
plt.plot(T, theta, label = "theta")
plt.plot(T, Tinv, label = "Tinv")
plt.plot(T, sqTinv, label = "sqTinv")
plt.plot(T, nsqTinv, label = "-sqTinv")
plt.show()



theta0 = np.copy(theta)
theta1 = np.copy(theta)
theta100 = np.copy(theta)
alpha0 = np.copy(alpha)
alpha1 = np.copy(alpha)
alpha100 = np.copy(alpha)

for i in T:
    alpha1[i-1] = 1/(i+1)
    alpha100[i-1] = 1/(i+100)

for i in range(1, t):
    theta1[i] = theta1[i-1] + alpha1[i] * (1 + eta[i] - theta1[i-1])
    theta100[i] = theta100[i-1] + alpha100[i] * (1 + eta[i] - theta100[i-1])

plt.plot(T, Tinv, label = "Tinv")
plt.plot(T, sqTinv, label = "sqTinv")
plt.plot(T, nsqTinv, label = "-sqTinv")

f, p = plt.subplots(1, 3, sharey=True)
p[0].plot(T, theta0, label = "theta0")
p[1].plot(T, theta1, label = "theta1")
p[2].plot(T, theta100, label = "theta100")
f.legend()
plt.show()


alpha = [0.3, 0.1, 0.03, 0.01]
theta = np.zeros((len(alpha), t))
f, p = plt.subplots(len(alpha), 1, sharex=True, sharey=True)
for i in range(len(alpha)):
   for j in range(1, t):
      theta[i][j] = theta[i][j-1] + alpha[i] * (1 + eta[j] - theta[i][j-1])
   p[i].plot(T, theta[i], label = "theta" + str(i))
f.legend()
plt.show()

