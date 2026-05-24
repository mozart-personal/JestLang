# JestLang

JestLang é uma linguagem de programação moderna, interpretada e open source criada com foco em simplicidade, produtividade e desenvolvimento backend.

A linguagem foi desenvolvida em Python e possui arquitetura própria, incluindo lexer, parser, AST, interpretador, runtime e sistema de execução customizado.

O objetivo da JestLang é oferecer uma experiência de programação mais limpa, rápida e natural, removendo complexidade desnecessária sem perder flexibilidade e poder de desenvolvimento.

---

# O Que é a JestLang

A JestLang é uma linguagem criada para ser:

* simples
* rápida
* moderna
* fácil de aprender
* produtiva
* focada em backend
* ótima para APIs
* agradável de programar

A linguagem busca permitir que qualquer pessoa consiga aprender programação de forma mais natural.

---

# Filosofia da Linguagem

A JestLang prioriza:

* sintaxe limpa
* menos boilerplate
* código legível
* produtividade
* experiência do desenvolvedor
* desenvolvimento rápido
* simplicidade

Inspirada principalmente por:

* Python
* Lua
* JavaScript
* Go

---

# Arquitetura

Toda a linguagem foi construída manualmente sem utilizar geradores externos.

A linguagem possui:

* Lexer próprio
* Parser próprio
* AST própria
* Interpretador próprio
* Runtime customizado
* Sistema de imports
* Sistema HTTP nativo
* CLI própria
* Extensão VSCode
* Suporte GitHub Linguist
* Arquivos `.jest`

---

# Instalação

## Clonando o Projeto

```bash
git clone https://github.com/ByteMajesty/JestLang.git
```

## Entrando na Pasta

```bash
cd JestLang
```

## Instalando Dependências

```bash
pip install flask
```

## Instalando a CLI Global

```bash
pip install -e .
```

---

# Executando Arquivos

A JestLang executa arquivos `.jest`.

## Executando com o comando global

```bash
jest arquivo.jest
```

Exemplo:

```bash
jest api.jest
```

## Executando diretamente com Python

```bash
python main.py arquivo.jest
```

Exemplo:

```bash
python main.py api.jest
```

---

# Seu Primeiro Programa

Crie um arquivo chamado:

```txt
main.jest
```

Adicione:

```jest
print("Olá Mundo")
```

Execute:

```bash
jest main.jest
```

Resultado:

```txt
Olá Mundo
```

---

# Aprendendo JestLang do Zero

# Variáveis

Variáveis armazenam informações.

## Exemplo

```jest
name = "Lucas"
age = 19
```

Agora:

* `name` guarda texto
* `age` guarda número

---

# Strings

Strings são textos.

```jest
message = "Hello World"
```

---

# Números

```jest
number = 10
price = 99.99
```

A linguagem suporta:

* inteiros
* decimais

---

# Booleanos

Booleanos representam verdadeiro ou falso.

```jest
online = true
admin = false
```

---

# Imprimindo Valores

Use `print()`.

```jest
name = "Lucas"

print(name)
```

---

# Arrays

Arrays armazenam múltiplos valores.

```jest
languages = [
    "JestLang",
    "Python",
    "Go"
]
```

---

# Objetos

Objetos armazenam dados organizados por propriedades.

```jest
user = {
    name: "Lucas",
    age: 19,
    language: "JestLang"
}
```

---

# Acessando Dados

```jest
print(user.name)
```

---

# Funções

Funções servem para reutilizar código.

```jest
fn greet(name):
    print("Hello")
    print(name)

greet("Lucas")
```

---

# Retorno de Funções

```jest
fn add(a, b):
    return a + b

result = add(10, 20)

print(result)
```

---

# Condicionais

Condicionais executam código dependendo de uma condição.

```jest
age = 18

if age >= 18:
    print("Adult")
else:
    print("Minor")
```

---

# Operadores Matemáticos

```jest
+
-
*
/
%
```

## Exemplo

```jest
result = 10 + 5

print(result)
```

---

# Operadores de Comparação

```jest
==
!=
>
<
>=
<=
```

## Exemplo

```jest
if age >= 18:
    print("Adult")
```

---

# Operadores Lógicos

```jest
and
or
not
```

---

# Loops

Loops repetem código automaticamente.

# While

```jest
count = 0

while count < 5:
    print(count)
    count = count + 1
```

---

# For

```jest
numbers = [1, 2, 3]

for n in numbers:
    print(n)
```

---

# Comentários

Comentários são ignorados pela linguagem.

```jest
# Isto é um comentário
```

---

# Imports

A linguagem possui sistema de imports próprio.

```jest
use web
```

---

# APIs HTTP

A JestLang possui runtime HTTP nativo baseado em Flask.

---

# Criando Uma API

```jest
use web

app = web

fn home():
    return {
        message: "JestLang Online",
        status: "running"
    }

app.get("/", home)

app.run(3000)
```

---

# Executando a API

Salve como:

```txt
api.jest
```

Execute:

```bash
jest api.jest
```

Resultado:

```txt
Running on http://127.0.0.1:3000
```

---

# Rotas Dinâmicas

```jest
fn user():
    return {
        id: params.id,
        name: "Lucas"
    }

app.get("/users/:id", user)
```

---

# Recursos Atuais

Atualmente a linguagem possui:

* Variáveis
* Funções
* Condicionais
* Loops
* Arrays
* Objetos
* Imports
* Runtime customizado
* APIs HTTP
* Execução via terminal
* Comando global `jest`
* Tipagem dinâmica
* Syntax Highlight
* Snippets VSCode
* Reconhecimento `.jest`

---

# VSCode

A JestLang possui extensão oficial para VSCode com:

* Syntax Highlight
* Snippets
* Reconhecimento `.jest`
* Ícones personalizados
* Auto indentação
* Auto closing pairs

---

# GitHub Linguist

A linguagem possui integração com GitHub Linguist para reconhecimento oficial da extensão `.jest`.

Isso permite:

* Syntax Highlight no GitHub
* Linguagem reconhecida automaticamente
* Estatísticas da linguagem no repositório
* Cor própria da linguagem

---

# Roadmap

Próximos recursos planejados:

* Máquina virtual própria
* Bytecode
* Compilador
* Async/Await
* Sistema de classes
* Package Manager
* Melhor sistema de erros
* LSP
* Formatter
* Debugger
* JIT Compiler
* Garbage Collector
* Banco de dados nativo
* Sistema de módulos avançado

---

# Objetivo do Projeto

O objetivo da JestLang é evoluir para um ecossistema completo de desenvolvimento moderno focado em backend, APIs, automações e produtividade.

A linguagem busca entregar simplicidade sem limitar o desenvolvedor.

---

# Licença

MIT License

