from iota import *
import sys
from threading import Thread
import datetime

SEED1 = b"PZEFQMVCFWIK9XAQYXACLCKTDFWCXUDVNZFVJFFPGDOCHMILTR9BUTPVSQWOIAJFDTECOUKCKD9WEAFE9"
ADDRESS_WITH_CHECKSUM_SECURITY_LEVEL_2 = b"QVFAKWATLPOAGESXLAYBHVEDVAWIQJUIHPIOITSLGLMSO9SIGACSPSSVZ9FQUFZTAQESOAFXRGZNLEXLDGNZX9TYRY"
api = Iota('https://pow1.iota.community:443', seed = SEED1)

class benchmark():
	def __init__(self):
		'''
		if len(sys.argv[1:]) != 4:
			print("Error Numero invalido de argumentos")
			print("Uso: python benchmark.py NUMTHREADS URI NUMBUNDLES NUMTXPERBUNDLE"
			sys.exit(1)
		'''
		self.nthreads = int(sys.argv[1])
		self.uri = sys.argv[2]
		self.nbundles = int(sys.argv[3])
		self.ntxperbundle = int(sys.argv[4])

	def sendTx(self):
		tx = ProposedTransaction(
	              address = Address(ADDRESS_WITH_CHECKSUM_SECURITY_LEVEL_2),
	              value = 0,
	              tag = Tag(b'EXAMPLE'),
	              message = TryteString.from_string('temperatura: 123 Fahrenheit :D')
		)

		l_bundle = [ProposedBundle() for i in range(self.nbundles)]

		for i in range(self.nbundles):
			for j in range(self.ntxperbundle):
				l_bundle[i].add_transaction(tx)
			l_bundle[i].finalize()
			api.send_trytes(trytes=l_bundle[i].as_tryte_strings(), depth=10)


if __name__ == "__main__":
	startProgram = datetime.datetime.now()

	bm = benchmark()
	bm.sendTx()

	th_list = [Thread(target = bm.sendTx) for i in range(bm.nthreads)]

	for th in th_list:
		th.start()

	for th in th_list:
		th.join()

	endProgram = datetime.datetime.now()

	print("Sent {} transactions using {} threads with the {} node in {} seconds.".format(
		bm.nbundles * bm.ntxperbundle * bm.nthreads,
		bm.nthreads,
		bm.uri,
		(endProgram - startProgram).total_seconds()))
