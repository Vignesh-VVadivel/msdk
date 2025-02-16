################################################################################
 # Copyright (C) 2022 Maxim Integrated Products, Inc., All Rights Reserved.
 #
 # Permission is hereby granted, free of charge, to any person obtaining a
 # copy of this software and associated documentation files (the "Software"),
 # to deal in the Software without restriction, including without limitation
 # the rights to use, copy, modify, merge, publish, distribute, sublicense,
 # and/or sell copies of the Software, and to permit persons to whom the
 # Software is furnished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included
 # in all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 # OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 # MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 # IN NO EVENT SHALL MAXIM INTEGRATED BE LIABLE FOR ANY CLAIM, DAMAGES
 # OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 # ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 # OTHER DEALINGS IN THE SOFTWARE.
 #
 # Except as contained in this notice, the name of Maxim Integrated
 # Products, Inc. shall not be used except as stated in the Maxim Integrated
 # Products, Inc. Branding Policy.
 #
 # The mere transfer of this software does not imply any licenses
 # of trade secrets, proprietary technology, copyrights, patents,
 # trademarks, maskwork rights, or any other form of intellectual
 # property whatsoever. Maxim Integrated Products, Inc. retains all
 # ownership rights.
 #
 ###############################################################################
"""Contains MAX78000 simulator implementations to get CNN model output.
"""
import numpy as np
import torch

import parse_qat_yaml
from .ai85net_faceid import AI85FaceIDNet
import ai85.ai8x as ai8x
from .ai8x import set_device #pylint: disable=relative-beyond-top-level
import torchvision

class Simulator:
    """
    MAX78000 Simulator.
    """
    model = None

    def __init__(self, checkpoint_path):
        self.device = self.__get_device()
        #load model
        set_device(85, True, True)
        self.model = AI85FaceIDNet().to(self.device)
        ai8x.fuse_bn_layers(self.model)
        checkpoint = torch.load(checkpoint_path, map_location=self.device)
        self.model.load_state_dict(checkpoint['state_dict'])
        ai8x.update_model(self.model)
        self.model = self.model.to(self.device)
        self.model.eval()

    def __get_device(self): #pylint: disable=no-self-use
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        print('Running on device: {}'.format(device))
        return device

    def get_model_out(self, data_in):
        """Returns output of the neural network on device."""
        set_device(85, True, True, verbose=False)
        
        in_tensor = data_in.transpose([2, 0, 1])[None, ].copy()
        if in_tensor.dtype == np.uint8:
            in_tensor = in_tensor.astype(np.float32)
            in_tensor -= 128
        else:
            in_tensor = in_tensor.astype(np.float32)
            in_tensor = 255 * in_tensor - in_tensor.min() / (in_tensor.max() - in_tensor.min())
            in_tensor = np.round(in_tensor) - 128
        in_tensor = torch.from_numpy(in_tensor).to(self.device)
        print(in_tensor.min(), in_tensor.max(), in_tensor.shape)
        data_out = self.model(in_tensor)
        return data_out.detach().cpu().numpy()

    def __del__(self):
        if self.model is not None:
            del self.model
        if self.device.type != 'cpu':
            torch.cuda.empty_cache()
