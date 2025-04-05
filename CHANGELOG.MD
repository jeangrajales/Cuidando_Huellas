> [!TIP]
> Cómo llenar el CHANGELOG
> El CHANGELOG.md debe registrar los cambios realizados en el proyecto de forma clara y estructurada. Usa este formato para mantener el orden:
> ## [Versión] - Fecha
> ### Added
> - Descripción de nuevas funcionalidades o recursos añadidos.
> ### Fixed
> - Descripción de errores solucionados.
> ### Changed
> - Descripción de cambios en funcionalidades existentes.
> ### Removed
> - Descripción de funcionalidades o recursos eliminados.
> ### Note
> - Notas adicionales sobre los cambios realizados.

---

### CHANGELOG

---

## [ch1.15.11-Alpha.1] - 2025-04-04

## Fixed

- Se ajustaron y organizaron los diseños predeterminados de varias páginas que presentaban desorden en su estructura.
- Se mejoró la lógica del inicio de sesión para restringir correctamente el acceso a determinadas secciones.

---
## [ch1.15.10-Alpha.1] - 2025-04-04

## Fixed

-Se corrigio algunas tarjetas, se implemento un diseño mas claro para el usuario.

---
## [ch1.15.9-Alpha.1] - 2025-04-03

## Added

- Se agrego la carpeta `veterinarias_asoviadas`

## Fixed

-Se corrigio algunas imagenes que no tenian nada que ver con lo planeado en `Nuestro_servicios`.

---

## [ch1.14.8-Alpha.1] - 2025-04-03

## Added

- Se agrego funcionalidad cuando el usuario ya esta registrado no puede acceder a cierta paginas

## Fixed

- Se corrigio error de espacios en el header de pagina_usuario

---

## [ch1.13.7-Alpha.1] - 2025-04-03

## Added

- Se agrego la pagina adopciones

- Se modifico el diseño de las paginas productos_usuarios y mascotas_perdidas

---

## [ch1.12.7-Alpha.1] - 2025-04-03

## Added

- Se ha agregado la funcionalidad que redirige a las páginas correspondientes tanto a administradores como a usuarios registrados al iniciar sesión.

---
## [ch1.11.7-Alpha.1] - 2025-04-01

## Added

- Se agrego pagina producto_compra

---

## [ch1.10.7-Alpha.1] - 2025-04-01

## Fixed

- Se corrigio el formulario de listar usuarios

---

## [ch1.10.6-Alpha.1] - 2025-04-01

## Added

- Se agregó la página productos_usuarios.html junto con su archivo de estilos CSS.

- Se agregó la página mascotas_perdidas.html junto con su archivo de estilos CSS.

- Se agregó la página pagina_usuarios.html junto con su archivo de estilos CSS.

---

## [ch1.9.6-Alpha.1] - 2025-04-01

## Added

- Se Implemento la funcionalidad para eliminar productos
- Se Implemento la Funcionalidad para editar productos

## Fixed

- Se soluciono problema que habia con los campos `Categoria, Estados`

---

### Note

- Quedar por traer los datos de los productos existente al editar un producto

## [ch1.8.5-Alpha.1] - 2025-03-31

## Added 

- Se creó el modelo Producto.
- Se implementó la funcionalidad para listar productos con su respectiva foto.

## Fixed

- Se soluciono problema que habia con el campo telefono de la tabla Usuarios

---

## [ch1.7.5-Alpha.1] - 2025-03-31

## Added

- Se creó la página de `Quiénes_somos` con su vista y plantilla en Django.
- Se agrego imagenes correspondientes adecuadas para los modulos.

### Removed
- Se corrigio el apartado de los botones y solo se dejo en la `pagina principal`.
---
## [ch1.6.4-Alpha.1] - 2025-03-31

## Added

- Se añadido la funcionalidad de enviar correos desde la pagina contactanos
- Se añadio nuevo archivo `forms.py`

---
## [ch1.5.4-Alpha.1] - 2025-03-30

## Added

- Se implementó la página principal para el administrador junto con su hoja de estilos (CSS).

- Se organizó la estructura del proyecto creando, en la carpeta Templates, una subcarpeta denominada Administrador que alberga los archivos correspondientes a los usuarios.

- Se estableció la estructura en Static mediante la creación de la carpeta Administrador/Css para los archivos de estilos.

- Se añadió la funcionalidad para mostrar todos los usuarios.

---

## [ch1.4.4-Alpha.1] - 2025-03-30


## Added

- Se añadio una imagen de fondo para las paginas `Pagina_principal, Nuestro_servicios, Contactos`.
- Se implementó una condición para mostrar el fondo solo en páginas específicas.

## Fixed

- Se corrigió el fondo de la página de Contactos, ajustando los colores de los iconos y la transparencia.
- Se mejoró la adaptación responsiva de la página de Contactos.
- Se optimizó el espaciado en la versión responsiva del menú `(Mascotas Perdidas, Productos, Servicios, Veterinaria Asociada)`.
- Se actualizó la URL de la página Contactos.

---
 
## [ch1.3.3-Alpha.1] - 2025-03-29

## Added
- Implementación inicial del formulario de contacto con campos básicos.
- Inclusión de Bootstrap para mejorar el diseño y la accesibilidad.

## Fixed
- Se corrigió la alineación de los íconos con la información de contacto (ubicación, teléfono y correo).

### Note
- Queda pendiente mejorar la imagen de fondo.
- El responsive entre el footer no quedan responsive.
- Entre el formulario y el footer queda un espacio en blanco, por estetica se queda asi o se mejora.

---
## [ch1.2.2-Alpha.1] - 2025-03-29

### Added

- Se agrego la funcionalidad de `registrarse`
- Se agrego el archivo decorador `utils.py`

### Fixed

- Se corrigió el error en el sistema de mensajes, asegurando que las notificaciones sean visibles para el usuario en lugar de solo para el administrador de Django.
- Se ajustó la visualización del sistema de mensajes para que aparezca centrado en la interfaz.

---

## [ch1.1.1-Alpha.1] - 2025-03-28

### Added

- Se agrego el `README.md`

### Fixed

- Se corrigio las extension de algunos archivos

--- 

## [ch1.0.0-Alpha.1] - 2025-03-28

### Added

- Se sube las estructuras del proyecto `Templates`,`Static: Css,img,js`
- Se agrego archivo `urls.py`
- Se agrego en la carpeta templates archivo `pagina_principal.html`
- Se agrego en la carpeta templates archivo `iniciar_sesion.html`
- Se agrego en la carpeta templates archivo `nuestros_servicios.html`
- Se agrego en la carpeta templates archivo `registrarse.html`
- Se agrego en la carpeta templates archivo `base.html`
- Se agrego en la carpeta Static: Css archivo `Pagina_principal.css`
- Se agrego en la carpeta Static: Css archivo `iniciar_sesion.css`
- Se agrego en la carpeta Static: Css archivo `nuestros_servicios.css`
- Se agrego en la carpeta Static: Css archivo `registrarse.css`
- Se agrego en la carpeta Static: Css archivo `base.css`
- Se agrego en la carpeta Static: Css archivo `bootstrap.min.css`
- Se agrego en la carpeta Static: Css archivo `bootstrap.min.css.map`
- Se agrego en la carpeta Static: Js archivo `bootstrap.bundle.min.js`
- Se agrego en la carpeta Static: Js archivo `bootstrap.bundle.min.js.map`
- Se agrego en la carpeta Static: img `Fotos que se usaran para: Pagina_principal, Iniciar_Sesion, Nuestros_servicios, Base , Registrarse`
- Se agrego en el models `Tabla Usuario`











