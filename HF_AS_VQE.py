import timeit
from qiskit.algorithms.optimizers import SLSQP
from qiskit.primitives import Estimator
from qiskit_nature.drivers import UnitsType
from qiskit_nature.second_q.algorithms import GroundStateEigensolver
from qiskit_nature.second_q.algorithms import VQEUCCFactory
from qiskit_nature.second_q.circuit.library import UCCSD
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import ParityMapper
from qiskit_nature.second_q.mappers import QubitConverter
from qiskit_nature.second_q.transformers import ActiveSpaceTransformer

start = timeit.default_timer()
# --------------------------------------------------------------------
# ************************  Laboratory *****************************
# --------------------------------------------------------------------
# ------------------- Driver ------------------

driver = PySCFDriver(atom='H 0.0 0.0 0.0; F 0 0 1.80',
                     unit=UnitsType.ANGSTROM, charge=0, spin=0, basis='STO3G')

# ---------------- Full Problem ----------------
full_problem = driver.run()

# --------------------------------------------------------------------
# ************************  Problem Defining *****************************
# --------------------------------------------------------------------

# ---------------- Reduction To HOMO LUMO Problem ----------------
#as_transformer = ActiveSpaceTransformer(8, 5, active_orbitals=[[1, 2, 3, 4, 5]])
#as_transformer = ActiveSpaceTransformer(10, 6, active_orbitals=[0, 1, 2, 3, 4, 5])
as_transformer = ActiveSpaceTransformer(6, 4, active_orbitals=[2, 3, 4, 5])

problem = as_transformer.transform(full_problem)



# -------------- Dictionaries --------------
optimizer = SLSQP()
estimator = Estimator()
ansatz = UCCSD()
mapper = ParityMapper()

# -------------- Calculation --------------
converter = QubitConverter(mapper=mapper, two_qubit_reduction=True)

vqe = VQEUCCFactory(estimator, ansatz, optimizer)

algorithm = GroundStateEigensolver(converter, vqe)

hl_result = algorithm.solve(problem)

print(hl_result)



stop = timeit.default_timer()
runtime = stop - start
print('Run Time: ', runtime, 'sec', ' or ', runtime/60, 'min','\n')
