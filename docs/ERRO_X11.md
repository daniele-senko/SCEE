# Solução para Erro X11 no Rocky Linux com XFCE

## Problema

```
X Error of failed request:  BadLength (poly request too large or internal Xlib length error)
  Major opcode of failed request:  139 (RENDER)
  Minor opcode of failed request:  20 (RenderAddGlyphs)
```

Este erro ocorre quando o Tkinter tenta renderizar fontes que causam problemas com o servidor X11.

## Solução para Rocky Linux 9.x com XFCE

### 1. Reinstalar Fontes do Sistema

```bash
# Reinstalar pacotes de fontes
sudo dnf reinstall -y fontconfig dejavu-sans-fonts liberation-fonts

# Limpar e reconstruir cache de fontes
sudo fc-cache -f -v

# Limpar cache local do usuário
rm -rf ~/.cache/fontconfig
rm -rf ~/.fontconfig

# Reconstruir cache do usuário
fc-cache -f -v
```

### 2. Instalar Fontes Adicionais (Opcional)

```bash
# Instalar fontes completas do Google
sudo dnf install -y google-noto-sans-fonts google-noto-serif-fonts

# Instalar fontes bitmap para fallback
sudo dnf install -y xorg-x11-fonts-misc xorg-x11-fonts-Type1

# Reconstruir cache
sudo fc-cache -f -v
```

### 3. Configurar XFCE para Fontes Seguras

```bash
# Abrir configurações de aparência do XFCE
xfce4-appearance-settings &

# Ou via linha de comando, definir fonte padrão
xfconf-query -c xsettings -p /Gtk/FontName -s "DejaVu Sans 10"
```

### 4. Variáveis de Ambiente (Se necessário)

Adicione ao `~/.bashrc` ou `~/.zshrc`:

```bash
# Desabilitar anti-aliasing que pode causar problemas
export GDK_USE_XFT=0

# Forçar uso de fontes core X11
export QT_X11_NO_MITSHM=1
```

Após adicionar, recarregue:
```bash
source ~/.zshrc  # ou ~/.bashrc
```

### 5. Verificar Fontes Disponíveis

```bash
# Listar fontes disponíveis
fc-list | grep -i "dejavu\|liberation\|free"

# Verificar fontes sendo usadas pelo Python
python3 -c "import tkinter; import tkinter.font; root = tkinter.Tk(); print(tkinter.font.families())"
```

### 6. Solução no Código (Já Implementada)

O sistema já usa fontes seguras através da configuração em `src/config/settings.py`:

```python
# Fontes seguras para Linux
FONT_FAMILY = "DejaVu Sans"  # Fonte padrão do Rocky/RHEL
FONT_HEADER = ("DejaVu Sans", 16, "bold")
FONT_BODY = ("DejaVu Sans", 10)
FONT_SMALL = ("DejaVu Sans", 8)
```

## Teste Final

Após aplicar as soluções, teste o aplicativo:

```bash
cd /home/renatoas/PycharmProjects/PythonProject/SCEE
python3 main.py
```

## Troubleshooting Adicional

### Se o erro persistir:

1. **Reiniciar sessão XFCE:**
   ```bash
   xfce4-session-logout
   ```
   E faça login novamente.

2. **Verificar servidor X11:**
   ```bash
   echo $DISPLAY
   xdpyinfo | grep -i render
   ```

3. **Usar fontes bitmap como fallback:**
   ```bash
   sudo dnf install -y xorg-x11-fonts-75dpi xorg-x11-fonts-100dpi
   sudo fc-cache -f -v
   ```

4. **Última opção - Desabilitar RENDER extension:**
   
   Edite `/etc/X11/xorg.conf.d/20-disable-render.conf`:
   ```bash
   sudo nano /etc/X11/xorg.conf.d/20-disable-render.conf
   ```
   
   Adicione:
   ```
   Section "Extensions"
       Option "RENDER" "Disable"
   EndSection
   ```
   
   **Atenção:** Isso pode afetar a aparência de outras aplicações.

## Referências

- [Rocky Linux Documentation](https://docs.rockylinux.org/)
- [XFCE Font Configuration](https://docs.xfce.org/xfce/xfce4-settings/appearance)
- [Tkinter Font Issues on Linux](https://wiki.tcl-lang.org/page/Fonts)
