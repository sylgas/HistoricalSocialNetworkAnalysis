import matplotlib.cm as cmx
import matplotlib.colors as colors
import networkx as nx
from matplotlib import pylab
from networkx.drawing.nx_pydot import graphviz_layout

from src.analysis.graph.centrality import CentralityMeasurer


class GraphDrawer:
    """
    dot - filter for drawing directed graphs
    neato - filter for drawing undirected graphs
    twopi - filter for radial layouts of graphs
    circo - filter for circular layout of graphs
    fdp - filter for drawing undirected graphs
    sfdp - filter for drawing large undirected graphs
    patchwork - filter for squarified tree maps
    osage - filter for array - based layouts
    """
    LAYOUT_PROG = 'fdp'

    """
    http://matplotlib.org/examples/color/colormaps_reference.html
    """
    CMAP_NAME = 'Accent'

    def draw(self, graph):
        pos = nx.random_layout(graph)
        pylab.figure()
        nx.draw(graph, pos=pos)
        pylab.show()

    def draw_groups(self, graph, groups):
        index = 0
        # {node: (float) groupId}
        node_group_list = self.__build_node_group_list(groups)
        color_group_index = self.__build_color_group_index(node_group_list)

        graph = graph.subgraph(node_group_list.keys())
        centrality = nx.degree_centrality(graph)
        ranking = dict(CentralityMeasurer.create_ranking(centrality))

        values = [(color_group_index.get(node_group_list[node], 0.0)) for node in graph.nodes()]
        f = pylab.figure(1)
        ax = self.__build_ax_with_legend(f, values, color_group_index)
        sizes = [v * 2000 for v in centrality.values()]
        labels = {node: self.create_label(node, ranking) for node in graph.nodes()}

        pos = graphviz_layout(graph, prog=GraphDrawer.LAYOUT_PROG)
        nx.draw_networkx_nodes(graph, pos=pos, cmap=GraphDrawer.CMAP_NAME, vmin=0, vmax=max(values), node_color=values,
                               node_size=sizes, ax=ax)
        nx.draw_networkx_labels(graph, pos, font_size=8)
        nx.draw_networkx_edges(graph, pos, width=0.2)

        pylab.axis('off')
        f.set_facecolor('w')

        pylab.legend(loc='lower left')

        f.tight_layout()
        pylab.show()

    @staticmethod
    def __build_ax_with_legend(f, values, color_group_index):
        normalized_colors = colors.Normalize(vmin=0, vmax=max(values))
        cmap = pylab.get_cmap(GraphDrawer.CMAP_NAME)
        scalarMap = cmx.ScalarMappable(norm=normalized_colors, cmap=cmap)
        ax = f.add_subplot(1, 1, 1)
        for label in color_group_index:
            ax.plot([0], [0], color=scalarMap.to_rgba(color_group_index[label]), label=label)
        return ax

    # (nodeId, str(group_index_list))
    @staticmethod
    def __build_node_group_list(groups):
        node_group_list = dict()
        index = 0
        for group in groups:
            index += 1
            for node in group:
                if node not in node_group_list:
                    node_group_list[node] = str(index)
                else:
                    node_group_list[node] += (', ' + str(index))
        return node_group_list

    # (str(group_list), float_index))
    @staticmethod
    def __build_color_group_index(node_group_list):
        color_group_node = dict()
        color_group_index = dict()
        index = 0.0
        for key, value in node_group_list.items():
            if value not in color_group_node:
                index += 1.0
                color_group_index[value] = index
                color_group_node[value] = []
            color_group_node[value].append(key)
        return color_group_index

    @staticmethod
    def create_label(node, ranking):
        if node in ranking:
            return node
        return ''
