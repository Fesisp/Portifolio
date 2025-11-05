Desafio: Resumo da aula dos beneficios do laboratório em nuvem

Aula em questão tratando sobre a criação de uma Máquina Virtual no Azure Algumas imagens no Azure Computação em nuvem Este projeto faz parte do desafio de projeto da DIO e tem como objetivo demonstrar os conhecimentos adquiridos no curso de Máquinas Virtuais da Azure. O projeto consiste em criar, configurar e documentar uma máquina virtual no Azure, explorando os principais recursos e funcionalidades da plataforma. E para criar a máquina virtual, foi executando os seguintes passos:

Acesse o Portal da Azure: Faça login em Portal Azure.

Crie um Grupo de Recursos: Crie um novo grupo de recursos para organizar os recursos da sua VM.

Crie a Máquina Virtual:

Selecione "Criar um recurso" e busque por "Máquina Virtual".

Preencha os detalhes da VM, como nome, região, imagem do sistema operacional, tamanho, etc.

Configure a rede, criando uma nova VNet ou utilizando uma existente.

Configure as regras de entrada no NSG para liberar as portas necessárias (ex: porta 80 para HTTP e porta 22 para SSH).

Acesse a Máquina Virtual:

Após a criação da VM, acesse-a via SSH (para Linux) ou RDP (para Windows).

Se for do interesse Instale:

Um Servidor web, como o NGINX ou Apache, para testar a conectividade.

