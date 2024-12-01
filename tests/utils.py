from pynvml import nvmlInit, nvmlDeviceGetCount, NVMLError
import hashlib

def normalize_name_collection(collection_name: str):
    return hashlib.md5(collection_name.encode()).hexdigest()


def check_gpu_available():
    try:
        nvmlInit()
        n_gpus = nvmlDeviceGetCount()
        return n_gpus > 0
    except NVMLError:
        return False