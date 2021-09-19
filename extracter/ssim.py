import sys
import os
import cv2
import numpy as np
from optparse import OptionParser
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr

def ssimCompare(file1, file2):
    img1 = cv2.imread(file1, cv2.IMREAD_UNCHANGED)
    img2 = cv2.imread(file2, cv2.IMREAD_UNCHANGED)
    _ssim = ssim(img1, img2, multichannel=True) # return <class 'numpy.float64'>
    return _ssim.item(); # return <class 'float'> on [0, 1]

# other https://lindevs.com/count-number-of-unique-colors-in-image-using-python/
# https://stackoverflow.com/questions/24780697/numpy-unique-list-of-colors-in-the-image
# identify -format "%k" imagefile
def unqiueColors(img):
    # img = cv2.imread("/home/yangzhiwen/downloads/lena.png", cv2.IMREAD_UNCHANGED); # cv2.IMREAD_UNCHANGED
    all_rgb_codes = img.reshape(-1, img.shape[2]) # 三维 to 二维
    unique_rgbs = np.unique(all_rgb_codes, axis=0)
    return len(unique_rgbs)

def psnr(file1, file2):
    img1 = cv2.imread(file1, cv2.IMREAD_UNCHANGED)
    img2 = cv2.imread(file2, cv2.IMREAD_UNCHANGED)
    _psnr = psnr(img1, img2)
    return _psnr

def cwebp(q, input, output, verbose):
    command = "cwebp -quiet -m 6 -q %s %s -o %s" % (q, input, output)
    print(command)
    os.system(command)

def isOptimizable(input, lowestQuality, lowestSsim, expectReducePercent, verbose):
    maxReduceSize = 0
    inputSize = os.stat(input).st_size
    output = "_%s" % os.path.basename(input)
    l = lowestQuality;
    r = 100
    while(l < r): # [l, r)
        q = (l+r) // 2

        try: cwebp(q, input, output, verbose)
        except: return False
        # command = "cwebp -quiet -m 6 -q %s %s -o %s" % (q, input, output)
        # os.system(command)

        try: _ssim = ssimCompare(input, output) * 100
        except: return False
        
        if(_ssim < lowestSsim): # 假设有损压缩q越低，ssim越低。寻找满足指定ssim范围时最低的q
            r = q;
            if(verbose):
                print("~[%2d, %3d) => %2d => %.2f" % (l, r, q, _ssim))

        else:
            outputSize = os.stat(output).st_size
            reduceSize = inputSize - outputSize # 体积减少大小
            reducePercent = reduceSize / inputSize * 100 # 体积减少比例
            if(verbose):
                print("[%2d, %3d) => %2d => %.2f %5d %3d%%" % (l, r, q, _ssim, reduceSize, reducePercent))

            maxReduceSize = max(reduceSize, maxReduceSize)
            l = q + 1;
    
    return maxReduceSize > (inputSize * expectReducePercent / 100)

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: ssim.py [options] file(s)")

    # input ssim q size verbose
    parser.add_option("-q", "--quality", dest="quality", default=1,
        help="the lowest quality, default: 1", type="int")

    parser.add_option("-r", "--reduce", dest="reduce", default=15,
        help="the expect reduce size, default: 15%", type="int")

    parser.add_option("-s", "--ssim", dest="ssim", default=90,
        help="the lowest ssim on [1,100), default: 90", type="int")
    
    parser.add_option("-v", "--verbose", dest="verbose", default=False,  
        action="store_true", help="print with some log")

    parser.add_option("-c", "--copmaressim", dest="copmaressim", default=False, 
        action="store_true", help="copmare ssim")

    (options, args) = parser.parse_args()

    if(options.copmaressim):
        for file in args:
            print(ssimCompare(args[0], file))
    else:
        for file in args:
            try:
                able = isOptimizable(file, options.quality, options.ssim, options.reduce, options.verbose)
                if(able): print(True)
                else: print(False)
            except:
                print(False)

    