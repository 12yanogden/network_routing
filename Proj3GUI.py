#!/usr/bin/env python3

import math
import random
import signal
import sys

from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt6.QtWidgets import *
    from PyQt6.QtGui import *
    from PyQt6.QtCore import *
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

# TODO: Error checking on txt boxes
# TODO: Color strings


# Import in the code with the actual implementation
from CS312Graph import *
from NetworkRoutingSolver import *

BLACK = (0, 0, 0)


class PointLineView(QWidget):
    # Signal for sending mouse clicks to the GUI
    pointclicked = pyqtSignal(str, QPointF)

    def __init__(self, status_bar, data_range):
        super(QWidget, self).__init__()
        self.setMinimumSize(600, 400)
        self.click_node = 'start'
        self.pointList = {}
        self.edgeList = {}
        self.labelList = {}
        self.status_bar = status_bar
        self.data_range = data_range
        self.start_pt = None
        self.end_pt = None

    def display_status_text(self, text):
        self.status_bar.showMessage(text)

    def clear_points(self):
        self.pointList = {}

    def clear_edges(self):
        self.edgeList = {}
        self.labelList = {}

    def add_points(self, point_list, color):
        if color in self.pointList:
            self.pointList[color].extend(point_list)
        else:
            self.pointList[color] = point_list

    def set_start_loc(self, point):
        self.start_pt = point
        self.repaint()

    def set_end_loc(self, point):
        self.end_pt = point
        self.repaint()

    def add_edge(self, start_point, end_point, label, edge_color, label_color=None):
        if not label_color:
            label_color = edge_color
        assert (type(start_point) == QPointF)
        assert (type(end_point) == QPointF)
        assert (type(label) == str)
        edge = QLineF(start_point, end_point)
        if edge_color in self.edgeList.keys():
            self.edgeList[edge_color].append(edge)
        else:
            self.edgeList[edge_color] = [edge]
        midp = QPointF((edge.x1() + edge.x2()) / 2.0,
                       (edge.y1() + edge.y2()) / 2.0)
        if edge_color in self.labelList.keys():
            self.labelList[edge_color].append((midp, label))
        else:
            self.labelList[edge_color] = [(midp, label)]

    # Reimplemented to allow setting source/target nodes with mouse click
    def mousePressEvent(self, e):
        scale = self.get_scale()
        self.pointclicked.emit(self.click_node,
                               QPointF((e.x() - self.width()) / scale + 2, (self.height() - e.y()) / scale - 1))
        if self.click_node == 'start':
            self.click_node = 'end'
        else:
            self.click_node = 'start'

    def get_scale(self):
        xr = self.data_range['x']
        yr = self.data_range['y']
        w = self.width()
        h = self.height()
        w2h_desired_ratio = (xr[1] - xr[0]) / (yr[1] - yr[0])
        if w / h < w2h_desired_ratio:
            scale = w / (xr[1] - xr[0])
        else:
            scale = h / (yr[1] - yr[0])
        return scale

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        scale = self.get_scale()
        tform = QTransform()
        tform.translate(self.width() / 2.0, self.height() / 2.0)
        tform.scale(1.0, -1.0)
        painter.setTransform(tform)
        for color in self.edgeList:
            c = QColor(color[0], color[1], color[2])
            painter.setPen(c)
            for edge in self.edgeList[color]:
                ln = QLineF(scale * edge.x1(), scale * edge.y1(), scale * edge.x2(), scale * edge.y2())
                painter.drawLine(ln)
        r = 1.0E3
        rect = QRectF(-r, -r, 2.0 * r, 2.0 * r)
        align = QTextOption(Qt.Alignment(Qt.AlignHCenter | Qt.AlignVCenter))
        for color in self.labelList:
            c = QColor(color[0], color[1], color[2])
            painter.setPen(c)
            for label in self.labelList[color]:
                temp_tform = QTransform()
                temp_tform.translate(self.width() / 2.0, self.height() / 2.0)
                temp_tform.scale(1.0, -1.0)
                pt = label[0]
                temp_tform.translate(scale * pt.x(), scale * pt.y())
                temp_tform.scale(1.0, -1.0)
                painter.setTransform(temp_tform)
                painter.drawText(rect, label[1], align)
        painter.setTransform(tform)
        for color in self.pointList:
            c = QColor(color[0], color[1], color[2])
            painter.setPen(c)
            for point in self.pointList[color]:
                pt = QPointF(scale * point.x(), scale * point.y())
                painter.drawEllipse(pt, 1.0, 1.0)
        if self.start_pt:
            painter.setPen(QPen(QColor(0.0, 255.0, 0.0), 2.0))
            pt = QPointF(scale * self.start_pt.x() - 0.0, scale * self.start_pt.y() - 0.0)
            painter.drawEllipse(pt, 4.0, 4.0)
        if self.end_pt:
            painter.setPen(QPen(QColor(255.0, 0.0, 0.0), 2.0))
            pt = QPointF(scale * self.end_pt.x() - 0.0, scale * self.end_pt.y() - 0.0)
            painter.drawEllipse(pt, 4.0, 4.0)


class Proj3GUI(QMainWindow):
    def __init__(self):
        super(Proj3GUI, self).__init__()
        self.RED_STYLE = "background-color: rgb(255, 220, 220)"
        self.PLAIN_STYLE = "background-color: rgb(255, 255, 255)"
        self.graph = None
        self.initUI()
        self.solver = NetworkRoutingSolver()
        self.gen_params = (None, None)

    def new_points(self):
        # TODO - ERROR CHECKING!!!!
        seed = int(self.randSeed.text())
        random.seed(seed)
        points = []

        xr = self.data_range['x']
        yr = self.data_range['y']
        n_points = int(self.size.text())
        while len(points) < n_points:
            x = random.uniform(0.0, 1.0)
            y = random.uniform(0.0, 1.0)
            if True:
                x_val = xr[0] + (xr[1] - xr[0]) * x
                y_val = yr[0] + (yr[1] - yr[0]) * y
                points.append(QPointF(x_val, y_val))
        return points

    def generate_network(self):
        nodes = self.new_points()
        out_degree = 3
        size = len(nodes)
        edge_list = {}
        for u in range(size):
            edge_list[u] = []
            pt_u = nodes[u]
            chosen = []
            for i in range(out_degree):
                v = random.randint(0, size - 1)
                while v in chosen or v == u:
                    v = random.randint(0, size - 1)
                chosen.append(v)
                pt_v = nodes[v]
                uv_len = math.sqrt((pt_v.x() - pt_u.x()) ** 2 + \
                                   (pt_v.y() - pt_u.y()) ** 2)
                edge_list[u].append((v, 100.0 * uv_len))
            edge_list[u] = sorted(edge_list[u], key=lambda n: n[0])
        self.graph = CS312Graph(nodes, edge_list)
        self.gen_params = (self.randSeed.text(), self.size.text())
        self.view.clear_edges()
        self.view.clear_points()
        self.sourceNode.setText('')
        self.targetNode.setText('')

    def generate_clicked(self):
        if int(self.size.text()) < 4:
            self.status_bar.showMessage('Input Error: Network size must be greater than 3')
        else:
            self.status_bar.showMessage('')
            self.generate_network()
            self.view.add_points([x.loc for x in self.graph.get_nodes()], (0, 0, 0))
            self.view.repaint()
            self.graph_ready = True
            self.check_gen_inputs()
            self.check_path_inputs()

    def display_paths(self, heap_path, heap_time, array_path, array_time):
        self.view.clear_edges()
        if heap_path:
            cost = heap_path['cost']
            for start, end, lbl in heap_path['path']:
                self.view.add_edge(start_point=start, end_point=end, label=lbl, edge_color=(128, 128, 255))
            self.heapTime.setText('{:.6f}s'.format(heap_time))
            if not array_path:
                self.arrayTime.setText('')
                self.speedup.setText('')
        if array_path:
            cost = array_path['cost']
            for start, end, lbl in array_path['path']:
                self.view.add_edge(start_point=start, end_point=end, label=lbl, edge_color=(128, 128, 255))
            self.arrayTime.setText('{:.6f}s'.format(array_time))
            if not heap_path:
                self.heapTime.setText('')
                self.speedup.setText('')
        if heap_path and array_path:
            if heap_time > 0:
                ratio = 1.0 * array_time / heap_time
            else:
                ratio = math.inf
            self.speedup.setText('Heap is {:.3f}x Faster'.format(ratio))
        self.view.repaint()

    def compute_clicked(self):
        self.solver.initialize_network(self.graph)
        do_array = False
        do_heap = False
        if self.useUnsorted.isChecked():
            do_array = True
            heap_path = None
            heap_time = None
        elif self.useHeap.isChecked():
            do_heap = True
            array_path = None
            array_time = None
        else:
            do_array = True
            do_heap = True
        if do_array:
            array_time = self.solver.compute_shortest_paths(int(self.sourceNode.text()) - 1, use_heap=False)
            array_path = self.solver.get_shortest_path(int(self.targetNode.text()) - 1)
            dist = array_path['cost']
        if do_heap:
            heap_time = self.solver.compute_shortest_paths(int(self.sourceNode.text()) - 1, use_heap=True)
            heap_path = self.solver.get_shortest_path(int(self.targetNode.text()) - 1)
            dist = heap_path['cost']
        self.display_paths(heap_path, heap_time, array_path, array_time)
        self.check_path_inputs()
        if dist == float('inf'):
            self.totalCost.setText('UNREACHABLE')
        else:
            self.totalCost.setText('{:.3f}'.format(dist))
        self.view.click_node = 'start'
        self.repaint()

    def check_gen_inputs(self):
        seed = self.randSeed.text()
        size = self.size.text()
        if self.graph:
            if self.gen_params[0] == seed and self.gen_params[1] == size:
                self.generateButton.setEnabled(False)
            elif (seed == '') or (size == ''):
                self.generateButton.setEnabled(False)
            else:
                self.generateButton.setEnabled(True)

    def check_input_value(self, widget, valid_range):
        assert (type(widget) == QLineEdit)
        retval = None
        valid = False
        try:
            sval = widget.text()
            if sval == '':
                valid = True
            else:
                i_val = int(sval)
                if valid_range:
                    if valid_range[0] <= i_val <= valid_range[1]:
                        retval = i_val
                        valid = True
        except:
            pass
        if not valid:
            widget.setStyleSheet(self.RED_STYLE)
        else:
            widget.setStyleSheet('')
        return '' if retval == None else retval

    def check_path_inputs(self):
        if not self.graph_ready:
            self.computeCost.setEnabled(False)
            print(self.sourceNode.styleSheet())
            self.sourceNode.setStyleSheet('')
            self.sourceNode.setEnabled(False)
            self.targetNode.setStyleSheet('')
            self.targetNode.setEnabled(False)
        else:  # HAS GRAPH!!!
            self.sourceNode.setEnabled(True)
            self.targetNode.setEnabled(True)
            self.computeCost.setEnabled(False)
            valid_inds = [1, int(self.gen_params[1])]
            points = self.graph.get_nodes()
            src = self.check_input_value(self.sourceNode, valid_inds)
            if not src == '':
                self.view.set_start_loc(points[src - 1].loc)
            else:
                self.view.set_start_loc(None)
            dest = self.check_input_value(self.targetNode, valid_inds)
            if not dest == '':
                if src == dest:
                    self.targetNode.setStyleSheet(self.RED_STYLE)
                    self.view.set_end_loc(None)
                else:
                    self.view.set_end_loc(points[dest - 1].loc)
            else:
                self.view.set_end_loc(None)
            if (not src == self.last_path[0] or not dest == self.last_path[1]) and \
                    (not src == '') and (not dest == '') and (not src == dest):
                self.computeCost.setEnabled(True)
                self.view.repaint()

    # Listens for signal of mouse click and finds the nearest point and sets it alternately as
    # source or target node
    def set_by_click(self, clicked_node, point):
        if not self.graph_ready:
            pass
        else:
            id = -1
            dist = math.inf
            for node in self.graph.nodes:
                if math.sqrt(pow((abs(node.loc.x() - point.x())), 2) + pow((abs(node.loc.y() - point.y())), 2)) < dist:
                    dist = math.sqrt(pow((abs(node.loc.x() - point.x())), 2) + pow((abs(node.loc.y() - point.y())), 2))
                    id = node.node_id + 1
            if id != -1:
                self.view.clear_edges()
                if clicked_node == 'start':
                    self.sourceNode.setText(str(id))
                elif clicked_node == 'end':
                    self.targetNode.setText(str(id))
                self.check_path_inputs()

    def initUI(self):
        self.setWindowTitle('Network Routing')
        self.setWindowIcon(QIcon('icon312.png'))
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        vbox = QVBoxLayout()
        box_widget = QWidget()
        box_widget.setLayout(vbox)
        self.setCentralWidget(box_widget)
        SCALE = 1.0
        self.data_range = {'x': [-2 * SCALE, 2 * SCALE], \
                           'y': [-SCALE, SCALE]}
        self.view = PointLineView(self.status_bar, \
								  self.data_range)
        self.generateButton = QPushButton('Generate')
        self.computeCost = QPushButton('Compute Cost')
        self.useUnsorted = QRadioButton('Unsorted Array')
        self.useHeap = QRadioButton('Min Heap')
        self.useBoth = QRadioButton('Use Both')
        self.arrayTime = QLineEdit('')
        self.arrayTime.setFixedWidth(120)
        self.arrayTime.setEnabled(False)
        self.heapTime = QLineEdit('')
        self.heapTime.setFixedWidth(120)
        self.heapTime.setEnabled(False)
        self.speedup = QLineEdit('')
        self.speedup.setFixedWidth(200)
        self.speedup.setEnabled(False)
        self.randSeed = QLineEdit('0')
        self.size = QLineEdit('7')
        self.sourceNode = QLineEdit('')
        self.targetNode = QLineEdit('')
        self.totalCost = QLineEdit('0.0')
        h = QHBoxLayout()
        h.addWidget(self.view)
        vbox.addLayout(h)
        h = QHBoxLayout()
        h.addWidget(QLabel('Random Seed: '))
        h.addWidget(self.randSeed)
        h.addWidget(QLabel('Size: '))
        h.addWidget(self.size)
        h.addWidget(self.generateButton)
        h.addStretch(1)
        vbox.addLayout(h)
        h = QHBoxLayout()
        h.addWidget(QLabel('Source Node: '))
        h.addWidget(self.sourceNode)
        h.addWidget(QLabel('Target Node: '))
        h.addWidget(self.targetNode)
        h.addWidget(self.computeCost)
        h.addWidget(QLabel('Total Path Cost: '))
        h.addWidget(self.totalCost)
        self.totalCost.setEnabled(False)
        h.addStretch(1)
        vbox.addLayout(h)
        h = QHBoxLayout()
        h.addWidget(self.useUnsorted)
        h.addWidget(self.arrayTime)
        h.addWidget(self.useHeap)
        h.addWidget(self.heapTime)
        h.addWidget(self.useBoth)
        h.addWidget(self.speedup)
        self.useHeap.setChecked(True)
        h.addStretch(1)
        vbox.addLayout(h)
        self.last_path = (None, None)
        self.computeCost.setEnabled(False)
        self.sourceNode.textChanged.connect(self.check_path_inputs)
        self.targetNode.textChanged.connect(self.check_path_inputs)
        self.view.pointclicked.connect(self.set_by_click)
        self.randSeed.textChanged.connect(self.check_gen_inputs)
        self.size.textChanged.connect(self.check_gen_inputs)
        self.generateButton.clicked.connect(self.generate_clicked)
        self.computeCost.clicked.connect(self.compute_clicked)
        self.graph_ready = False
        self.check_path_inputs()
        self.show()


if __name__ == '__main__':
    # This line allows CNTL-C in the terminal to kill the program
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    w = Proj3GUI()
    sys.exit(app.exec())
