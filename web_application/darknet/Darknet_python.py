import os
import sys

import tempfile

sys.path.append(os.path.dirname(__file__))

from _darknet import *

# 標準出力・標準エラー出力の抑制
def silent(verbose=False):
    def _silent(func):
        def wrapper(*args, **kwargs):
            if not verbose:
                devnull = open(os.devnull, 'w')
                stdout = os.dup(1)
                stderr = os.dup(2)
                os.dup2(devnull.fileno(), 1)
                os.dup2(devnull.fileno(), 2)

            res = func(*args, **kwargs)

            if not verbose:
                os.dup2(stdout, 1)
                os.dup2(stderr, 2)
                devnull.close()

            return res

        return wrapper
    return _silent

class Darknet:
    def __init__(self, meta_file, cfg_file, weights_file, verbose=False):
        @silent(verbose=verbose)
        def _init():
            self.net = load_net(cfg_file.encode('ascii'), weights_file.encode('ascii'), 0)
            self.meta = load_meta(meta_file.encode('ascii'))

        _init()

    # [ name, conf, (x, y, w, h) ]
    # x, y is the center of the object

    def detect_pil(self, img_pil, format='jpg', verbose=False):
        with tempfile.NamedTemporaryFile(suffix='.%s' % os.path.basename(format)) as fp:
            filename = fp.name
            img_pil.save(fp.name)

            return self.detect_file(filename, verbose)

    def detect_file(self, img_file, verbose=False):
        @silent(verbose=verbose)
        def _detect():
            return detect(self.net, self.meta, img_file.encode('ascii'))

        results = _detect()

        ret = []
        for result in results:
            name, conf, box = result
            ret.append((
                name.decode('utf-8'),
                conf,
                box,
            ))

        return ret

if __name__ == "__main__":
    import argparse
    import time

    parser = argparse.ArgumentParser()
    parser.add_argument('meta', type=str) # *.data
    parser.add_argument('cfg', type=str) # *.cfg
    parser.add_argument('weights', type=str) # *.weights
    parser.add_argument('img', type=str)
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    darknet = Darknet(meta_file=args.meta, cfg_file=args.cfg, weights_file=args.weights, verbose=args.verbose)

    ts = time.time()
    # direct
    results = darknet.detect_file(args.img, verbose=args.verbose)

    # PIL example
    # from PIL import Image
    # img_pil = Image.open(args.img)
    # results = darknet.detect_pil(img_pil, verbose=args.verbose)

    elapsed = time.time() - ts

    print('FPS: %f (%f s)' % (1/elapsed, elapsed))

    print('%d boxes found' % len(results))
    for result in results:
        name, conf, box = result
        print(name, conf, box)
