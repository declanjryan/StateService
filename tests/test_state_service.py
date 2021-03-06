#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

from unittest import mock
from unittest import TestCase

from datetime import datetime

from .test_fixtures import argparse_fixture
from .test_fixtures import state_machine_fixture
from .test_fixtures import time_machine_fixture
from ..state_service.state_service import app


class TestStateService(TestCase):

    machine_module = 'state_service.state_service.state_machine.StateMachine'
    parser_module = 'argparse.ArgumentParser'
    state_module = 'state_service.state_service.state.State'
    patched_machine_func = f'{machine_module}._read_machine'
    patched_parser_func = f'{parser_module}.parse_known_args'
    patched_now_func = f'{state_module}._now'

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        self.app = None

    @mock.patch(patched_machine_func, return_value=state_machine_fixture())
    @mock.patch(patched_parser_func, return_value=argparse_fixture())
    def test_get_normal_state_tests_current_state(self, *patch):
        expected = 200
        actual = self.app.get('/state?state=state_1')

        self.assertEqual(expected, actual.status_code)

        expected = b'state_1'
        self.assertEqual(expected, actual.data)

    @mock.patch(patched_machine_func, return_value=state_machine_fixture())
    @mock.patch(patched_parser_func, return_value=argparse_fixture())
    def test_put_normal_state_updates_current_state(self, *patch):
        self.app.put('/state?state=state_1')

        expected = 200
        actual = self.app.get('/state?state=state_1')

        self.assertEqual(expected, actual.status_code)

        expected = b'state_1'
        self.assertEqual(expected, actual.data)

        self.app.put('/state?state=state_1')

        expected = 406
        self.app.put('/state?state=state_1')
        actual = self.app.get('/state?state=state_1')

        self.assertEqual(expected, actual.status_code)

        expected = 200
        actual = self.app.get('/state?state=state_2')

        self.assertEqual(expected, actual.status_code)

        expected = b'state_2'
        self.assertEqual(expected, actual.data)

    @mock.patch(patched_machine_func, return_value=time_machine_fixture())
    @mock.patch(patched_now_func, return_value=datetime(3000, 1, 1, 3, 0))
    @mock.patch(patched_parser_func, return_value=argparse_fixture())
    def test_get_time_state_tests_current_state(self, *patch):
        expected = 200
        actual = self.app.get('/state?state=state_1')

        self.assertEqual(expected, actual.status_code)

        expected = b'state_1'
        self.assertEqual(expected, actual.data)

    @mock.patch(patched_machine_func, return_value=time_machine_fixture())
    @mock.patch(patched_now_func, return_value=datetime(3000, 1, 1, 3, 0))
    @mock.patch(patched_parser_func, return_value=argparse_fixture())
    def test_put_time_state_updates_current_state(self, *patch):
        expected = 200
        actual = self.app.get('/state?state=state_2')

        self.assertEqual(expected, actual.status_code)
        expected = 200
        actual = self.app.put('/state?state=state_2')

        self.assertEqual(expected, actual.status_code)
