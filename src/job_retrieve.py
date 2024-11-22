from qiskit_ibm_runtime import QiskitRuntimeService
from lib import *
import matplotlib.pyplot as plt

service = QiskitRuntimeService(
    channel='ibm_quantum',
    instance='ibm-q/open/main',
    token=my_token
)
job = service.job('cx0e2gapjw300085ssj0')
result = job.result()

print(result.get_counts())

plot_histogram(result.get_counts(), title=f"Results")
plt.tight_layout()
plt.show(block=False)
input()

# To get counts for a particular pub result, use 
#
# pub_result = job_result[<idx>].data.<classical register>.get_counts()
#
# where <idx> is the index of the pub and <classical register> is the name of the classical register. 
# You can use circuit.cregs to find the name of the classical registers.