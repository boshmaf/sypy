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

class BaseDetectorBenchmark:

    def __init__(self, detector, runs):
        self.detector = detector
        self.runs = runs
        self.bench_results = {}

    def __check_integrity(self):
        if not isinstance(self.detector, sypy.BaseDetector):
            raise Exception("Invalid detector")

    def start(self):
        raise NotImplementedError("This method is not supported")

class SimpleDetectorBenchmark(BaseDetectorBenchmark):

    def __init__(self, detector, arg_name, arg_values, runs=1):
        BaseDetectorBenchmark.__init__(self, detector, runs)
        self.arg_name = arg_name
        self.arg_values = arg_values

    def run(self):
        for arg_value in self.arg_values:
            setattr(self.detector, self.arg_name, arg_value)
            results = self.detector.detect()
            self.bench_results[arg_value] = results

    def roc_analysis(self, plot=True, file_name=None, file_type="pdf", font_size=18):
        if not self.bench_results:
            raise Exception("Run the benchmark first.")

        operating_values = sorted(self.bench_results.keys())
        if min(operating_values) != 0.0 or max(operating_values) != 1.0:
            raise Exception("Invalid argument value range.")

        tpr = []
        fpr = []
        for value in operating_values:
            tpr.append( self.bench_results[value].sensitivity() )
            fpr.append( 1.0 - self.bench_results[value].specificity() )

        auc = self.__compute_auc(fpr, tpr)
        if plot:
            self.__plot_roc(fpr, tpr, auc, file_name, file_type, font_size)

        data = [ (fpr[i], tpr[i]) for i in range(0, len(fpr)) ]
        self.roc_curve = {
            "data": data,
            "auc": auc
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

    def __plot_roc(self, fpr, tpr, auc, file_name, file_format, font_size):
        fig = plt.figure()
        fig.suptitle("auc={0:.2f}, threshold={1}".format(auc, self.arg_name))

        ax = fig.add_subplot(111)
        matplotlib.rcParams.update({"font.size": font_size})

        name = self.detector.__class__.__name__

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


