
## Objectivos da Aplicação

A aplicação que aqui vai ser desenvolvida tem como objectivo testar a diferença de desempenho de replicação de uma base de dados numa rede containers e numa rede de máquinas virtuais. Para tal vai ser usado o ambiente Docker para a componente dos containers, e software da VMware para as máquinas virtuais.

## Requisitos da Aplicação

A aplicação deve ser independente do ambiente em que será utilizada (containers ou VMs). A mesma será desenvolvida em [Python3](https://www.python.org/download/releases/3.0/), com a base de dados implementada em [MySQL](https://www.mysql.com/). Para fazer pedidos à base de dados será utilizada a API [MySQLdb](http://mysql-python.sourceforge.net/MySQLdb.html) que está disponível como módulo para Python3 nos repositórios do Ubuntu com o nome [python3-mysqldb](https://packages.ubuntu.com/artful/python3-mysqldb).

## Funcionamento da Aplicação

### Início

A aplicação tem como argumentos o número de inserções na base de dados por segundo e o número máximo de inserções, utilizado como condição de paragem.
```bash
user@user-pc$ python3 toyapp.py 
```
