#!/usr/bin/python
# -*- coding: utf-8 -*-
"""!
    ____  ____  ______       __      __       __       _____
   / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_     |__  /
  / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \     /_ <
 / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /
/_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/
                German BOS Information Script
                     by Bastian Schroll

@file:        inoutSource.py
@date:        28.10.2018
@author:      Bastian Schroll
@description: Base class for boswatch input sources
"""
import time
import logging
import threading
from abc import ABC, abstractmethod

logging.debug("- %s loaded", __name__)


class InputBase(ABC):
    """!Base class for handling inout sources"""

    def __init__(self, inputQueue, inputConfig, decoderConfig):
        """!Build a new InputSource class

        @param  inputQueue: Python queue object to store input data
        @param inputConfig: ConfigYaml object with the inoutSource config
        @param decoderConfig: ConfigYaml object with the decoder config"""
        self._inputThread = None
        self._isRunning = False
        self._inputQueue = inputQueue
        self._inputConfig = inputConfig
        self._decoderConfig = decoderConfig

    def start(self):
        """!Start the input source thread"""
        logging.debug("starting input thread")
        self._isRunning = True
        self._inputThread = threading.Thread(target=self._runThread, name="inputThread",
                                             args=(self._inputQueue, self._inputConfig, self._decoderConfig))
        self._inputThread.daemon = True
        self._inputThread.start()

    @abstractmethod
    def _runThread(self, dataQueue, sdrConfig, decoderConfig):
        """!Thread routine of the input source has to be inherit"""

    def shutdown(self):
        """!Stop the input source thread"""
        if self._isRunning:
            logging.debug("wait for stopping the input thread")
            self._isRunning = False
            self._inputThread.join()
            logging.debug("input thread stopped")

    def addToQueue(self, data):
        """!Adds alarm data to the queue for further processing during boswatch client"""
        self._inputQueue.put_nowait((data, time.time()))
        logging.debug("Add received data to queue")
        print(data)
