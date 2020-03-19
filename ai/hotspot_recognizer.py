import matplotlib.pyplot as plt
import numpy
from sklearn.cluster import MeanShift

from pojos.hotspot import HotSpot

import matplotlib.pyplot as plt
import numpy
from sklearn.cluster import MeanShift

from pojos.hotspot import HotSpot


class HotSpotRecognizer:
    def recognize_hotspots(self, events):
        data = numpy.array([[e.latitude, e.longitude] for e in events])
        algo = MeanShift()
        clustering = algo.fit(data)
        centers = clustering.cluster_centers_

        print(clustering.cluster_centers_)
        plt.scatter([x[0] for x in data], [x[1] for x in data])
        plt.scatter([x[0] for x in centers], [x[1] for x in centers])
        plt.show()

        return [HotSpot(center[0], center[1], 1) for center in centers]

