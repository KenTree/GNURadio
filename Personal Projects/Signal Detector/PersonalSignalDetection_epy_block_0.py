"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, threshold=1.17):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Average Power Block',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.samples_since_print = 0
        self.threshold = threshold
        self.total_batches = 0
        self.correct = 0
        self.detection_state = False
        self.message_port_register_out(pmt.intern("detected"))

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        # Calculate each sample's power
        powers = np.abs(input_items[0]) ** 2
        
        # Average the power values and store it
        self.average = np.mean(powers)
                
        self.samples_since_print += len(input_items[0])
        
        # Check if the average signal exceeds the threshold
        detected = bool(self.average > self.threshold)
        
        self.total_batches += 1
        
        if self.detection_state != detected:
            # Insert message / Placeholder return
            self.message_port_pub(
                pmt.intern("detected"),
                pmt.from_bool(detected)
            )
            self.detection_state = detected

        if detected:
            self.correct += 1

        if self.samples_since_print >= 32000:
            print(f"Average power: {self.average:.6f} \nExceed Threshold: {detected}")
            self.samples_since_print = 0
            rate = self.correct / self.total_batches
            print(f"Detected Batches: {self.correct}/{self.total_batches} ({rate:.2%})")
        
        
        output_items[0][:] = input_items[0]
        
        return len(output_items[0])
