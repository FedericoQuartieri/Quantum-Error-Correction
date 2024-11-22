from qiskit_ibm_runtime import QiskitRuntimeService
from lib import *
from qiskit.primitives import BitArray
import matplotlib.pyplot as plt

service = QiskitRuntimeService(
    channel='ibm_quantum',
    instance='ibm-q/open/main',
    token=my_token
)
job = service.job('cx0gjxvpx23g008j8vj0')
if not job.done():
    print("Status = " + job.status())
    exit(-1)
result = job.result()[0].data

bitReg = [arr for key,arr in result.items()]
concatBitReg = BitArray.concatenate_bits(bitReg)

print(concatBitReg)
print(concatBitReg.get_counts())

shots = concatBitReg.num_shots
counts = concatBitReg.get_counts()

plot_histogram(counts, title=f"Ancilla results shots={shots}")
plt.tight_layout()
plt.show()