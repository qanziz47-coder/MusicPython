import os
import pygame
import time
import random
import math

# ============ KONFIGURASI ============
WIDTH = 1100
HEIGHT = 700
FPS = 60

# Warna
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (180, 180, 180)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 200)
DARK_GRAY = (50, 50, 50)

def load_japanese_font(size):
    """Load font yang support bahasa Jepang"""
    
    # Coba font custom dari folder fonts/
    font_paths = [
        os.path.join("fonts", "NotoSansJP-Regular.ttf"),
        os.path.join("fonts", "NotoSansJP-Bold.ttf"),
        os.path.join("fonts", "meiryo.ttf"),
        os.path.join("fonts", "japanese_font.ttf"),
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                font = pygame.font.Font(path, size)
                # Test render karakter Jepang
                test = font.render("日本語", True, WHITE)
                if test.get_width() > 10:
                    print(f"✅ Font Jepang: {os.path.basename(path)}")
                    return font
            except:
                pass
    
    # Coba font sistem Windows
    system_fonts = ["meiryo", "msgothic", "yugothic", "segoeui", "malgun gothic"]
    
    for font_name in system_fonts:
        try:
            font = pygame.font.SysFont(font_name, size)
            test = font.render("日本語", True, WHITE)
            if test.get_width() > 10:
                print(f"✅ Font sistem: {font_name}")
                return font
        except:
            pass
    
    # Fallback ke font default (akan tampil kotak)
    print("⚠️ Font Jepang tidak ditemukan! Install Noto Sans JP")
    return pygame.font.Font(None, size)

def baca_file_lrc(file_path):
    """Baca file LRC dan pasangkan Jepang dengan Latin"""
    lyrics_data = []
    
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        
        # Skip metadata
        if line.startswith('[ti:') or line.startswith('[ar:') or line.startswith('[al:') or line.startswith('[by:'):
            i += 1
            continue
        
        if line.startswith('[') and ']' in line:
            try:
                end_bracket = line.index(']')
                time_str = line[1:end_bracket]
                text = line[end_bracket+1:].strip()
                
                if text and ':' in time_str:
                    minutes, seconds = time_str.split(':')
                    total_seconds = int(minutes) * 60 + float(seconds)
                    
                    # Cek apakah ini baris Jepang (mengandung karakter Jepang)
                    has_japanese = any('\u4e00' <= c <= '\u9fff' or 
                                       '\u3040' <= c <= '\u309f' or 
                                       '\u30a0' <= c <= '\u30ff' for c in text)
                    
                    # Cek baris berikutnya apakah memiliki timestamp yang sama (berpasangan)
                    next_line = lines[i+1].strip() if i+1 < len(lines) else ""
                    has_pair = False
                    romanji_text = ""
                    
                    if next_line.startswith('[') and ']' in next_line:
                        try:
                            next_end = next_line.index(']')
                            next_time_str = next_line[1:next_end]
                            next_text = next_line[next_end+1:].strip()
                            next_min, next_sec = next_time_str.split(':')
                            next_total = int(next_min) * 60 + float(next_sec)
                            
                            # Jika timestamp sama (beda < 0.1 detik) dan ini adalah pasangan
                            if abs(next_total - total_seconds) < 0.1 and next_text:
                                has_pair = True
                                romanji_text = next_text
                                i += 1  # Skip baris berikutnya
                        except:
                            pass
                    
                    lyrics_data.append({
                        'time': total_seconds,
                        'japanese': text if has_japanese else None,
                        'romanji': romanji_text if has_pair else (text if not has_japanese else None),
                        'has_pair': has_pair
                    })
            except:
                pass
        i += 1
    
    # Gabungkan data yang sama waktunya
    merged_data = []
    i = 0
    while i < len(lyrics_data):
        current = lyrics_data[i]
        if i + 1 < len(lyrics_data) and abs(lyrics_data[i+1]['time'] - current['time']) < 0.1:
            # Gabungkan
            merged_data.append({
                'time': current['time'],
                'japanese': current['japanese'] or lyrics_data[i+1]['japanese'],
                'romanji': current['romanji'] or lyrics_data[i+1]['romanji'],
                'has_pair': True
            })
            i += 2
        else:
            merged_data.append(current)
            i += 1
    
    print(f"   Load {len(merged_data)} baris lirik (berpasangan)")
    return merged_data

def wrap_text(text, font, max_width):
    """Wrap teks panjang"""
    if not text:
        return []
    
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        if font.size(test_line)[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines if lines else [text]

def run_lyrics_display(lyrics_data, lagu_name, file_lagu, artist_name="Official髭男dism"):
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"🎵 {lagu_name} - Official髭男dism")
    clock = pygame.time.Clock()
    
    # Load fonts
    japanese_font = load_japanese_font(38)      # Font untuk Jepang (besar)
    romanji_font = load_japanese_font(24)       # Font untuk Latin (kecil)
    title_font = load_japanese_font(36)
    artist_font = load_japanese_font(22)
    small_font = pygame.font.Font(None, 16)
    
    # Inisialisasi musik
    pygame.mixer.init()
    pygame.mixer.music.load(file_lagu)
    
    # Background gradient
    background = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(20 + t * 30)
        g = int(10 + t * 20)
        b = int(40 + t * 60)
        pygame.draw.line(background, (r, g, b), (0, y), (WIDTH, y))
    
    # Particles
    particles = []
    for _ in range(80):
        particles.append({
            'x': random.randint(0, WIDTH),
            'y': random.randint(0, HEIGHT),
            'speed': random.uniform(0.3, 1.5),
            'size': random.randint(1, 2),
        })
    
    # Status
    running = True
    paused = False
    start_time = time.time()
    current_index = 0
    total_lines = len(lyrics_data) if lyrics_data else 0
    
    # Current display
    current_japanese = ""
    current_romanji = ""
    prev_japanese = ""
    prev_romanji = ""
    next_japanese = ""
    next_romanji = ""
    
    # Animasi
    fade_alpha = 255
    pulse = 0
    
    def update_lyrics_display():
        nonlocal current_japanese, current_romanji, prev_japanese, prev_romanji, next_japanese, next_romanji
        
        if not lyrics_data or current_index == 0:
            return
        
        # Current
        current = lyrics_data[current_index - 1]
        current_japanese = current.get('japanese', '')
        current_romanji = current.get('romanji', '')
        
        # Previous
        if current_index >= 2:
            prev = lyrics_data[current_index - 2]
            prev_japanese = prev.get('japanese', '')
            prev_romanji = prev.get('romanji', '')
        else:
            prev_japanese = ""
            prev_romanji = ""
        
        # Next
        if current_index < total_lines:
            next_lyric = lyrics_data[current_index]
            next_japanese = next_lyric.get('japanese', '')
            next_romanji = next_lyric.get('romanji', '')
        else:
            next_japanese = ""
            next_romanji = ""
    
    print(f"\n🎵 MEMUTAR: {lagu_name}")
    print(f"📝 Total lirik: {total_lines} baris")
    print("=" * 50)
    print("🎮 KONTROL:")
    print("   SPASI = Pause/Play")
    print("   ESC   = Stop")
    print("   →     = Skip 5 detik")
    print("   ←     = Mundur 5 detik")
    print("=" * 50)
    
    # Mulai musik
    pygame.mixer.music.play()
    
    while running:
        current_time = time.time()
        music_time = current_time - start_time
        
        # Handle event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if paused:
                        pygame.mixer.music.unpause()
                        paused = False
                        if lyrics_data and current_index > 0:
                            start_time = time.time() - lyrics_data[current_index-1]['time']
                        else:
                            start_time = time.time()
                    else:
                        pygame.mixer.music.pause()
                        paused = True
                elif event.key == pygame.K_RIGHT:
                    new_time = music_time + 5
                    pygame.mixer.music.set_pos(new_time)
                    start_time = time.time() - new_time
                    # Update current_index
                    if lyrics_data:
                        for i, lyric in enumerate(lyrics_data):
                            if lyric['time'] > new_time:
                                current_index = i
                                update_lyrics_display()
                                break
                elif event.key == pygame.K_LEFT:
                    new_time = max(0, music_time - 5)
                    pygame.mixer.music.set_pos(new_time)
                    start_time = time.time() - new_time
                    if lyrics_data:
                        for i, lyric in enumerate(lyrics_data):
                            if lyric['time'] > new_time:
                                current_index = i
                                update_lyrics_display()
                                break
        
        # Cek lagu selesai
        if not pygame.mixer.music.get_busy() and not paused:
            time.sleep(1)
            running = False
            break
        
        # Update lirik berdasarkan timestamp
        if lyrics_data and not paused and current_index < total_lines:
            next_time = lyrics_data[current_index]['time']
            if music_time >= next_time:
                current_index += 1
                update_lyrics_display()
                pulse = 1.0
        
        # Update animasi pulse
        pulse *= 0.9
        if pulse < 0.05:
            pulse = 0
        
        # ============ GAMBAR ============
        screen.blit(background, (0, 0))
        
        # Particle effect
        for p in particles:
            color = CYAN if p['size'] == 1 else (100, 200, 255)
            pygame.draw.circle(screen, color, (int(p['x']), int(p['y'])), p['size'])
            p['y'] += p['speed']
            if p['y'] > HEIGHT:
                p['y'] = 0
                p['x'] = random.randint(0, WIDTH)
        
        # ============ HEADER ============
        # Garis dekorasi
        line_width = 250 + int(30 * pulse)
        for i in range(2):
            y_pos = 70 + i * 3
            pygame.draw.line(screen, YELLOW, (WIDTH//2 - line_width//2, y_pos), 
                           (WIDTH//2 + line_width//2, y_pos), 2)
        
        # Judul lagu dengan pulse
        title_size = int(36 + 4 * pulse)
        title_font_pulse = load_japanese_font(title_size)
        title_surface = title_font_pulse.render(f"♪ {lagu_name.upper()} ♪", True, GOLD)
        title_rect = title_surface.get_rect(center=(WIDTH//2, 45))
        screen.blit(title_surface, title_rect)
        
        # Artist name
        artist_surface = artist_font.render(artist_name, True, GRAY)
        artist_rect = artist_surface.get_rect(center=(WIDTH//2, 90))
        screen.blit(artist_surface, artist_rect)
        
        # ============ LIRIK SEBELUMNYA ============
        y_prev_start = HEIGHT // 2 - 150
        
        if prev_japanese:
            prev_jp_surface = romanji_font.render(prev_japanese, True, GRAY)
            prev_jp_rect = prev_jp_surface.get_rect(center=(WIDTH//2, y_prev_start))
            screen.blit(prev_jp_surface, prev_jp_rect)
        
        if prev_romanji and prev_romanji != prev_japanese:
            prev_rom_surface = small_font.render(prev_romanji, True, DARK_GRAY)
            prev_rom_rect = prev_rom_surface.get_rect(center=(WIDTH//2, y_prev_start + 25))
            screen.blit(prev_rom_surface, prev_rom_rect)
        
        # ============ LIRIK SAAT INI ============
        # Efek pulse
        current_size = int(38 + 8 * pulse)
        current_font_pulse = load_japanese_font(current_size)
        
        y_current_start = HEIGHT // 2 - 50
        
        if current_japanese:
            # Wrap jika terlalu panjang
            wrapped_jp = wrap_text(current_japanese, current_font_pulse, WIDTH - 150)
            for i, line in enumerate(wrapped_jp):
                jp_surface = current_font_pulse.render(line, True, YELLOW)
                jp_rect = jp_surface.get_rect(center=(WIDTH//2, y_current_start + i * 50))
                screen.blit(jp_surface, jp_rect)
        
        if current_romanji and current_romanji != current_japanese:
            rom_surface = romanji_font.render(current_romanji, True, LIGHT_GRAY)
            rom_rect = rom_surface.get_rect(center=(WIDTH//2, y_current_start + 70))
            screen.blit(rom_surface, rom_rect)
        
        # ============ LIRIK BERIKUTNYA ============
        y_next_start = HEIGHT // 2 + 120
        
        if next_japanese:
            next_jp_surface = romanji_font.render(next_japanese, True, GRAY)
            next_jp_rect = next_jp_surface.get_rect(center=(WIDTH//2, y_next_start))
            screen.blit(next_jp_surface, next_jp_rect)
        
        if next_romanji and next_romanji != next_japanese:
            next_rom_surface = small_font.render(next_romanji, True, DARK_GRAY)
            next_rom_rect = next_rom_surface.get_rect(center=(WIDTH//2, y_next_start + 25))
            screen.blit(next_rom_surface, next_rom_rect)
        
        # ============ PROGRESS BAR ============
        if lyrics_data and total_lines > 0:
            progress = current_index / total_lines
            bar_w = WIDTH - 200
            bar_h = 4
            bar_x = 100
            bar_y = HEIGHT - 60
            
            pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_w, bar_h))
            pygame.draw.rect(screen, YELLOW, (bar_x, bar_y, int(bar_w * progress), bar_h))
            
            circle_x = bar_x + int(bar_w * progress)
            circle_radius = int(6 + 3 * pulse)
            pygame.draw.circle(screen, YELLOW, (circle_x, bar_y + bar_h//2), circle_radius)
        
        # ============ INFO ============
        current_min = int(music_time // 60)
        current_sec = int(music_time % 60)
        
        status_text = "▶️ PLAYING" if not paused else "⏸️ PAUSED"
        status_color = YELLOW if not paused else GRAY
        status_surface = small_font.render(f"{status_text}  |  {current_min:02d}:{current_sec:02d}", True, status_color)
        screen.blit(status_surface, (20, HEIGHT - 30))
        
        if lyrics_data:
            info_surface = small_font.render(f"Lyrics: {current_index}/{total_lines}", True, (80, 80, 80))
            screen.blit(info_surface, (WIDTH - 150, HEIGHT - 30))
        
        help_surface = small_font.render("SPACE=Pause  ESC=Stop  ◀/▶=Skip 5s", True, (60, 60, 80))
        screen.blit(help_surface, (WIDTH//2 - 160, HEIGHT - 30))
        
        # ============ FADE IN ============
        if fade_alpha > 0:
            fade_surface = pygame.Surface((WIDTH, HEIGHT))
            fade_surface.fill(BLACK)
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))
            fade_alpha -= 5
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.mixer.music.stop()
    pygame.quit()
    print("\n🎵 Lagu selesai")

# ============ PROGRAM UTAMA ============
def main():
    print("=" * 60)
    print("     🎤 SOULSOUP - DUAL LYRIC PLAYER 🎤")
    print("=" * 60)
    print("\n✨ FITUR:")
    print("   • Lirik JEPANG (besar, kuning)")
    print("   • Lirik ROMAJI/LATIN (kecil, abu-abu)")
    print("   • Muncul BERPASANGAN (dua baris sekaligus)")
    print("   • Animasi pulse saat ganti lirik")
    print("=" * 60)
    
    # Path file
    base_path = "C:/Users/zankx/OneDrive/Desktop/vscode/soulsoup"
    music_file = f"{base_path}/music/soulsoup.mp3"
    lyrics_file = f"{base_path}/lyrics/soulsoup.lrc"
    
    # Cek file musik
    if not os.path.exists(music_file):
        print(f"\n❌ File musik tidak ditemukan!")
        print(f"   Letakkan soulsoup.mp3 di: {base_path}/music/")
        input("\nTekan Enter untuk keluar...")
        return
    
    # Baca lirik
    if not os.path.exists(lyrics_file):
        print(f"\n❌ File lirik tidak ditemukan!")
        print(f"   Letakkan soulsoup.lrc di: {base_path}/lyrics/")
        input("\nTekan Enter untuk keluar...")
        return
    
    print(f"\n📂 Membaca file lirik...")
    lyrics_data = baca_file_lrc(lyrics_file)
    
    if not lyrics_data:
        print("\n❌ Tidak ada lirik yang valid!")
        input("\nTekan Enter untuk keluar...")
        return
    
    # Preview
    print(f"\n📝 Preview lirik pertama:")
    first = lyrics_data[0]
    if first.get('japanese'):
        print(f"   🇯🇵 {first['japanese'][:50]}...")
    if first.get('romanji'):
        print(f"   🔤 {first['romanji'][:50]}...")
    
    # Jalankan
    run_lyrics_display(lyrics_data, "SoulSoup", music_file, "Official髭男dism")
    
    print("\n👋 Terima kasih!")

if __name__ == "__main__":
    main()