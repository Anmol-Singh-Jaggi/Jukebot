#!/usr/bin/env python2
import cPickle as pickle
from pprint import pprint

import matplotlib.pyplot as plt


hs = pickle.load(open("history_LSTM.p", "rb"))
print type(hs)
print len(hs)
pprint(hs)


plt.plot([x for x in range(0, 20)], hs['val_loss'])
plt.ylim((0.0, 10.0))
plt.show()

