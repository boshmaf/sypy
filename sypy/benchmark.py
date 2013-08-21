#    SyPy: A Python framework for evaluating graph-based Sybil detection
#    algorithms in social and information networks.
#
#    Copyright (C) 2013  Yazan Boshmaf
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sypy
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class BaseBenchmark:

    def __init__(self, detector):
        self.detector = detector

    def __check_integrity(self):
        if not isinstance(self.detector, sypy.BaseDetector):
            raise Exception("Invalid detector")

    def run(self):
        raise NotImplementedError("This method is not supported")

class RocAnalysisBenchmark(BaseBenchmark):
    """
    Benchmarks a detector using ROC analysis over a given detection
    threshold and its values. It also computes the curve's AUC.
    """
    def __init__(self, detector, threshold, values=None):
        BaseBenchmark.__init__(self, detector)
        self.threshold = threshold

        self.values = values
        if not self.values:
            self.values = [ i/10.0 for i in xrange(0,11) ]

        self.roc_curve = {}

    def run(self):
        results = {}
        for value in self.values:
            setattr(self.detector, self.threshold, value)
            results[value] = self.detector.detect()

        self.__analyze(results)

    def __analyze(self, results):
        tpr = []
        fpr = []
        for value in sorted(results.keys()):
            tpr.append( results[value].sensitivity() )
            fpr.append( 1.0 - results[value].specificity() )

        self.roc_curve = {
            "fpr": fpr,
            "tpr": tpr,
            "auc": self.__compute_auc(fpr, tpr)
        }

    def __compute_auc(self, x, y, reorder=False):
        """
        Computes the AUC using the trapezoidal rule.
        """
        if len(x) < 2 or len(y) < 2:
            raise Exception("Invalid number of data points")

        direction = 1
        if reorder:
            order = np.lexsort((y, x))
            x, y = x[order], y[order]
        else:
            dx = np.diff(x)
            if np.any(dx < 0):
                if np.all(dx <= 0):
                    direction = -1
                else:
                    raise Exception("Data points need to be reordered.")

        area = direction * np.trapz(y, x)
        return area

    def plot(self, file_name=None, file_format="pdf", font_size=18):
        auc = self.roc_curve["auc"]
        fpr = self.roc_curve["fpr"]
        tpr = self.roc_curve["tpr"]
        name = self.detector.__class__.__name__

        fig = plt.figure()
        fig.suptitle("auc={0:.2f}, threshold={1}".format(auc, self.threshold))

        ax = fig.add_subplot(111)
        matplotlib.rcParams.update({"font.size": font_size})

        plt.xlim([-0.05, 1.05])
        plt.ylim([-0.05, 1.05])

        plt.plot([0, 1], [0, 1], "k--", lw=3, label="Random")
        plt.plot(fpr, tpr, lw=3, label=name)

        plt.xlabel("False positive rate")
        plt.ylabel("True positive rate")
        plt.legend(loc="lower right", prop={"size":font_size})

        if file_name:
            plt.savefig(
                "{0}.{1}".format(file_name, file_format),
                format=file_format
            )
            plt.clf()
        else:
            plt.show()


