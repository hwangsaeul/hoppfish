#!/bin/env python3

import pytest

from hoppfish.worker import Worker
from hoppfish.pipeline import Pipeline, GstPipeline


def test_empty_worker():
    worker = Worker()
    worker.start()
    worker.join()
