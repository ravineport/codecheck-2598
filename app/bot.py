#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import MySQLdb
from SPARQLWrapper import SPARQLWrapper, JSON


class Bot():
    # Please write your code here.
    def __init__(self):
        self.connector = MySQLdb.connect(host='xxxx', db='xxxx', user='xxxx', charset='utf8')
        self.cursor = self.connector.cursor()
        self.sparql = SPARQLWrapper('http://ja.dbpedia.org/sparql')

    def recv_message(self, msg):
        msg = msg.strip()
        if re.match('bot', msg) == None or msg == 'bot':
            return None
        command_list = re.split(' +', msg)[1:]

        # ping pong
        if command_list[0] == 'ping':
            return 'pong'

        # todo list
        if command_list[0] == 'todo':
            return self.todo(command_list[1:])

        # abstract a word
        if command_list[0] == 'abst':
            return self.abst_word(command_list[1])

    def todo(self, command_list):
        operator = command_list[0]
        ans = ''
        if operator == 'add':
            ans = self.todo_add(command_list[1:])
        elif operator == 'delete':
            ans = self.todo_delete(command_list[1])
        elif operator == 'list':
            ans = self.todo_list()
        return ans

    def todo_add(self, command_list):
        if len(command_list) != 2: return 'format error!'
        command_list = [command.decode('utf-8') for command in command_list]
        sql = u"INSERT INTO todo(title, description) VALUES('{0[0]}','{0[1]}')".format(command_list)
        ans = self.execute_sql(sql)
        if ans == '': ans = 'todo added'
        return ans

    def todo_delete(self, command):
        sql = u"DELETE FROM todo WHERE title='{}'".format(command.decode('utf-8'))
        ans = self.execute_sql(sql)
        if ans == '': ans = 'todo deleted'
        return ans

    def todo_list(self):
        sql = u"SELECT title, description FROM todo"
        ans = self.execute_sql(sql)
        if ans == '':
            result = self.cursor.fetchall()
            if len(result) == 0: return 'todo empty'
            ans = '\n'.join([' '.join(todo) for todo in result])
        return ans

    def execute_sql(self, sql):
        try:
            self.cursor.execute(sql)
            self.connector.commit()
        except MySQLdb.Error, e:
            return 'error!'
        return ''

    def abst_word(self, word):
        query = u"""
            PREFIX abst: <http://dbpedia.org/ontology/abstract>
            SELECT ?x
            WHERE {{ <http://ja.dbpedia.org/resource/{}> abst: ?x .}}
        """.format(word.decode('utf-8'))
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        return results['results']['bindings'][0]['x']['value']


if __name__ == '__main__':
    my_bot = Bot()
    # print my_bot.todo_add(['today', 'aaaaa'])
    # print my_bot.todo_delete('today')
    # print my_bot.todo_list()
    input = raw_input().decode('utf-8')
    print my_bot.abst_word(input)
