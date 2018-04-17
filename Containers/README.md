## Objectivos da Aplicação

A aplicação que aqui vai ser desenvolvida tem como objectivo testar a diferença de desempenho de replicação de uma base de dados numa rede containers e numa rede de máquinas virtuais. Para tal vai ser usado o ambiente Docker para a componente dos containers, e software da VMware para as máquinas virtuais.

## Requisitos da Aplicação

A aplicação deve ser independente do ambiente em que será utilizada (containers ou VMs). A mesma será desenvolvida em [Python3](https://www.python.org/download/releases/3.0/), com a base de dados implementada em [MySQL](https://www.mysql.com/). Para fazer pedidos à base de dados será utilizada a API [MySQLdb](http://mysql-python.sourceforge.net/MySQLdb.html) que está disponível como módulo para Python3 nos repositórios do Ubuntu com o nome [python3-mysqldb](https://packages.ubuntu.com/artful/python3-mysqldb).

## Funcionamento da Aplicação

De seguida serão apresentados pedaços de pseudocódigo com alguma semelhança a python para demonstrar e esclarecer o funcionamento da aplicação. Estarão estruturados numa fase de **Inicialização**, **Ciclo** e **Finalização**.

### Inicialização

Na inicialização da aplicação têm de ser passados como argumentos o número de inserções na base de dados por minuto, o número máximo de inserções (*condição de paragem*), o número de clientes instanciados, o endereço do primeiro cliente lançado (os restantes são calculdados) e o número de tuplos que devem ser inseridos de cada vez nas bases de dados remotas:

```console
user@user-pc ~ $ python3 toyapp.py n_inserts_minute n_max_inserts n_clients starting_ip batch_size
```
Como os ambientes não serão todos lançados ao mesmo tempo, existe uma necessidade de serem sincronizados antes de começarem a ser feitas inserções nas bases de dados de outras aplicações na rede, de forma a garantir que os serviços já estão operacionais e prontos a receber pedidos. 
É então usada uma chave (*num_online*) na base de dados de cada uma das aplicações que será incrementada pelos restantes clientes, e que apenas quando for igual ao número de clientes instanciados, permitirá à aplicação prosseguir, garantindo assim alguma sincronização entre todos os clientes na rede, ou seja, um cliente não só tem de incrementar o valor dessa chave em todos os outros clientes, como também tem que aguardar que a sua chave fique com o valor esperado:

```python
#Increment others
for c in connections:
	c.insert(UPDATE table_name SET num_online = num_online + 1;)

#Wait for others to increment
sync = False
while not sync:
	n = db.query(SELECT num_online FROM table_name)
	if n == n_clients
		sync = True
	else
		sleep(1)
```

Depois desta inicialização temos então alguma garantia que os clientes ficaram sincronizados.

### Ciclo

Durante esta fase o objetivo será de "stressar" o sistema, saturando-o com constantes inserções nas diversas bases de dados de cada client.

```python

wait_time = Seconds_in_a_min / n_inserts_minute

while num_inserts < num_inserted:
	wait_time = wait_time - time_passed_inserting_last_batch

	if wait_time has passed:

		key = sha256(random_number)
		value = random_number

		for client in all_clients:
			insert_in_database(client , key, value)

		collect_analytics()
    

```
**TODO**
  * definir os dados a recolher
  * as inserções nos outros clientes poderão ser em "batches" (conjuntos de tuplos guardados numa tabela auxiliar) ou 
		a inserção nos outros clientes é feita 1 a 1 (este ponto está por definir)

### Finalização

Na fase final do programa, este deve interpretar os dados recolhidos durante a execução (estes ainda estão por definir) de
modo a efetuar uma análise estatística dos mesmos.

nota: a maneira de efetuar a análise estatística dos dados ainda está por definir




