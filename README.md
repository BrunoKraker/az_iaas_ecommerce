# Azure IaaS E-commerce

> Projeto: E-commerce multi-camadas com arquitetura IaaS no Azure

![Azure](https://img.shields.io/badge/Azure-IaaS-blue)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

---

## Sobre o Projeto

O projeto está sendo desenvolvido como parte dos meus estudos em cloud computing e também para colocar em prática conhecimentos obtidos através dos estudos para a certificação AZ-900. Foco em aplicação de conceitos de Infraestrutura como Service (IaaS), alta disponibilidade e organização de recursos em ambiente cloud, não contemplando inicialmente aspectos avançados de frontend ou experiência do usuário.

### Objetivos (planejamento)

- [ ] Implementar arquitetura de 3 camadas (Frontend, Backend, Database)
- [ ] Configurar alta disponibilidade com Load Balancer e Availability Sets
- [ ] Aplicar segurança em camadas com NSG
- [ ] Implementar monitoramento e alertas com Azure Monitor
- [ ] Otimizar custos visando SLA de 99.95%
- [ ] Documentar todo o processo

---

## Diagrama de Infraestrutura (planejamento)

Diagrama da infraestrutura planejada:

![diagrama](diagrams/arquitetura.png)

---

## Componentes (planejamento)

| Camada | Componente | Função | 
| ------ | ---------- | ------ |
| Load Balancing | Azure Load Balancer (Basic SKU) | Distribuir tráfego HTTP/HTTPS
| Computação | 2x VMs Ubuntu B2ts_v2 + Availability Set | Hospedagem da aplicação
| Aplicação | Nginx + Python/Flask | Reverse proxy + API REST
| Database | PostgreSQL 14 | Armazenamento persistente
| Rede | VNet + Subnet + NSG | Isolamento e segurança
| Monitoramento | Azure Monitor + Alertas | Observabilidade

---

## Tecnologias a serem utilizadas

- Cloud: Microsoft Azure (IaaS)
- SO: Ubuntu Server 22.04 LTS
- Web Server: Nginx 1.18+
- Runtime: Python 3.11
- Framework: Flask
- Database: PostgreSQL 14
- Orquestração: Systemd
- Monitoramento: Azure Monitor

---
## Processo de Implementação

### Fases

| Fase | Descrição |
|------|-----------|
| 1 | Fundação (Rede + NSG) |
| 2 | Load Balancer |
| 3 | VMs |
| 4 | Stack (Nginx + Python + PostgreSQL) |
| 5 | Database |
| 6 | Monitoramento |

---

## Estrutura do Repositório

```
az-iaas-ecommerce/
├── README.md                 # Este arquivo
├── docs/                     # Documentação detalhada
├── diagrams/                 # Diagramas de arquitetura
├── screenshots/              # Evidências da implementação
├── scripts/                  # Scripts e configurações
├── infrastructure/           # Futuro IaC
└── costs/                    # Análise de custos
```

---

## Como executar

Espaço que irei preencher após a implementação.

---

## Resultados Esperados

- Aplicação altamente disponível
- Balanceamento de carga funcional
- Monitoramento ativo com alertas
- Arquitetura funcional, documentada e otimizada

---

## Decisões de Arquitetura

Espaço que irei preencher durante a implementação.

---

## Aprendizados

Espaço que irei preencher durante a implementação.

---

## Desafios

Espaço que irei preencher durante a implementação.

---

## Sugestões de Melhoria

Espaço que irei preencher durante a implementação.

---

## Autor

Bruno Kraker

- GitHub: [@bruno-kraker](https://github.com/BrunoKraker)
- LinkedIn: [Bruno Kraker](https://www.linkedin.com/in/brunokraker/)

---

## Status do Projeto

- Fase atual: Planejamento
- Próximo passo: Fase 1 - Fundação (Rede + NSG)
- Última atualização: 23/04/2026