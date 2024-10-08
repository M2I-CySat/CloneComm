#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: CloneComm
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import blocks, gr
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
from gnuradio import pdu
from gnuradio import soapy
from gnuradio import uhd
import time
from gnuradio import zeromq
import satellites.core



class sat_downlink_uplink_fall2024(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "CloneComm", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("CloneComm")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "sat_downlink_uplink_fall2024")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1000000
        self.rr_decim = rr_decim = 5
        self.fm_decimate = fm_decimate = 4
        self.deviation = deviation = 150e3
        self.center_freq = center_freq = 436375000

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_sub_msg_source_0 = zeromq.sub_msg_source('tcp://127.0.0.1:5556', 100, False)
        self.zeromq_pub_msg_sink_0 = zeromq.pub_msg_sink('tcp://127.0.0.1:5557', 100, True)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(('', '', "master_clock_rate=120e6")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        # No synchronization enforced.

        self.uhd_usrp_sink_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_gain(0, 0)
        self.soapy_hackrf_source_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_source_0.set_sample_rate(0, samp_rate)
        self.soapy_hackrf_source_0.set_bandwidth(0, 0)
        self.soapy_hackrf_source_0.set_frequency(0, center_freq)
        self.soapy_hackrf_source_0.set_gain(0, 'AMP', False)
        self.soapy_hackrf_source_0.set_gain(0, 'LNA', min(max(16, 0.0), 40.0))
        self.soapy_hackrf_source_0.set_gain(0, 'VGA', min(max(16, 0.0), 62.0))
        self.satellites_satellite_decoder_0 = satellites.core.gr_satellites_flowgraph(file = '/home/groundstation/CloneComm/GNU Radio Files/CYSAT.yml', samp_rate = samp_rate, grc_block = True, iq = True, options = "")
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=240385,
                decimation=19200,
                taps=[],
                fractional_bw=0)
        self.pdu_pdu_to_stream_x_1 = pdu.pdu_to_stream_b(pdu.EARLY_BURST_APPEND, 64)
        self.pdu_pdu_to_stream_x_0 = pdu.pdu_to_stream_b(pdu.EARLY_BURST_APPEND, 64)
        self.network_socket_pdu_0 = network.socket_pdu('UDP_SERVER', '127.0.0.1', '5556', 10000, False)
        self.digital_gfsk_mod_0 = digital.gfsk_mod(
            samples_per_symbol=2,
            sensitivity=1.0,
            bt=1,
            verbose=False,
            log=False,
            do_unpack=True)
        self.blocks_message_debug_0_0_0 = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_message_debug_0_0 = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/home/groundstation/CloneComm/GNU Radio Files/Packets/packets822.txt', False)
        self.blocks_file_sink_0.set_unbuffered(True)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.satellites_satellite_decoder_0, 'out'), (self.network_socket_pdu_0, 'pdus'))
        self.msg_connect((self.satellites_satellite_decoder_0, 'out'), (self.pdu_pdu_to_stream_x_0, 'pdus'))
        self.msg_connect((self.satellites_satellite_decoder_0, 'out'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.uhd_usrp_sink_0, 'async_msgs'), (self.blocks_message_debug_0_0, 'print'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.blocks_message_debug_0_0_0, 'print_pdu'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.pdu_pdu_to_stream_x_1, 'pdus'))
        self.connect((self.digital_gfsk_mod_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.pdu_pdu_to_stream_x_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.pdu_pdu_to_stream_x_1, 0), (self.digital_gfsk_mod_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.soapy_hackrf_source_0, 0), (self.satellites_satellite_decoder_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "sat_downlink_uplink_fall2024")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.soapy_hackrf_source_0.set_sample_rate(0, self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_rr_decim(self):
        return self.rr_decim

    def set_rr_decim(self, rr_decim):
        self.rr_decim = rr_decim

    def get_fm_decimate(self):
        return self.fm_decimate

    def set_fm_decimate(self, fm_decimate):
        self.fm_decimate = fm_decimate

    def get_deviation(self):
        return self.deviation

    def set_deviation(self, deviation):
        self.deviation = deviation

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.soapy_hackrf_source_0.set_frequency(0, self.center_freq)
        self.uhd_usrp_sink_0.set_center_freq(self.center_freq, 0)




def main(top_block_cls=sat_downlink_uplink_fall2024, options=None):

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
