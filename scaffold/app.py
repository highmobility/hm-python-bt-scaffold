#!/usr/bin/env python
# The MIT License
#
# Copyright (c) 2014- High-Mobility GmbH (https://high-mobility.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import codecs
import traceback
import datetime
import time
from hmkit import hmkit, linklistener, broadcastlistener, autoapi
import hmkit.autoapi as hm_autoapi
#from hmkit.autoapi import autoapi_dump
from hmkit.autoapi import Identifiers, msg_type, CommandResolver
from hmkit.autoapi.commands import LockUnlockDoors, Notification, SetReductionChargingCurrentTimes, Capabilities
from hmkit.autoapi.commands import get_ignition_state, turn_ignition_onoff, get_vehiclestatus
from hmkit.autoapi.properties.value import Lock, ActionItem, StartStop
from hmkit.autoapi.properties.value.charging import ChargeMode, ChargingTimer, TimerType, ChargePortState, ReductionTime
from hmkit.autoapi.properties import PermissionLocation, PermissionType, Permissions, BitLocation

import logging

log = logging.getLogger('hmkit')

class Link_Listener(hmkit.linklistener.LinkListener):

    def __init__(self):
        pass

    def command_incoming(self, link, cmd):
        """
        Callback for incoming commands received from bluetooth link.
        Change in States will be received in this callback

        :param link Link: :class:`link` object
        :param bytearray cmd: data received
        :rtype: None
        """

        log.info("Len: " + str(len(cmd)))
        log.info("\n App: Cmd :" + str(cmd))

        hmkit_inst = hmkit.get_instance()
        hmkit_inst.autoapi_dump.message_dump(cmd)

        cmd_obj = CommandResolver.resolve(cmd)
        log.debug("cmd_obj: " + str(cmd_obj))
        #log.debug(" isinstance of LockState: " + str(isinstance(cmd_obj, lockstate.LockState)))

        if isinstance(cmd_obj, Capabilities):
            print("App: Capabilities received ")

        return 1

    def command_response(self, link, cmd):
        """
        Callback for command response received from bluetooth link
        Usually Acknowledgements

        :param link Link: :class:`link` object
        :param bytearray cmd: data received
        :rtype: None
        """

        log.info(" LinkListener: App, Response Msg: " + str(cmd) + " Len: " + str(len(cmd)))
        return 1


class Broadcast_Listener(hmkit.broadcastlistener.BroadcastListener):

    def __init__(self):
        self.bt_connected = 0;

    def connected(self, Link):
        log.info("App: Link connected")
        #self.bt_connected = 1;
        #return 1

    def disconnected(self, Link):
        log.info("App: Link disconnected")
        #self.bt_connected = 0;
        return 1

    def state_changed(self, state, old_state):
        # code: place holder api
        log.info("state_changed")

# -----------------------------------------------------------------------

def send_bt_command(hmkit):

    while True:
        if hmkit.bluetooth.broadcaster.is_connected() == False:
            time.sleep(2)
        else:
            constructed_bytes = get_ignition_state.GetIgnitionState().get_bytearray()
            hmkit.bluetooth.link.sendcommand(constructed_bytes)
            return

if __name__== "__main__":

    # Initialise with HMKit class with a Device Certificate and private key.
    # This can accept Base64 strings straight from the Developer Center
    hmkit = hmkit.HmKit(["PASTE DEVICE CERTIFICATE SNIPPET HERE"], logging.DEBUG)

    # Download Access Certificate with the token
    try:
        hmkit.get_instance().download_access_certificate("PASTE ACCESS TOKEN HERE")
    except Exception as e:
        # Handle the error
        log.critical("Error in Access certicate download " + str(e.args[0]))
        print("Error in Access certicate download " + str(e.args[0]))
        hmkit.hmkit_exit()

    # local LinkListener object of sampleapp
    linkListener = Link_Listener()

    # local BroadcastListener object of sampleapp
    broadcastListener = Broadcast_Listener()

    # set link listener for BLE link device events
    hmkit.bluetooth.link.set_listener(linkListener)

    # set Broadcast listener for BT broadcast events
    hmkit.bluetooth.broadcaster.set_listener(broadcastListener)

    # Start BLE broadcasting/advertising
    hmkit.bluetooth.startBroadcasting()

    #hmkit.bluetooth.stopBroadcasting()

    # app. send command through bluetooth
    send_bt_command(hmkit)

    #time.sleep(20)
