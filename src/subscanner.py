import cv2 as cv
import glob
import numpy as np
import os
import sys

SUBTITLE_DETECTION_THRESHOLD = 0.45

def scan(src):
    assert(len(src.shape) == 2)

    dft = cv.dft(np.float32(src), flags=cv.DFT_COMPLEX_OUTPUT+cv.DFT_ROWS)
    
    spectrum = cv.magnitude(dft[:,:,0], dft[:,:,1])
    spectrum = 20 * cv.log(spectrum + 1)

    spectrum = np.reshape(np.sum(spectrum, 1), (spectrum.shape[0], 1))
    spectrum -= np.amin(spectrum)
    spectrum /= np.amax(spectrum)
    spectrum *= 255
    spectrum = np.uint8(spectrum)

    kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 5))

    _, binary = cv.threshold(spectrum, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
    binary = cv.morphologyEx(binary, cv.MORPH_CLOSE, kernel, iterations=5)
    binary = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel, iterations=3)

    return binary, spectrum

def find_rect(src):
    r = cv.findContours(src, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

    if type(r) == type(tuple()):
        t = -1
        tt = None

        for rr in r:
            if cv.contourArea(rr) > t:
                t = cv.contourArea(rr)
                tt = rr
        
        r = tt
            
    r = np.reshape(r, (4, 2))

    return r

def do_processing(src_path, dst_path):
    src = cv.imread(src_path)

    assert(sum(src.shape) > 0)

    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    binary, spectrum = scan(gray)

    t = sum(binary > 0) / binary.shape[0]

    if t > SUBTITLE_DETECTION_THRESHOLD:
        print(f"Failed to detect any subtitle from {src_path}")
        print(f"Detected t value of {t}, it should not be higher than {SUBTITLE_DETECTION_THRESHOLD}")
        print(f"Writing spectrum image to {dst_path}")

        cv.imwrite(dst_path, np.repeat(spectrum, gray.shape[1], 1))

        return

    binary = np.repeat(binary, gray.shape[1], 1)

    r = find_rect(binary)

    gray = gray[r[0][1]:r[1][1]+1,:]
    gray = cv.transpose(gray)

    binary_cols, _ = scan(gray)
    binary_cols = cv.transpose(binary_cols)
    binary_cols = np.repeat(binary_cols, gray.shape[1], 0)

    binary[r[0][1]:r[1][1]+1,:] = binary_cols
    
    r = find_rect(binary)

    cv.imwrite(dst_path, src[max(r[0][1]-5, 0):r[1][1]+5,max(r[0][0]-20, 0):r[2][0]+20,:])

def main():
    assert(len(sys.argv) == 3 or len(sys.argv) == 4)

    src = sys.argv[1]
    dst = sys.argv[2]

    if len(sys.argv) == 4 and sys.argv[3] == "-clean":
        clean = True
    else:
        clean = False

    assert(not((os.path.isdir(src) or '*' in src) and not os.path.isdir(dst)))

    if os.path.isdir(src):
        src = glob.glob(os.path.join(src, '*'))
    elif '*' in src:
        src = glob.glob(os.path.join(src))
    else:
        src = [src]

    if os.path.isdir(dst):
        if clean:
            for f in glob.glob(os.path.join(dst, '*')):
                os.remove(f)

        dst = [os.path.join(dst, os.path.split(s)[-1]) for s in src]
    else:
        dst = [dst]
    
    for i, s in enumerate(src):
        do_processing(s, dst[i])

if __name__ == '__main__':
    main()