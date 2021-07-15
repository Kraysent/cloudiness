from subprocess import call
import numpy as np
for mmm in np.arange(3)+4:
	if len(str(mmm))==1:
		ms = '0'+str(mmm)
	else:
		ms = str(mmm)
	call('rsync -azP cheryasov@192.168.15.58:~/panorams/MAP2021-{}-* ./'.format(ms),shell=True)
