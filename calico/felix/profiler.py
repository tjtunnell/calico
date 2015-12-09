# -*- coding: utf-8 -*-
# Copyright 2015 Metaswitch Networks
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
calico.felix.profiler
~~~~~~~~~~~~~~~~~~~~~

Utilities for profiling CPU usage etc.
"""

import logging
import signal
import gevent

_log = logging.getLogger(__name__)


def bind_profiler_to_signal(signal_number=signal.SIGUSR2):
    try:
        import gevent_profiler
    except ImportError:
        _log.info("Profiling not available, gevent_profiler not installed.")
        try:
            gevent.signal(signal_number, do_nothing)
        except AttributeError:
            _log.warning("Unable to install no-op SIGUSR2 handler")
            pass
    else:
        _log.info("Profiling enabled, attached to signal %s", signal_number)
        gevent_profiler.set_summary_output("/tmp/felix-profiling-summary.txt")
        gevent_profiler.set_stats_output("/tmp/felix-profiling-stats.txt")
        gevent_profiler.set_trace_output(None)
        gevent_profiler.attach_on_signal(signum=signal_number, duration=60)


def do_nothing(*args, **kwargs):
    _log.info("SIGUSR2 received but gevent_profiler not available.")