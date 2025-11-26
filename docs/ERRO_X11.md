# ⚠️ Erro: Aplicação GUI sem Display Gráfico

## Problema

Você está tentando executar uma aplicação **GUI (Tkinter)** em um ambiente **sem interface gráfica** (headless server/SSH sem X11).

```
X Error of failed request: BadLength
```

## Por que isso acontece?

- SCEE é uma aplicação **desktop** com Tkinter
- Tkinter requer um **servidor X11** (display gráfico)
- Servidores SSH/headless **não têm display** por padrão

## ✅ Soluções

### 1️⃣ Executar em Máquina com Desktop (Recomendado)

Execute em uma máquina com interface gráfica (Linux Desktop, Windows, macOS):

```bash
# Em sua máquina local com desktop
git clone https://github.com/daniele-senko/SCEE.git
cd SCEE
./run.sh
```

### 2️⃣ Usar SSH com X11 Forwarding

Se precisar executar remotamente via SSH:

```bash
# No servidor, garantir que X11Forwarding está habilitado
# /etc/ssh/sshd_config:
# X11Forwarding yes
# X11UseLocalhost no

# Conectar com X11 forwarding
ssh -X usuario@servidor

# Ou com compressão (mais rápido)
ssh -XC usuario@servidor

# Verificar se DISPLAY está configurado
echo $DISPLAY  # Deve mostrar algo como localhost:10.0

# Executar aplicação
cd SCEE
python main.py
```

### 3️⃣ Usar VNC (Desktop Remoto)

Instalar e usar VNC para ter desktop remoto completo:

```bash
# No servidor
sudo dnf install tigervnc-server

# Configurar VNC
vncserver :1 -geometry 1920x1080 -depth 24

# Conectar via cliente VNC
# vnc://servidor:5901
```

### 4️⃣ Usar Xvfb (Virtual Display) - Apenas para Testes

**Não recomendado para uso normal** (você não verá a interface):

```bash
# Instalar Xvfb
sudo dnf install xorg-x11-server-Xvfb

# Executar com display virtual
Xvfb :99 -screen 0 1024x768x24 &
export DISPLAY=:99
python main.py
```

## 🔄 Alternativas ao Tkinter

Se você precisa executar em servidor sem GUI, considere:

### Opção A: Interface Web (Flask/FastAPI)

```python
# Converter para aplicação web
# Usuários acessam via navegador: http://servidor:5000
```

### Opção B: Interface CLI (Command Line)

```python
# Criar interface de linha de comando
# Usuários interagem via terminal
```

### Opção C: API REST

```python
# Backend puro com FastAPI
# Frontend separado (React, Vue, etc.)
```

## 📊 Verificar Ambiente

```bash
# Verificar se há display
echo $DISPLAY

# Testar X11
xeyes  # Se abrir, X11 funciona

# Verificar SSH
echo $SSH_CLIENT
echo $SSH_CONNECTION

# Verificar Tkinter
python -c "import tkinter; tkinter.Tk()"
```

## 🎯 Para Este Projeto (SCEE)

**Escolha:**

1. **Desktop Local**: Execute `./run.sh` em máquina com GUI
2. **SSH + X11**: Use `ssh -X` para executar remotamente
3. **VNC**: Configure desktop remoto completo

**Não Recomendado:**
- Executar em servidor headless sem X11
- Usar Xvfb (não verá interface)

## 📝 Nota

O SCEE foi desenvolvido como aplicação **desktop** para ambientes com interface gráfica. Se você precisa de uma versão **web** ou **CLI**, seria necessário refatorar a camada de apresentação mantendo a lógica de negócio.

---

**Para execução imediata**: Use uma máquina com desktop ou `ssh -X` 🖥️
