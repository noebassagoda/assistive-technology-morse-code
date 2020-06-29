#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Chotox utility for debug
#
# Copyright (c) 2012-2015 Alan Aguiar alanjas@hotmail.com
# Copyright (c) 2012-2015 Butiá Team butia@fing.edu.uy
# Butia is a free and open robotic platform
# www.fing.edu.uy/inco/proyectos/butia
# Facultad de Ingeniería - Universidad de la República - Uruguay
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from usb4butia import USB4Butia
from baseboard import Baseboard
from device import Device
import random

ERROR = -1

class Chotox(USB4Butia):

    def __init__(self, debug=False, get_modules=True):
        USB4Butia.__init__(self, debug, False)
        self._debug_flag = debug
        self.max_h = 14
        self.max_p = 6
        self.create_all()
        if get_modules:
            self.getModulesList(refresh=False)

    def create_all(self):
        b = Baseboard(None)
        listi = ['admin', 'pnp', 'port', 'ax', 'button', 'hackp', 'motors', 'butia', 'led']
        listi = listi + ['grey', 'light', 'res', 'volt', 'temp', 'distanc']
        listi = listi + ['modActA', 'modActB', 'modActC', 'modSenA', 'modSenB', 'modSenC']
        for i, m in enumerate(listi):
            b.listi[i] = m
        hotplug = {2:'modSenA', 4:'grey', 5:'distanc'}
        for m in hotplug:
            b.add_device(m, Device(b, hotplug[m], m, self._drivers_loaded[hotplug[m]]))
        openables = {0:'admin', 7:'pnp'}
        for m in openables:
            b.add_device(m, Device(b, openables[m], m, self._drivers_loaded[openables[m]], True))
        self._bb.append(b)

    def getModulesList(self, normal=True, refresh=True):
        """
        Get the list of modules loaded in the board
        """
        self._debug('=Listing Devices')
        modules = []
        self._debug('===board', 0)
        b = self._bb[0]
        for i in range(self.max_h):
            if b.devices.has_key(i):
                module_name = b.devices[i].name
            elif i <= self.max_p:
                module_name = 'port'
            
            if b.devices.has_key(i) or (i < 7):
                complete_name = module_name + ':' +  str(i)
                modules.append(complete_name)
                self._debug('=====module ' + module_name + (9 - len(module_name)) * ' ' + complete_name)

        return modules
        
    def callModule(self, modulename, board_number, number, function, params = [], ret_type = int):
        """
        Call one function: function for module: modulename in board: board_name
        with handler: number (only if the module is pnp, else, the parameter is
        None) with parameteres: params
        """
        board = self._bb[0]
        self._open_or_validate(modulename, board)

        if modulename == 'butia' and function == 'getVolt':
            return 10.5
        elif modulename == 'motors' and function == 'getType':
            return 2

        if function == 'getValue':
            if modulename == 'button':
                return random.randrange(0, 2)
            elif modulename == 'grey' or modulename == 'distanc':
                return random.randrange(0, 65536)
            elif modulename == 'modSenA':
                return random.randrange(0, 65536)
            else:
                return ERROR
        elif function == 'getVersion':
            if modulename == 'admin':
                return 7
            else:
                return 1
        elif function == 'send':
            if len(params) > 0:
                return params[0]
            return ''
        else:
            return ERROR

    def refresh(self):
        """
        Search for connected USB4Butia boards and open it
        """
        pass

    def close(self):
        """
        Closes all open baseboards
        """
        pass

    def moduleOpen(self, mod):
        """
        Open the module mod
        """
        split = self._split_module(mod)
        modulename = split[1]
        b = int(split[2])
        if len(self._bb) < (b + 1):
            return ERROR
        board = self._bb[b]
        return self._open_or_validate(modulename, board)

    def _open_or_validate(self, modulename, board):
        """
        Open o check if modulename module is open in board: board
        """
        if modulename in self._openables:
            if modulename in board.get_openables_loaded():
                return board.get_device_handler(modulename)
            else:
                m = self._max_handler()
                dev = Device(board, modulename, m, self._drivers_loaded[modulename], True)
                board.add_device(m, dev)
                return m
        return ERROR

    def moduleClose(self, mod):
        """
        Close the module mod
        """
        split = self._split_module(mod)
        modulename = split[1]
        if modulename in self._openables:
            b = int(split[2])
            if len(self._bb) < (b + 1):
                return ERROR
            board = self._bb[b]
            if modulename in board.get_openables_loaded():
                number = board.get_device_handler(modulename)
                board.remove_device(number)
                return number
            else:
                self._debug('cannot close no opened module')
                return ERROR
        else:
            self._debug('cannot close no openable module')
        return ERROR

    def _max_handler(self):
        b = self._bb[0]
        l = b.devices.keys()
        m = range(self.max_p + 1, self.max_h)
        for e in m:
            if not(e in l):
                return e

