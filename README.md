# ⚽ Simulador LaLiga EA Sports 2025 (Monte Carlo + ELO)

Este proyecto es un simulador de la temporada final de LaLiga EA Sports 2024/2025.\
Permite estimar, mediante **método Monte Carlo** y **modelo ELO ajustado**, las probabilidades de:

- Ser **campeón de liga** 🏆
- Clasificarse para **Champions League** (2º–5º) 🌟
- Clasificarse para **Europa League** (6º–7º) 🌍
- Clasificarse para **Conference League** (8º) 🏆
- **Descender** a Segunda División (18º–20º) 📉

---

## 📦 Características

- **Interfaz gráfica moderna** usando [`ttkbootstrap`](https://ttkbootstrap.readthedocs.io/).
- **Elección del número de simulaciones** por parte del usuario.
- **Simulación realista** basada en la clasificación actual (tras jornada 33) y un sistema ELO modificado.
- **Visualización completa** de resultados con scroll vertical.
- **Botón para exportar resultados a CSV**.


---

## 🛠️ Tecnologías usadas

- Python 3.10+
- [`ttkbootstrap`](https://github.com/israel-dryer/ttkbootstrap) (Interfaz moderna)
- [`tqdm`](https://github.com/tqdm/tqdm) (Barra de progreso)
- `tkinter` (estándar en Python)

---

## ✨ Mejoras futuras

- Ajustar dinámicamente las probabilidades de empate según diferencia de ELO.
- Hacer un ajuste del ELO más personalizado.
- Implementar modelo de goles Poisson, para tener en cuenta los desempates.

---

## 🧐 Créditos

**Hecho para ver las probabilidades que tiene mi equipo de salvarse.**

