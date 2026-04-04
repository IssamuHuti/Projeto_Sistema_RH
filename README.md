# 📊 Sistema de Gestão de Recursos Humanos (RH)

## 📌 Sobre o Projeto

Este projeto é um sistema de linha de comando desenvolvido em Python para gerenciamento de recursos humanos, utilizando banco de dados SQLite.

O sistema permite o controle de funcionários, cargos, departamentos e o processamento da folha de pagamento mensal.

---

## ⚙️ Funcionalidades

* 📌 Cadastro de Funcionários
* 📌 Cadastro de Cargos
* 📌 Cadastro de Departamentos
* 📌 Listagem de dados cadastrados
* 📌 Processamento da folha de pagamento mensal
* 📌 Cálculo de salário com:

  * Desconto por faltas
  * Desconto de vale transporte
  * Acréscimo por dependentes

---

## 🧮 Regras de Negócio

* Funcionários possuem status (Ativo/Demitido)
* Funcionários com faltas têm desconto proporcional
* Vale transporte desconta 5% do salário
* Dependentes geram acréscimo percentual no salário

---

## 🚧 Melhorias Futuras

* 🔧 Otimização de consultas SQL com JOIN
* 🔧 Implementação da possibilidade de alterar dados cadastrais registradas
* 🔧 Adaptação do projeto a modelo com interface gráfica com Pyside6
* 🔧 Adaptação do projeto a POO
* 🔧 Modularização mais detalhada
* 🔧 Corrigir o erro de permitir cadastrar mais do que a quantidade máxima de funcionários por cargo

---

## 📈 Nova Regra Planejada

Será implementada uma nova regra de cálculo salarial:

* A cada **5 anos de empresa**, o funcionário receberá um **acréscimo de 5% no salário**
* O aumento será **cumulativo**
