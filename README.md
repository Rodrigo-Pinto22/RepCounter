# RepCounter

Sistema de visão computacional em tempo real para avaliação de movimentos de exercício físico e validação de repetições.

---

## Descrição

O RepCounter é um projeto desenvolvido no âmbito da unidade curricular de Visão Computacional. O sistema utiliza técnicas clássicas de visão computacional em conjunto com o MediaPipe para analisar o movimento de uma pessoa durante a realização de exercícios físicos, determinando automaticamente se cada repetição é válida ou não.

---

## Objetivos

- Detetar e rastrear os membros e articulações do utilizador em tempo real
- Calcular ângulos articulares para avaliar a amplitude do movimento
- Validar repetições com base em critérios biomecânicos definidos
- Fornecer feedback visual em sobreposição (_overlay_) no vídeo em direto
- Comparar abordagem clássica de deteção de esqueleto com o MediaPipe

---

## Exercícios Suportados

| Exercício             | Articulações Analisadas   |
| --------------------- | ------------------------- |
| Flexões (_Push-up_)   | Ombro → Cotovelo → Pulso  |
| Agachamento (_Squat_) | Anca → Joelho → Tornozelo |
| Abdominal (_SitUp_)   | Anca → Ombro → Cabeça     |

---

## Pipeline Técnico

```
Frame da Câmara
      ↓
[#03] Pré-processamento (redução de ruído, normalização de iluminação)
      ↓
[#04] Deteção de Contornos (silhueta corporal com Canny)
      ↓
[#05] Operações Morfológicas (limpeza da máscara corporal)
      ↓
[#06] Rastreamento de Características (fluxo ótico Lucas-Kanade)
      ↓
[MediaPipe] Estimação de Pose (landmarks das articulações)
      ↓
Cálculo de Ângulos → Validação da Repetição
      ↓
Overlay Visual em Tempo Real
```

---

## Estrutura do Projeto

```
repcounter/
├── data/
│   ├── photos/               # Imagens para desenvolvimento do pipeline
│   │   ├── pushup/
│   │   ├── squat/
│   │   └── curl/
│   └── videos/               # Vídeos para teste e validação
│       ├── pushup/
│       ├── squat/
│       └── curl/
├── src/
│   ├── preprocessing/        # #03 - Pré-processamento
│   ├── tracking/             # #06 - Rastreamento + MediaPipe
│   ├── exercise/             # Lógica de ângulos, repetições e validação
│   └── ui/                   # Overlay e feedback visual
├── tests/                    # Testes unitários
├── notebooks/                # Exploração e prototipagem
├── output/                   # Frames e vídeos processados
├── main.py                   # Ponto de entrada
├── config.py                 # Parâmetros e limiares
└── pyproject.toml            # Dependências (geridas com uv)
```

---

## Instalação

### Pré-requisitos

- Python 3.10+
- [uv](https://github.com/astral-sh/uv)

### Passos

```bash
# Clonar o repositório
git clone https://github.com/utilizador/repcounter.git
cd repcounter

# Criar ambiente virtual e instalar dependências
uv venv
source .venv/bin/activate  # Linux/Mac

uv sync
```

---

## Utilização

```bash
# Executar o sistema em tempo real
uv run main.py

# Executar com exercício específico
uv run main.py --exercise pushup

# Explorar notebooks
uv run jupyter notebook
```

---

## Dataset

O dataset foi criado pelos próprios elementos do grupo, com gravações de exercícios em condições controladas, incluindo exemplos de forma correta e incorreta para cada exercício.

---

## 👥 Equipa

| Elemento   | Responsabilidade                                                           |
| ---------- | -------------------------------------------------------------------------- |
| Elemento A | Pipeline de visão computacional (pré-processamento, deteção, rastreamento) |
| Elemento B | Lógica de exercício, contagem de repetições e interface visual             |

---

## Apresentações

| Data          | Conteúdo                                                             |
| ------------- | -------------------------------------------------------------------- |
| 07/05         | Proposta: Problema, Objetivo, Dataset, Metodologia, Solução Prevista |
| Final de Maio | Final: Resultados, Comparação Clássico vs MediaPipe, Demo ao Vivo    |

---

## Tecnologias

- **Python 3.10+**
- **OpenCV** — processamento de imagem e vídeo
- **MediaPipe** — estimação de pose
- **NumPy** — cálculos matriciais e geométricos
- **uv** — gestão de dependências

---

## Licença

Projeto académico desenvolvido para a unidade curricular de Visão Computacional.
