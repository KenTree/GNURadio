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

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Recording Control Block',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.recording = False
        self.message_port_register_in(pmt.intern("record"))
        self.set_msg_handler(pmt.intern("record"), self.handle_msg)
        self.saved_batches = []
        self.saved_samples = 0
        
    def handle_msg(self, msg):
        new_state = pmt.to_bool(msg)
        
        if new_state != self.recording:
            if new_state == True:
                print("Recording started!")
            else:
                print("Recording stopped!")
                print(f"Saved batches: {len(self.saved_batches)}, "
                      f"saved samples: {self.saved_samples}")
            
        self.recording = new_state

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        if self.recording:
            self.saved_batches.append(input_items[0].copy())
            self.saved_samples += len(input_items[0])
        output_items[0][:] = input_items[0]
        return len(output_items[0])
