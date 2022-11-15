import asyncio
from dataclasses import dataclass

import pynvml
from pynvml import *

gpu_count = 0

# try:
#     pynvml.nvmlInit()
#     gpu_count = nvmlDeviceGetCount()
# except NVMLError as e:
#     print(str(e))


@dataclass
class GpuPayload:
    # total_memory: float = 0.0
    # free_memory: float = 0.0
    # used_memory: float = 0.0
    # temperature: float = 0.0
    utilization: c_nvmlUtilization_t = None

    def show(self):
        return self.utilization


def get_gpu_payload(pynvml_handler, x, i):
    print(round(x * i, 2))

    try:

        gpu_count = nvmlDeviceGetCount()

        gpu_payloads = []
        for gpu_idx in range(0, gpu_count):
            handle = nvmlDeviceGetHandleByIndex(gpu_idx)
            use = pynvml_handler.nvmlDeviceGetUtilizationRates(handle)

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


# def write_log_to_file(pynvml_handler, file_handler, x, i):
def write_log_to_file(file_handler, payloads):
    print("-" * 100)
    [
        # file_handler.write(" --- " + str(payload.utilization)) for payload in get_gpu_payload(pynvml_handler, x, i)
        file_handler.write(" --- " + str(payload.utilization)) for payload in payloads
    ]
    file_handler.write("\n")


async def timer(x):
    pynvml.nvmlInit()

    with open("gpu_payload_log.txt", "w") as file_handler:
        for i in range(0, 1000):
            print(i)
            fu = asyncio.ensure_future(asyncio.sleep(x))

            payloads = get_gpu_payload(pynvml, x, i)
            # print([file_handler.write(" --- " + str(payload.utilization)) for payload in get_gpu_payload(pynvml_handler, x, i)])
            print(str([" --- " + str(p.utilization) for p in payloads]) + "\n")
            fu.add_done_callback(
                #lambda output: write_log_to_file(pynvml, file_handler, x, i)
                lambda output: write_log_to_file(file_handler, payloads)
            )
            await fu

# t = timer(0.1)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(t)
