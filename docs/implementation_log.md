# Log de Implementação

Registro cronológico de todas as etapas do projeto.

---

## [23/04/2026] - Início do Projeto

### Ações

- Repositório no GitHub criado
- Estrutura de pastas definida
- README inicial criado
- Diagrama de arquitetura inicial criado

### Próximo Passo

- Fase 1

---

## [24/04/2026] - Fase 1: Fundação (Rede + NSG)

### Ações

- Grupo de recursos (rg-ecommerce-dev) criado no Central US
- VNet criada no Central US (vnet-ecommerce - 10.0.0.0/16)
- Subnet criada dentro da VNet (subnet-vms - 10.0.1.0/24)
- NSG criado, configurado e associado a subnet (nsg-vms-secure) com 4 regras de entrada
- IP público criado para o Load Balancer (pip-loadbalancer - Estático)

### Notas

- Criação dos recursos no Central US para ser possível posteriormente criar VMs com menor custo (Família Bsv2 Standard vCPUs)

### Próximo Passo

- Fase 2

---

## [26/04/2026] - Fase 2: Load Balancer

### Ações

- Load Balancer criado no Central US (lb-ecommerce)
- Configuração do IP público do Load Balancer (frontend - associado ao pip-loadbalancer)
- Criação de pool do backend (backend-vms vazio por enquanto, ou seja, sem VMs)
- Configuração de Health Probe a cada 15 seg (http-probe - HTTP GET / a cada 15s, limite 2)
- Configuração de Regra de Balanceamento (http-rule - TCP/80 frontend --> backend)

### Notas

- Criação de pool backend vazio para posteriormente colocar as VMs que serão criadas lá dentro
- Entendimento de Health Probe (verificar saúde) visando melhor alta disponibilidade da aplicação

### Próximo Passo

- Fase 3

---

## [28/04/2026] - Fase 3: VMs

### Ações

- Criação e configuração de conjunto de disponilidade com 2 domínios de falha e 5 domínios de atualização
- Provisionamento e configuração de 2 VMs no Central US
- Uso de VMs baratas para otimizar custo
- Associação das VMs com o availability set, VNet e Subnet
- Verificação do pool de backend e das VMs no conjunto de disponibilidade
- Criação de IPs públicos temporários
- Teste de conexão com as VMs via SSH (par de chaves)
- Aprendizado de comandos do powershell e do linux

### Notas

- Demorei bastante para entender o permissionamento que envolve os arquivos .pem (chaves SSH)
- Aprendi a configurar o permissionamento
- Possível problema com as regras outbound do NSG
- Testes ping google.com não funcionaram nas VMs
- Devo lembrar de apagar os IPs públicos temporários depois

### Próximo Passo

- Fase 4