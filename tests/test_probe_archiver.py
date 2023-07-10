import os
import unittest
from unittest.mock import patch
from types import SimpleNamespace
from freezegun import freeze_time
from datetime import datetime

from argo_probe_archiver.NagiosResponse import NagiosResponse
from argo_probe_archiver.argo_archiver import process_files


class ArgoProbeArchiverTests(unittest.TestCase):
    def setUp(self):
        arguments = {"path": "foo_folder"}
        self.arguments = SimpleNamespace(**arguments)

    def tearDown(self):
        NagiosResponse._msgBagCritical = []

    @patch("builtins.print")
    def test_all_passed(self, mock_print):
        os.mkdir("foo_folder")
        with self.assertRaises(SystemExit) as e:
            process_files(self.arguments)
        os.rmdir("foo_folder")

        mock_print.assert_called_with('OK - All services work fine.')
        self.assertEqual(e.exception.code, 0)

    @patch('builtins.print')
    @patch("argo_probe_archiver.argo_archiver.os.listdir")
    def test_folder_not_found_error(self, mock_listdir, mock_print):
        mock_listdir.side_effect = FileNotFoundError()

        with self.assertRaises(SystemExit) as e:
            process_files(self.arguments)

        mock_print.assert_called_with("CRITICAL - Directory does not exist.")
        self.assertEqual(e.exception.code, 2)

    @freeze_time("2023-07-05")
    @patch("builtins.print")
    @patch("argo_probe_archiver.argo_archiver.sorted")
    @patch("argo_probe_archiver.argo_archiver.parse_conffiles")
    @patch("argo_probe_archiver.argo_archiver.os.listdir")
    def test_missing_file(self, mock_listdir, mock_configparser, mock_sorted_paths, mock_print):
        mock_listdir.return_value = ['ams-consumer-foo1.conf']
        mock_configparser.return_value = '/var/lib/argo-ams-consumer/foo1'
        mock_sorted_paths.side_effect = ['argo-consumer_log_2023-07-03.avro']

        with self.assertRaises(SystemExit) as e:
            process_files(self.arguments)

        mock_print.assert_called_with("CRITICAL - Today's file in FOO1 directory is missing for today.")
        self.assertEqual(e.exception.code, 2)

    @patch('builtins.print')
    @patch("argo_probe_archiver.argo_archiver.os.listdir")
    def test_os_error(self, mock_listdir, mock_print):
        mock_listdir.side_effect = OSError("OSError raised")

        with self.assertRaises(SystemExit) as e:
            process_files(self.arguments)

        mock_print.assert_called_with('CRITICAL - OSError raised ')
        self.assertEqual(e.exception.code, 2)

    @patch('builtins.print')
    @patch("argo_probe_archiver.argo_archiver.parse_conffiles")
    @patch("argo_probe_archiver.argo_archiver.os.listdir")
    def test_value_error(self, mock_listdir, mock_configparser, mock_print):
        mock_listdir.return_value = ['ams-consumer-foo1.conf']
        mock_configparser.side_effect = ValueError("ValueError raised")

        with self.assertRaises(SystemExit) as e:
            process_files(self.arguments)

        mock_print.assert_called_with("CRITICAL - OSError raised ValueError raised ")
        self.assertEqual(e.exception.code, 2)

    @freeze_time("2023-07-05 13:00:01")
    @patch("builtins.print")
    @patch("argo_probe_archiver.argo_archiver.datetime.fromtimestamp")
    @patch("argo_probe_archiver.argo_archiver.os.stat")
    @patch("argo_probe_archiver.argo_archiver.sorted")
    @patch("argo_probe_archiver.argo_archiver.parse_conffiles")
    @patch("argo_probe_archiver.argo_archiver.os.listdir")
    def test_file_not_modified(self, mock_listdir, mock_configparser, mock_sorted_paths, mock_stats, mock_fromtimestamp, mock_print):
        mock_listdir.return_value = ['ams-consumer-foo1.conf']
        mock_configparser.return_value = '/var/lib/argo-ams-consumer/foo1'
        mock_sorted_paths.side_effect = ['argo-consumer_log_2023-07-05.avro']
        mock_stats.return_value.st_mtime = 1111111
        mock_fromtimestamp.return_value = datetime(2023, 7, 5, 10, 30, 21)

        with self.assertRaises(SystemExit) as e:
            process_files(self.arguments)

        mock_print.assert_called_with("WARNING - Today's file in FOO1 directory hasn't been modified in the last 2 hours.")
        self.assertEqual(e.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
