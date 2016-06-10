#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

class Bot():
    # Please write your code here.
    def __init__(self):
        pass

    def recv_message(self, msg):
        msg = msg.strip()
        if re.match('bot', msg) == None or msg == 'bot':
            return msg
        command_list = re.split(' +', msg)[1:]

        # ping pong
        if command_list[0] == 'ping':
            return 'pong'

        # todo list
        if command_list[0] == 'todo':
            self.todo(command_list[1:])

    def todo(self, command_list):
        pass

    def todo_add(self, command_list):
        pass

    def todo_delete(self, command_list):
        pass

    def todo_list(self, command_list):
        pass
