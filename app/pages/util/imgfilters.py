import cv2
import numpy as np


def to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# def filter_by_thresholding(img):
    

def hist_equalize(img):
    return cv2.equalizeHist(img)


def filter_by_mean_blur(img, kernel_size):
    kernel = np.ones((kernel_size, kernel_size), np.float32)
    return cv2.filter2D(img, -2, kernel)


def filter_by_median_blur(img, x):
    return cv2.medianBlur(img, x)


def filter_by_gaussian_blur(img, mask_size):
    return cv2.GaussianBlur(img, (mask_size, mask_size), 0)


def filter_by_sobel(img, type):
    if type == "Horizontal":
        return cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    if type == "Vertical":
        return cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)


def filter_by_laplacian(img):
    return cv2.Laplacian(img, cv2.CV_64F)


def filter_by_butterworth_low(img, n, cutoff):
    Fshift = np.fft.fftshift(np.fft.fft2(img))

    M, N = img.shape

    H = np.zeros((M, N), dtype=np.float32)

    for u in range(M):
        for v in range(N):
            D = np.sqrt((u-M/2)**2 + (v-N/2)**2)
            H[u, v] = 1 / (1 + (D/cutoff)**(2*n))

    Gshift = Fshift * H
    G = np.fft.ifftshift(Gshift)
    g = np.abs(np.fft.ifft2(G))
    return g


def filter_by_butterworth_high(img, n, cutoff):
    Fshift = np.fft.fftshift(np.fft.fft2(img))
    M, N = img.shape

    H = np.zeros((M, N), dtype=np.float32)

    for u in range(M):
        for v in range(N):
            D = np.sqrt((u-M/2)**2 + (v-N/2)**2)
            H[u, v] = 1 / (1 + (cutoff/D)**(2*n))

    Gshift = Fshift * H
    G = np.fft.ifftshift(Gshift)
    g = np.abs(np.fft.ifft2(G))
    return g
