#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Groundstation Transmit
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore



from gnuradio import qtgui

class sat_tx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Groundstation Transmit", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Groundstation Transmit")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "sat_tx")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.iq_file_samp_rate = iq_file_samp_rate = 96000
        self.interpolation = interpolation = 6
        self.decimation = decimation = 1
        self.variable_qtgui_range_1 = variable_qtgui_range_1 = 40
        self.samp_rate = samp_rate = 240000
        self.samp_per_symbol = samp_per_symbol = 2
        self.baud = baud = 9600
        self.TX_samp_rate = TX_samp_rate = int(iq_file_samp_rate * interpolation / decimation)
        self.RF_Center_Freq = RF_Center_Freq = 436375000

        ##################################################
        # Blocks
        ##################################################
        self._variable_qtgui_range_1_range = Range(0, 32000, 1, 40, 200)
        self._variable_qtgui_range_1_win = RangeWidget(self._variable_qtgui_range_1_range, self.set_variable_qtgui_range_1, "'variable_qtgui_range_1'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._variable_qtgui_range_1_win)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(240385)
        # No synchronization enforced.

        self.uhd_usrp_sink_0.set_center_freq(RF_Center_Freq, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_gain(0, 0)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=240385,
                decimation=19200,
                taps=[],
                fractional_bw=0)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            variable_qtgui_range_1, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.digital_gfsk_mod_0 = digital.gfsk_mod(
            samples_per_symbol=samp_per_symbol,
            sensitivity=1.0,
            bt=1,
            verbose=False,
            log=False,
            do_unpack=True)
        self.blocks_message_debug_0 = blocks.message_debug(True)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/cysat-radio/Desktop/CloneComm/Newly_Generated_CySat_Packet_For_Uplink', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.uhd_usrp_sink_0, 'async_msgs'), (self.blocks_message_debug_0, 'print'))
        self.connect((self.blocks_file_source_0, 0), (self.digital_gfsk_mod_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.uhd_usrp_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "sat_tx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_iq_file_samp_rate(self):
        return self.iq_file_samp_rate

    def set_iq_file_samp_rate(self, iq_file_samp_rate):
        self.iq_file_samp_rate = iq_file_samp_rate
        self.set_TX_samp_rate(int(self.iq_file_samp_rate * self.interpolation / self.decimation))

    def get_interpolation(self):
        return self.interpolation

    def set_interpolation(self, interpolation):
        self.interpolation = interpolation
        self.set_TX_samp_rate(int(self.iq_file_samp_rate * self.interpolation / self.decimation))

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.set_TX_samp_rate(int(self.iq_file_samp_rate * self.interpolation / self.decimation))

    def get_variable_qtgui_range_1(self):
        return self.variable_qtgui_range_1

    def set_variable_qtgui_range_1(self, variable_qtgui_range_1):
        self.variable_qtgui_range_1 = variable_qtgui_range_1

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_samp_per_symbol(self):
        return self.samp_per_symbol

    def set_samp_per_symbol(self, samp_per_symbol):
        self.samp_per_symbol = samp_per_symbol

    def get_baud(self):
        return self.baud

    def set_baud(self, baud):
        self.baud = baud

    def get_TX_samp_rate(self):
        return self.TX_samp_rate

    def set_TX_samp_rate(self, TX_samp_rate):
        self.TX_samp_rate = TX_samp_rate

    def get_RF_Center_Freq(self):
        return self.RF_Center_Freq

    def set_RF_Center_Freq(self, RF_Center_Freq):
        self.RF_Center_Freq = RF_Center_Freq
        self.uhd_usrp_sink_0.set_center_freq(self.RF_Center_Freq, 0)




def main(top_block_cls=sat_tx, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
