"""
AudioManager - Gerenciador de Música de Fundo
==============================================

Gerencia a reprodução de música ambiente no sistema.
"""
import os
from typing import Optional


class AudioManager:
    """
    Gerenciador de música de fundo para o sistema.
    Usa pygame.mixer para reprodução de áudio.
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pattern - apenas uma instância."""
        if cls._instance is None:
            cls._instance = super(AudioManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa o gerenciador de áudio."""
        if not AudioManager._initialized:
            self.enabled = True
            self.volume = 0.3  # Volume padrão (30%)
            self.music_file = None
            self.pygame_available = False
            
            try:
                import pygame.mixer as mixer
                mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                self.mixer = mixer
                self.pygame_available = True
                print("✓ AudioManager inicializado com sucesso")
            except ImportError:
                print("⚠ pygame não disponível - música desabilitada")
                self.enabled = False
            except Exception as e:
                print(f"⚠ Erro ao inicializar áudio: {e}")
                self.enabled = False
            
            AudioManager._initialized = True
    
    def set_music(self, music_file: str) -> bool:
        """
        Define o arquivo de música a ser reproduzido.
        
        Args:
            music_file: Caminho completo para o arquivo de música
            
        Returns:
            True se carregou com sucesso, False caso contrário
        """
        if not self.enabled or not self.pygame_available:
            return False
        
        if not os.path.exists(music_file):
            print(f"⚠ Arquivo de música não encontrado: {music_file}")
            return False
        
        try:
            self.mixer.music.load(music_file)
            self.music_file = music_file
            print(f"✓ Música carregada: {os.path.basename(music_file)}")
            return True
        except Exception as e:
            print(f"✗ Erro ao carregar música: {e}")
            return False
    
    def play(self, loops: int = -1) -> bool:
        """
        Inicia a reprodução da música.
        
        Args:
            loops: Número de repetições (-1 = infinito)
            
        Returns:
            True se iniciou com sucesso, False caso contrário
        """
        if not self.enabled or not self.pygame_available or not self.music_file:
            return False
        
        try:
            self.mixer.music.set_volume(self.volume)
            self.mixer.music.play(loops=loops)
            print(f"♪ Música iniciada (volume: {int(self.volume * 100)}%)")
            return True
        except Exception as e:
            print(f"✗ Erro ao reproduzir música: {e}")
            return False
    
    def stop(self) -> None:
        """Para a reprodução da música."""
        if self.enabled and self.pygame_available:
            try:
                self.mixer.music.stop()
                print("■ Música parada")
            except:
                pass
    
    def pause(self) -> None:
        """Pausa a reprodução da música."""
        if self.enabled and self.pygame_available:
            try:
                self.mixer.music.pause()
                print("⏸ Música pausada")
            except:
                pass
    
    def unpause(self) -> None:
        """Resume a reprodução da música."""
        if self.enabled and self.pygame_available:
            try:
                self.mixer.music.unpause()
                print("▶ Música retomada")
            except:
                pass
    
    def set_volume(self, volume: float) -> None:
        """
        Define o volume da música.
        
        Args:
            volume: Volume de 0.0 a 1.0
        """
        if not self.enabled or not self.pygame_available:
            return
        
        self.volume = max(0.0, min(1.0, volume))
        try:
            self.mixer.music.set_volume(self.volume)
            print(f"🔊 Volume ajustado: {int(self.volume * 100)}%")
        except:
            pass
    
    def toggle(self) -> bool:
        """
        Alterna entre tocar/pausar.
        
        Returns:
            True se está tocando, False se pausado
        """
        if not self.enabled or not self.pygame_available:
            return False
        
        try:
            if self.mixer.music.get_busy():
                self.pause()
                return False
            else:
                self.unpause()
                return True
        except:
            return False
    
    def is_playing(self) -> bool:
        """
        Verifica se a música está tocando.
        
        Returns:
            True se está tocando, False caso contrário
        """
        if not self.enabled or not self.pygame_available:
            return False
        
        try:
            return self.mixer.music.get_busy()
        except:
            return False
    
    def fadeout(self, duration_ms: int = 1000) -> None:
        """
        Para a música com fade out.
        
        Args:
            duration_ms: Duração do fade em milissegundos
        """
        if self.enabled and self.pygame_available:
            try:
                self.mixer.music.fadeout(duration_ms)
            except:
                pass


# Instância global
audio_manager = AudioManager()
