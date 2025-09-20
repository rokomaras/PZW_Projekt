# PZW Grafički Dizajn - Blog Aplikacija

Web aplikacija za blog o grafičkom dizajnu razvijena u Flask framework-u. Aplikacija omogućuje korisnicima objavljivanje članaka, komentiranje, upravljanje profilima i administraciju sadržaja.

## ✨ Funkcionalnosti

- **Korisničke račune**: Registracija, prijava i upravljanje profilima
- **Blog sustav**: Stvaranje, uređivanje i brisanje članaka s Markdown podrškom
- **Komentari**: Komentiranje objava s autentifikacijom
- **Slike**: Upload i prikaz slika pomoću GridFS
- **Označavanje**: Dodjeljivanje oznaka (tagova) člancima
- **Teme**: Različite Bootstrap teme za personalizaciju
- **Admin panel**: Administracija korisnika i sadržaja
- **Responzivni dizajn**: Prilagođen svim uređajima

## 🛠️ Tehnologije

- **Backend**: Flask (Python)
- **Baza podataka**: MongoDB
- **Frontend**: Bootstrap 5, HTML/CSS/JavaScript
- **Autentifikacija**: Flask-Login
- **Forme**: Flask-WTF
- **Stiliziranje**: Bootstrap + custom CSS

## 📋 Preduvjeti

- Python 3.7+
- MongoDB server
- pip (Python package manager)

## 🚀 Instalacija

1. **Kloniraj repozitorij**
   ```bash
   git clone https://github.com/rokomaras/PZW_Projekt.git
   cd PZW_Projekt/PZW_Projket
   ```

2. **Stvori virtualno okruženje**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Na Windows: venv\Scripts\activate
   ```

3. **Instaliraj ovisnosti**
   ```bash
   pip install -r requirements.txt
   ```

4. **Pokreni MongoDB**
   
   Uvjeri se da je MongoDB server pokrenut na `localhost:27017`

5. **Postavi environment varijable (opcionalno)**
   
   Stvori `.env` file u root direktoriju:
   ```
   SECRET_KEY=tvoj_tajni_kljuc_ovdje
   ```

## ▶️ Pokretanje

```bash
python app.py
```

Aplikacija će biti dostupna na `http://localhost:5000`

## 📁 Struktura projekta

```
PZW_Projket/
├── app.py              # Glavna Flask aplikacija
├── forms.py            # WTF forme za korisničke unose
├── requirements.txt    # Python ovisnosti
├── static/            # Statični files (CSS, JS, slike)
│   └── css/
├── templates/         # HTML template-i
│   ├── base.html      # Osnovni template
│   ├── index.html     # Početna stranica
│   ├── login.html     # Prijava
│   ├── register.html  # Registracija
│   ├── profile.html   # Korisnički profil
│   ├── blog_edit.html # Uređivanje članaka
│   ├── blog_view.html # Prikaz članka
│   └── ...
└── .env              # Environment varijable (opcionalno)
```

## 👤 Korištenje

### Za obične korisnike:
1. Registriraj se na `/register`
2. Prijavi se na `/login`
3. Stvori novi članak na `/blog/create`
4. Upravljaj svojim profilom na `/profile`

### Za administratore:
- Pristup popisu korisnika na `/users`
- Uređivanje i brisanje svih objava
- Upravljanje korisničkim računima

## 🎨 Teme

Aplikacija podržava više Bootstrap tema:
- Cerulean, Cosmo, Cyborg, Darkly, Flatly
- Journal, Litera, Lumen, Lux, Materia
- Minty, Morph, Pulse, Quartz, Sandstone
- Simplex, Sketchy, Slate, Solar, Spacelab
- Superhero, United, Vapor, Yeti, Zephyr

## 🔧 Konfiguracija

### Baza podataka
Aplikacija koristi MongoDB s bazom `pzw_blog_database` i kolekcijama:
- `posts` - članci
- `users` - korisnici  
- `comments` - komentari
- `fs.files` i `fs.chunks` - GridFS za slike

### Environment varijable
- `SECRET_KEY` - tajni ključ za Flask sesije (zadano: 'tajni_kljuc')

## 🤝 Doprinos

1. Fork repozitorij
2. Stvori feature branch (`git checkout -b feature/nova-funkcionalnost`)
3. Commit promjene (`git commit -am 'Dodaj novu funkcionalnost'`)
4. Push na branch (`git push origin feature/nova-funkcionalnost`)
5. Stvori Pull Request

## 📄 Licencija

Projekt je dostupan pod MIT licenciju.

## 📞 Kontakt

Za pitanja i podršku, molimo kontaktirajte autore projekta.

---

*Izrađeno s ❤️ za PZW Grafički Dizajn*