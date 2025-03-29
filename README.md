# Cuidando Huellas

## 🐾 Descripción del Proyecto

**Cuidando Huellas** es una aplicación destinada a la localización de mascotas perdidas y la promoción de la adopción responsable. Permite el registro de mascotas, reportes de pérdida, un catálogo de adopciones, una red colaborativa y notificaciones en tiempo real, **La aplicación está disponible para todo el público, permitiendo que cualquier persona pueda unirse y contribuir a la causa.**
 
## 1️⃣ 🚀 Objetivo del Proyecto

- Reducir la cantidad de mascotas extraviadas mediante alertas en tiempo real.  
- Conectar a dueños con personas que hayan encontrado a su mascota.  
- Fomentar la adopción responsable de animales sin hogar.  
- Crear una comunidad colaborativa de rescate y ayuda animal.

## 🚀 Cómo Funciona

1. **Registro de Mascotas Perdidas:** Los dueños pueden ingresar información sobre su mascota y la última ubicación donde fue vista.    
2. **Búsqueda y Reporte:** Las personas que encuentran mascotas pueden reportarlas en la plataforma.  
3. **Adopciones:** Los refugios y usuarios pueden publicar mascotas disponibles para adopción.  
4. **Comunidad y Red de Ayuda:** Los usuarios pueden interactuar y compartir información relevante. 




### Mantener la rama main actualizada (antes de trabajar)

1. Cambiar a la rama `main`:
   ```bash
   git checkout main
   ```

2. Actualizar la rama `main`:
   ```bash
   git pull origin main
   ```

### Integrar los últimos cambios de main a tu rama de trabajo

3. Cambiar a tu rama de trabajo:
   ```bash
   git checkout yoiner
   # O el nombre de la rama en la que trabajes.
   ```

4. Obtener los últimos cambios de la rama `main` y fusionarlos con `merge`:
   ```bash
   git merge main
   # O usar rebase si prefieres:
   # git rebase main
  
  >[!NOTE]
  >La diferencia entre merge y rebase es que merge crea un nuevo commit de fusión, mientras que rebase aplica tus cambios sobre los cambios de la rama main, creando un historial más limpio.


5. Realizar cambios, añadir y confirmar:
   ```bash
   git add .
   git commit -m "Descripción de los cambios"
   git tag -a v1.1.0-alpha.1 -m "v1.1.0-alpha.1"
   ```

6. Subir los cambios a la rama remota:
   ```bash
   git push -u origin yoiner --tags
   # O el nombre de la rama en la que trabajes.
   ```
Recuerda resolver cualquier conflicto que pueda surgir durante el merge o rebase.