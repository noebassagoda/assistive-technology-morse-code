#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# USB4Butia main
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


import os
import imp
import inspect
import com_usb
from baseboard import Baseboard
from device import Device
from functions import ButiaFunctions

ERROR = -1

class USB4Butia(ButiaFunctions):

    def __init__(self, debug=False, get_modules=True):
        self._debug_flag = debug
        self._hotplug = []
        self._openables = []
        self._drivers_loaded = {}
        self._bb = []
        self._b_ports = []
        self._get_all_drivers()
        self.refresh()
        if get_modules:
            self.getModulesList(refresh=False)

    def _debug(self, message, err=''):
        if self._debug_flag:
            print message, err

    def closeService(self):
        """
        Close bobot service
        """
        return 0

    def getButiaCount(self):
        """
        Gets the number of boards detected
        """
        return len(self._bb)

    def getModulesList(self, refresh=True):
        """
        Get the list of modules loaded in the board
        """
        self._debug('=Listing Devices')
        modules = []
        if refresh:
            self.refresh()
        n_boards = self.getButiaCount()
        for i, b in enumerate(self._bb):
            try:
                listi = b.get_listi()
                s = b.get_handler_size()
                self._debug('===board', i)
                for m in range(0, s + 1):
                    t = b.get_handler_type(m)
                    if not (t == 255):
                        module_name = listi[t]
                        if n_boards > 1:
                            complete_name = module_name + '@' + str(i) + ':' +  str(m)
                        else:
                            complete_name = module_name + ':' +  str(m)
                        self._debug('=====module ' + module_name + (9 - len(module_name)) * ' ' + complete_name)
                        if not(module_name == 'port'):
                            modules.append(complete_name)
                            if not(b.devices.has_key(m) and (b.devices[m].name == module_name)):
                                d = Device(b, module_name, m, self._drivers_loaded[module_name], module_name in self._openables)
                                b.add_device(m, d)
                        else:
                            b.remove_device(m)
            except Exception, err:
                self._debug('ERROR:usb4butia:get_modules_list', err)
        return modules

    def _get_all_drivers(self):
        """
        Load the drivers for the differents devices
        """
        # current folder
        path_drivers = os.path.join(os.path.dirname(__file__), 'drivers')
        self._debug('Searching drivers in: ', str(path_drivers))
        # normal drivers
        tmp = os.listdir(path_drivers)
        tmp.sort()
        for d in tmp:
            if d.endswith('.py'):
                name = d.replace('.py', '')
                self._openables.append(name)
                self._get_driver(path_drivers, name)
        # hotplug drivers
        path = os.path.join(path_drivers, 'hotplug')
        tmp = os.listdir(path)
        tmp.sort()
        for d in tmp:
            if d.endswith('.py'):
                name = d.replace('.py', '')
                self._hotplug.append(name)
                self._get_driver(path, name)

    def _get_driver(self, path, driver):
        """
        Get a specify driver
        """
        self._debug('Loading driver %s...' % driver)
        abs_path = os.path.abspath(os.path.join(path, driver + '.py'))
        try:
            self._drivers_loaded[driver] = imp.load_source(driver, abs_path)
        except:
            self._debug('ERROR:usb4butia:_get_driver cannot load %s' % driver, abs_path)
        
    def callModule(self, modulename, board_number, number, function, params = [], ret_type = int):
        """
        Call one function: function for module: modulename in board: board_name
        with handler: number (only if the module is pnp, else, the parameter is
        None) with parameteres: params
        """
        try:
            number = int(number)
            board_number = int(board_number)
            if len(self._bb) < (board_number + 1):
                return ERROR
            board = self._bb[board_number]
            if board.devices.has_key(number) and (board.devices[number].name == modulename):
                return board.devices[number].call_function(function, params)
            else:
                number = self._open_or_validate(modulename, board)
                if number == ERROR:
                    return ERROR
                return board.devices[number].call_function(function, params)
        except Exception, err:
            if hasattr(err, 'errno'):
                if (err.errno == 5) or (err.errno == 19):
                    self.closeB(board)
            self._debug('ERROR:usb4butia:callModule', err)
            return ERROR

    def refresh(self):
        """
        Search for connected USB4Butia boards and open it
        """
        devices_ports = []
        devices = com_usb.find()
        for dev in devices:
            n = dev.get_address()
            if not(n == None):
                devices_ports.append(n)
                if not(n in self._b_ports):
                    b = Baseboard(dev)
                    try:
                        b.open_baseboard()
                        self._bb.append(b)
                        self._b_ports.append(n)
                    except Exception, err:
                        self._debug('ERROR:usb4butia:refresh', err)

        for b in self._bb:
            n = b.dev.get_address()
            if not(n in devices_ports):
                self.closeB(b)

    def closeB(self, b):
        try:
            n = b.dev.get_address()
            self._bb.remove(b)
            b.close_baseboard()
            if n in self._b_ports:
                self._b_ports.remove(n)
        except:
            pass

    def close(self):
        """
        Closes all open baseboards
        """
        for b in self._bb:
            self.closeB(b)
        self._bb = []
        self._b_ports = []

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
                dev = Device(board, modulename, None, self._drivers_loaded[modulename], True)
                number = dev.module_open()
                if number == 255:
                    self._debug('cannot open module', modulename)
                    return ERROR
                else:
                    board.add_device(number, dev)
                    return number
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
                try:
                    res = board.devices[number].module_close()
                    if res == 1:
                        board.remove_device(number)
                        return res
                except Exception, err:
                    self._debug('ERROR:usb4butia:moduleClose', err)
                    return ERROR
            else:
                self._debug('cannot close no opened module')
                return ERROR
        else:
            self._debug('cannot close no openable module')
        return ERROR

    def getListi(self, board_number=0):
        """
        returns a list of instanciables modules
        """
        board_number = int(board_number)
        if len(self._bb) < (board_number + 1):
            return []
        board = self._bb[board_number]
        listi = board.get_listi()
        return listi.values()

    def describe(self, mod):
        """
        Describe the functions of a modulename
        """
        split = self._split_module(mod)
        mod = split[1]
        funcs = []
        d = {}
        if self._drivers_loaded.has_key(mod):
            driver = self._drivers_loaded[mod]
            a = dir(driver)
            if '__package__' in a:
                funcs = a[a.index('__package__') + 1:]
            for f in funcs:
                h = getattr(driver, f)
                try:
                    i = inspect.getargspec(h)
                    parameters = i[0]
                    if 'dev' in parameters:
                        parameters.remove('dev')
                    d[f] = parameters
                except:
                    pass
        return d

