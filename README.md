\# Infrastructure Monitoring and Incident Detection System

A modular Python-based log monitoring and incident detection system designed to simulate infrastructure security monitoring.
The system analyzes system logs, detects suspicious activity, and generates strutured alerts in once or watch mode.

\## Overview

This project implements a configurable monitoring engine capable of detecting:

* Brute-force login attempts
* Unauthorized access attempts
* Critical system errors
* Resource-related failures (e.g. disk space warnings)

The system processes log entries, applies rule-based detection logic, and outputs alerts in both human-readable and structured formats.

\## Objectives

* Build a modular monitoring engine
* Implement configurable rule-based detection
* Support real-time and batch log analysis
* Generate structured alert outputs
* Separate detection logic from configuration

\## Features

\### Real-time Monitoring
Continuously monitors logs as new entries are appended.

\### Batch Ananlysis mode
Processes a log file once and generates alerts.

\### Brute-Force Detection
* Tracks failed login attempts per IP address
* Applies time-window evaluation
* Triggers 'CRITICAL' alert when threshold is exceeded
* Includes cooldown logic to prevent alert flooding

\### Error Detection
* Keyword-based 'HIGH' severity alerts
* Generic 'ERROR' fallback classified as 'MEDIUM'

\### Configuration Rules
All detection behaviour is defined in 'config.json'.

\### Structured Output
Alerts are written to:
* 'incident_log.txt'
* 'incident_log.jsonl'

\### Modular Architecture
Detection logic is separated into independent modules within the 'detectors/' directory.

\## Project Structure

infrastructure-monitoring-system/
│
├── monitor.py
├── config.json
│
├── detectors/
│ ├── failed_login.py
│ └── error_detector.py
│
├── tools/
│ ├── generate_logs.py
│ └── dashboard.py
│
├── tests/
│ └── test_detectors.py
│
├── sample_logs/
│ └── system.log
│
└── alerts/

\## Configuration

Detection behaviour is controlled via 'config.json'.

Example:

```json
{
    "failed_login_threshold": 2,
    "failed_login_window_seconds": 300,
    "cooldown_seconds": 5,
    "error_keywords": [
        "Disk space critically low",
        "Unauthorised access attempt"
    ],
    "alert_output_text": "alerts/incident_log.txt",
    "alert_ouput_jsonl": "alerts/incident_log.jsonl"
}


\## Running the System

\### Run Once (Batch Mode)

* This mode reviews logs after an event or test detection logic.
python monitor.py --mode once --log sample_logs/system.log

\### Watch Mode (Real-Time Monitoring)

* Continuously monitors new log entries appended to the file.
python monitor.py --mode watch --log sample_logs/system.log

\## Live Demonstration

Simulates real-time system activity and demonstrates automatioc alert generation.

Terminal 1
python monitor.py --mode watch --log smaple_logs/system.log

Terminal 2
python tools/generate_logs.py

\##Example Alert Output

CRITICAL | Multiple failed logins from 10.0.0.5 (2 attempts in 300s)
MEDIUM | Generic error: ERROR Unauthoried access attempt
HIGH | Error keyword matched: Disk space critically low

\## Unit Testing

This project uses Python's built-in 'unittest' framework to validate detection logic.
The test suite verifies:
* Failed login threshold triggering
* Cooldown enforcement
* Keyword-based error detection
* Generic error classification

Run tests using:

```bash
python -m unittest -v tests.test_detectors
