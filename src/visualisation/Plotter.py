import matplotlib.pyplot as plt


# line:     list of further values to be presented on plot
# bar:      list of tuple (label, value)
# legend:   list of string
from src import BASE_DIR


class Plotter:
    def line_plot(self, title, x_label, y_label, line):
        fig, ax1 = plt.subplots()
        ax1.plot(line)
        ax1.set_title(title)
        ax1.set_xlabel(x_label)
        ax1.set_ylabel(y_label)
        self.__save_plot(title)

    def multiple_lines_plot(self, title, x_label, y_label, legend, line):
        fig, ax1 = plt.subplots()
        for plot in line:
            ax1.plot(plot[1])
        ax1.legend(legend, loc='upper left')
        ax1.set_title(title)
        ax1.set_xlabel(x_label)
        ax1.set_ylabel(y_label)
        self.__save_plot(title)

    def bar_plot(self, title, x_label, y_label, bars):
        fig, ax1 = plt.subplots()
        ax1.bar([i for i in range(len(bars))], [b[1] for b in bars], 1.)
        plt.xticks([i + 1 / 2. for i in range(len(bars))], [b[0] for b in bars], rotation='vertical')
        ax1.set_title(title)
        ax1.set_xlabel(x_label)
        ax1.set_ylabel(y_label)
        ax1.autoscale(tight=True)
        self.__save_plot(title)

    # def multiple_bars_plot(self, title, x_label, y_label, legend, bars):
    #     fig, ax1 = plt.subplots()
    #     color_cycle = ax1._get_lines.color_cycle
    #     for i in range(len(bars)):
    #         ax1.bar([self.count_bar_position(b[0], i, len(legend)) for b in bars[i]], [b[1] for b in bars[i]],
    #                 width=1.0 / len(legend), align='edge', color=next(color_cycle))
    #     ax1.set_title(title)
    #     ax1.legend(legend, loc='upper left')
    #     ax1.set_xlabel(x_label)
    #     ax1.set_ylabel(y_label)
    #     ax1.autoscale(tight=True)
    #     self.__save_plot(title)

    # def line_and_bar_plot(self, title, x_label, line_label, bar_label, line, bar):
    #     fig, ax1 = plt.subplots()
    #     ax1.plot(line, linewidth=5)
    #     ax1.set_ylabel(line_label)
    #
    #     ax2 = ax1.twinx()
    #     ax2.bar([b[0] for b in bar], [b[1] for b in bar])
    #     ax2.set_ylabel(bar_label)
    #     ax2.set_title(title)
    #     ax1.set_xlabel(x_label)
    #     ax2.autoscale(tight=True)
    #     self.__save_plot(title)

    # def multiple_lines_and_bars_plot(self, title, x_label, line_label, bar_label, legend, lines, bars):
    #     fig, ax1 = plt.subplots()
    #     for line in lines:
    #         ax1.plot(line, linewidth=5)
    #     ax1.set_ylabel(line_label)
    #
    #     ax2 = ax1.twinx()
    #     color_cycle = ax2._get_lines.color_cycle
    #     for i in range(len(bars)):
    #         ax2.bar([self.count_bar_position(b[0], i, len(legend)) for b in bars[i]], [b[1] for b in bars[i]],
    #                 width=1.0 / len(legend), align='edge', color=next(color_cycle))
    #     ax2.autoscale(tight=True)
    #     ax2.set_ylabel(bar_label)
    #     ax2.set_title(title)
    #     ax2.legend(legend, loc='upper left')
    #     ax1.set_xlabel(x_label)
    #     self.__save_plot(title)

    @staticmethod
    def __save_plot(title):
        plt.savefig(BASE_DIR + '/plot/{0}.png'.format(title), bbox_inches='tight')
        plt.close()

    @staticmethod
    def count_bar_position(x, i, length):
        delta = -0.5
        delta += i * (1.0 / length)
        return float(x) + delta
