# JobsOptimizer 🚀

Plataforma inteligente para agregar, filtrar y optimizar la búsqueda de ofertas de trabajo en tecnología.
Actualmente en versión MVP (Producto Mínimo Viable).

## 🛠️ Tecnologías

**Backend (El Cerebro):**
* **Python** & **FastAPI** (API REST rápida y moderna).
* **PostgreSQL** (Base de datos relacional).
* **SQLAlchemy 2.0** & **Alembic** (ORM y Migraciones).
* **BeautifulSoup4** (Scraping de datos).

**Frontend (La Cara):**
* **Next.js 14** (App Router).
* **TypeScript** (Seguridad de tipos).
* **Tailwind CSS** (Estilos modernos).
* **Lucide React** (Íconos).

---

## ⚙️ Configuración del Entorno

### 1. Base de Datos
Asegúrate de tener PostgreSQL corriendo y una base de datos llamada `jobs_optimizer`.

### 2. Backend
```bash
cd backend
# Activar entorno virtual (Windows)
..\venv\Scripts\Activate

# Instalar dependencias (si es la primera vez)
pip install -r requirements.txt

# Ejecutar servidor
uvicorn main:app --reload


La API correrá en: http://127.0.0.1:8000

3. Frontend

cd frontend
# Instalar dependencias (si es la primera vez)
npm install

# Ejecutar servidor de desarrollo
npm run dev
La Web correrá en: http://localhost:3000

🗺️ Estado del Proyecto
[x] Arquitectura base (Backend + Frontend).

[x] Scraper funcional (Python.org).

[x] Base de datos conectada.

[x] Interfaz de usuario (UI) con tarjetas de empleo.

[ ] Scraper avanzado (LinkedIn/Glassdoor).

[ ] Filtros de búsqueda.

---

### Paso 2: Subirlo a la rama `dev` 🌿

Ahora vamos a guardar esto **solo en tu rama de desarrollo**.

1.  Abre la terminal en VS Code.
2.  Confirma que estás en la rama correcta (debe decir `dev` abajo a la izquierda, o escribe `git status` y verás "On branch dev").
3.  Ejecuta estos comandos:

```powershell

