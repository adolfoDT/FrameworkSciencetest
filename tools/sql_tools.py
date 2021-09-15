#!/usr/bin/python3
# -*- encoding:utf-8 -*-

import sys
import logging
import decimal
from pymssql import _mssql
import pytz
from datetime import datetime, timedelta


__author__ = 'Carlos Añorve/Benjamín N'
__version__ = '1.1'
__all__ = ['SQLManagerConnections',
           'general_records']


class SQLManagerConnections:
    def __init__(self, host, user, password):
        super(SQLManagerConnections, self).__init__()
        self.__logger = logging.getLogger('SQL')
        self.__host = host
        self.__user = user
        self.__password = password
        self.conexion = None
        self.__max_intentos_para_cerrar_conexiones = 5
        self.__intentos_para_cerrar_conexiones = 0
    def connect(self, database):
        try:
            self.__logger.info('Connecting to the database: {}'.format(database))
            self.conexion = _mssql.connect(server=self.__host,
                                           user=self.__user,
                                           password=self.__password,
                                           database=database)
        except _mssql.MssqlDatabaseException as error:
            self.__logger.error('Error while trying to connect to database.'
                                ' Error: {}'.format(error))
            sys.exit(1)
        else:
            self.__logger.info('Connecting to the database:: {}'.format(database))

    def check_open_conexions(self):
        if self.__max_intentos_para_cerrar_conexiones > self.__intentos_para_cerrar_conexiones:
            if self.conexion.connected:
                self.__logger.warning('The connection still open.'
                                      'Trying to close connection...')
                self.conexion.close()
                self.__intentos_para_cerrar_conexiones += 1
                self.check_open_conexions()
            else:
                self.__logger.info('There is not open connections.')
                self.__intentos_para_cerrar_conexiones = 0
        else:
            self.__logger.warning('It was not possible to close the connection after {} attempts'
                                  ' try to kill the connection from the system.'
                                  ''.format(self.__intentos_para_cerrar_conexiones))
            self.__intentos_para_cerrar_conexiones = 0

class general_records(SQLManagerConnections):
    def __init__(self, host, user, password):
        super(general_records, self).__init__(host, user, password)
        self.__logger = logging.getLogger('general_records')
    def __Ejecutar_qry(self, databse, qry):
        self.connect(databse)
        if not (self.conexion is None):
            # noinspection PyBroadException
            try:
                self.conexion.execute_query('{}'.format(qry))
            except Exception as details:
                self.__logger.warning(f'Problems in the execution of the query\n'
                                      f'Details: {details}')
            resultado = self.__debug_query()
            self.conexion.close()
            self.check_open_conexions()
            return resultado
    def __debug_query(self):
        try:
            resultado = []
            for reg in self.conexion:
                registro = []
                for llave in list(reg.keys()):
                    if type(llave) is str:
                        if type(reg[llave]) is decimal.Decimal:
                            if not reg[llave].is_nan():
                                try:
                                    reg[llave] = int(reg[llave])
                                except ValueError:
                                    reg[llave] = float(reg[llave])
                        registro.append((llave, reg[llave]))
                resultado.append(dict(registro))
        except Exception as details:
            self.__logger.error('Error trying to debug the query.\n'
                                'Details: {}'.format(details))
            self.check_open_conexions()
        else:
            self.__logger.debug(resultado)
            return resultado
    def general_query(self,columns, direction):
        try:
            qry =""" 
            SELECT {columns} FROM {direction}
                
            """.format(columns= columns, direction = direction)
        except Exception as err:
            self.__logger.warning(f"There was a problem building the query: {err}")
            return []
        resp = self.__Ejecutar_qry("framework",qry)
        return resp

    