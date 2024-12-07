from pynvml import nvmlInit, nvmlDeviceGetCount, NVMLError


def check_gpu_available():
    try:
        nvmlInit()
        n_gpus = nvmlDeviceGetCount()
        return n_gpus > 0
    except NVMLError:
        return False
