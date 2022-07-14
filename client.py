#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.uix.gridlayout import GridLayout
import urllib


class MainLayout(GridLayout):

    count = 1

    def send_message(self, message):
        POST_data = self._prepare_data(message)
        self._send_message(POST_data)

    def _prepare_data(self, message):
        auth_data = {'message': message}
        auth_data = urllib.parse.urlencode(auth_data)
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        return {'auth_data': auth_data, 'headers': headers}

    def _send_message(self, POST_data):
        UrlRequest(
            url='http://localhost:5000/hello',
            req_body=POST_data['auth_data'],
            req_headers=POST_data['headers'],
            on_failure=self._on_connection_failure,
            on_error=self._on_connection_error,
            on_success=self._on_connection_success,
        )

    def _on_connection_success(self, request, result):
        self.ids.status_label.text =\
            'message %s delivered' % self.count
        self.count += 1

    def _on_connection_failure(self, request, result):
        self.ids.status_label.text = 'connection fail'

    def _on_connection_error(self, request, result):
        self.ids.status_label.text = 'connection error'


class Test(App):
    pass


Test().run()