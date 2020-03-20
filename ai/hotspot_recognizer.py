import matplotlib.pyplot as plt
import numpy
from scipy.spatial import distance
from sklearn.cluster import MeanShift

from pojos.hotspot import HotSpot


def get_radius(data, labels, curr_label, curr_center):
    relevant_data = [data[i] for i in range(len(data)) if labels[i] == curr_label]
    dists = [distance.euclidean(x, curr_center) for x in relevant_data]
    return max(dists)


class HotSpotRecognizer:
    def recognize_hotspots(self, events):
        data = numpy.array([[e.latitude, e.longitude] for e in events])
        algo = MeanShift()
        clustering = algo.fit(data)
        centers = clustering.cluster_centers_

        print(clustering.cluster_centers_)
        fig, ax = plt.subplots()

        labels = clustering.labels_
        radii = [get_radius(data, labels, i, centers[i]) for i in range(len(centers))]
        for i in range(len(centers)):
            circush = plt.Circle((centers[i][0], centers[i][1]), radii[i], color="red", fill=False)
            ax.add_artist(circush)

       # plt.scatter([x[0] for x in data], [x[1] for x in data])

      #  plt.scatter([x[0] for x in centers], [x[1] for x in centers])
        # plt.xlim(-50, 150)
        # plt.ylim(-50, 150)
     #   plt.show()

     #   print(clustering.labels_)
        return [HotSpot(centers[i][0], centers[i][1], radii[i]) for i in range(len(centers))]
