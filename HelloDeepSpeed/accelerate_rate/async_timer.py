import asyncio
from dataclasses import dataclass

import pynvml
from pynvml import *

gpu_count = 0

try:
    pynvml.nvmlInit()
    gpu_count = nvmlDeviceGetCount()
except NVMLError as e:
    print(str(e))


@dataclass
class GpuPayload:
    # total_memory: float = 0.0
    # free_memory: float = 0.0
    # used_memory: float = 0.0
    # temperature: float = 0.0
    utilization: c_nvmlUtilization_t = None

    def show(self):
        return self.utilization


def get_gpu_payload(x, i):
    print(round(x * i, 2))

    try:
        gpu_payloads = []
        for gpu_idx in range(0, gpu_count):
            handle = nvmlDeviceGetHandleByIndex(gpu_idx)
            use = pynvml.nvmlDeviceGetUtilizationRates(handle)

            # gpu_info = nvmlDeviceGetMemoryInfo(handle)
            # gpu_temperature = nvmlDeviceGetTemperature(
            #     handle, NVML_TEMPERATURE_GPU)

            gpu_payloads.append(
                GpuPayload(
                    # total_memory=gpu_info.total >> 20,
                    # free_memory=gpu_info.free >> 20,
                    # used_memory=gpu_info.used >> 20,
                    # temperature=gpu_temperature,
                    utilization=use
                )
            )
        return gpu_payloads
    except Exception as e:
        print(str(e))


def write_log_to_file(file_handler, x, i):
    [
        file_handler.write(str(payload.utilization) + "\n") for payload in get_gpu_payload(x, i)
    ]


async def timer(x):
    with open("gpu_payload_log.txt", "w") as file_handler:
        for i in range(0, 1000):
            fu = asyncio.ensure_future(asyncio.sleep(x))
            fu.add_done_callback(
                lambda output: write_log_to_file(file_handler, x, i)
            )
            await fu

# t = timer(0.1)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(t)
