# GNU Radio Projects

This repository tracks my progress on learning GNU Radio

## About

I'm learning software-defined radio (SDR) with [GNU Radio](https://www.gnuradio.org/). This repo holds my tutorial work and the projects I build along the way.

## Hardware

Will be detailed in project folders markdown files.

## Projects 

# Signal Detection v1 - Power-Triggered Recorder

A simulated signal detector that automatically stores complex samples in memory when measured power exceeds a configurable threshold. Recording stops when power falls below the threshold, while monitoring continues.

* Generates a signal mixed with noise.
* Measures average power and compares it against a tested threshold.
* Publishes messages when detection changes.
* Uses those messages to start and stop storing samples in memory.
* Displays the signal and reports recording totals.

**Validation**

With a gaussian noise amplitude fixed at 1 and signal amplitude at 0.5:
* A threshold of 1.17 detected all 256 batches in one-signal present test
* A separate noise-only test produed no false alarms at this threshold 
* Changing the signal source amplitude from 0 to 0.5 triggered recording stop/start transitions 

**Concepts practiced**
Complex IQ samples, average power estimation, threshold detection, asynchronous message passing, state management, and conditional sample recording.

**Current limitations**
The detector identifies elevated power rather than a specific transmission. Recording boundaries are not sample-exact because control messages are asynchronous. Recordings remain in memory, grow with recording duration, and are lost when the program exits.

**Personal Notes**
This project allowed me to question why and how signals mixed in with noise should be treated. I was able to gain a lot more experience with creating my own embedded python blocks to handle signal data while also learning how to use message control in these blocks.