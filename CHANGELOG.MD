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

## [ch2.34.30-Alpha.1] - 2025-05-25

## Added

- Se agrego la funcionalidad de filtrar en los productos por edad y sexo.

---

## [ch2.33.30-Alpha.1] - 2025-05-21

## Fixed

- Se corrigio el Estilo de Listar usurios y adopciones para darles un estado mas limpio.

---

## [ch2.33.29-Alpha.1] - 2025-05-21

## Added

- Se agrego el modulo  `soportes`, `suspender_cuenta`, `notificaciones`. para que los usuarios puedean enviar quejas sobre el funcionamiento de la pagina 

## Fixed 

- Se modifico el contenido de la `base_sesion` para agregar un submenu en el apartado configuraciones y 

---

## [ch2.32.28-Alpha.1] - 2025-05-20

## Added

- Se agrego en el formulario registrarse Los terminos y condiciones

## Fixed

- Se corrigio el Estilo de Listar mascotas perdidas

---

## [ch2.31.27-Alpha.1] - 2025-05-19

## Added

- Se pinto las publicaciones y productos en la pagina principal

## Fixed

- Se corrigieron `iniciar_sesion` y `registrarse`que al marcar error no se borre un formulario.

---

## [ch2.30.26-Alpha.1] - 2025-05-12

## Fixed

- Se corrigieron errores de mensajes y de carrito

---

## [ch2.30.25-Alpha.1] - 2025-05-11

## Added

-Se agrego un modal para  `Mascotas perdidas` y  `Adopciones` para tener una vista mas completa de la publicacion.

## Fixed

- Se corrigio el diseño de algunas paginas para tener un estilo mas simple para el usuario como  `Veterinarias Asociadas`,  `Adopciones`,  `Productos`,  `Pagina_administrador`.

---

## [ch2.29.24-Alpha.1] - 2025-05-10

## Added

- Se agrego el modulo de reportes, se le dio un estilo simple y entendido para el administrador a la hora de ver los reportes.

---

## [ch2.28.24-Alpha.1] - 2025-05-05

## Added

- Se agrego el modulo de configuracion, se le dio un estilo simple y entendido para el usuario.
- Se agrego la funcionalidad para eliminar la cuenta permanente.

---

## [ch2.27.24-Alpha.1] - 2025-05-03

## Added

- Se agrego el modulo de mis publicaciones, para que cada usuario pueda ver solo sus publicaciones.
- se agrego el editar de las publicaciones de cada usuario, para asi poder corregir y actualizar su publicacion sin ningun problema.

---

## [ch2.26.24-Alpha.1] - 2025-05-02

## Changed

- Se corrigio el estructurado del footer

---

## [ch2.26.23-Alpha.1] - 2025-05-02

## Fixed

- Se corrigio la foto del usuario que al cambiarla salga tambien en la publicacion, se modifico un poco el editar usuario cambio de color..

---

## [ch2.26.22-Alpha.1] - 2025-05-01

## Added

- Se Agrego funcionalidad al editar perfil, ya todo esta en funcionamiento, puede actualizar tanto una campo, como la contraseña.

---

## [ch2.25.22-Alpha.1] - 2025-05-01

## Fixed

- Se corrigio el modulo de productos la foto del producto, que cuando se editaba y se guardaba la foto se eliminaba.

- Se corrigio las validaciones del formulario del usuario.

- Se Actualizo el aspecto del usuario a la hora de ver las publicaciones, que al momento de agregar una mascota salga el formulario en una ventana modal.

---

## [ch2.25.21-Alpha.1] - 2025-04-29

# Added

- Se agrego que cuando sea administrador ahí en el icono de usuario que despliegue la opción panel administrador, de resto si es usuario no aparezca.

## Fixed

- Se corrigio el formulario de productos para que no permita cantidad negativa, precio mayor a 0 y que sea decimal.

- Se corrigio el direccionamiento de registar tenia un pequeño bug.

---

## [ch2.24.20-Alpha.1] - 2025-04-29

## Fixed
- Se corrigio en el admin el modulo productos en el formulario que solo se permitan fotos en formatos JPG, JPEG, PNG, GIF.

- Se corrigio el modulo de productos donde se ven los productos mas vendidos, la logica estaba mal por que ciertas cosas no tenian sentido, pero ya se soluciono el problema.

---

## [ch2.24.19-Alpha.1] - 2025-04-28

## Added 

- Se agrego nueva funcionalidad de ver producto detalladamente, se le agrego un carrusel para ver varios productos.

---

## [ch2.23.19-Alpha.1] - 2025-04-28

## Added

- Se agrego funcionalidad para que una foto sea estrictamente png, jpg o jpeg

# Fixed

- Se corrigio un error la cual no se habria el carrito

## Note

- Queda pendiente arreglar que cuando se agregar o incrementa el carrito se reinicia la pagina

---

## [ch2.22.18-Alpha.1] - 2025-04-24

## Added

- Se agrego una nueva funcionalidad para los productos destacados.

---

## [ch2.21.18-Alpha.1] - 2025-04-24

## Fixed

- Se corrigio el modulo de productos para darle una buena estetica mas simple y entendida para el usuario.

---

## [ch2.21.17-Alpha.1] - 2025-04-21

## Added

- Se agrego la funcionalidad editar_usuario (Todavia esta estatico)

---

## [ch2.20.17-Alpha.1] - 2025-04-21

## Added

- Se reestructuro toda la pagina_principal

## Fixed

- Se corrigio dropdown de la pagina principal
- Se corrigio el logo de sus tamaños, posiciones, de base_sesion y pagina principal

## Removed

- Se elimino las paginas `Quienes somos, contactos , Nuestros servicios con sus respectivos Css, Base`


---

## [ch1.19.16-Alpha.1] - 2025-04-11

## Added

- Se añadio Templates del `modal_carrito` por problemas de mensajes

## Fixed

- Se corrigio la encriptacion de contraseñas
- Se corrigio el error que no lo deje agregar si no hay cantidad disponible

---

## [ch1.18.15-Alpha.1] - 2025-04-08 

## Added

- Se agrego menu de usuario Icono

## Fixed 

- Se corrigieron los colores del modulo `iniciar_sesion` y `registrase`

---

## [ch1.18.14-Alpha.1] - 2025-04-06

## Added 

- Se agrego funcionalidad para validar que un correo sea de tipo `@Gmail.com, @hotmail.com, @outlook.com`

## Fixed

- Se corrigio imagenes que no cargaban en panel administrador y pagina usuarios

---

## [ch1.17.13-Alpha.1] - 2025-04-06

## Added

- Se agrego la funcionalidad de redirigir publicacion dependiendo de que tipo era, Mascotas perdidas y adopciones.
- Se implemento nuevo formulario para subir una publicacion mas detallada.

## Fixed

- Se corrigio el diseño del administrador.
- Se cambiaron los colores del panel administrador.
- Se corrigio el redireccionamiento del usuario al iniciar sesion.

---

## [ch1.16.12-Alpha.1] - 2025-04-05

## Added

- Se agrego toda la funcionalidad del carrito
- Se agrego nueva tablas de los carritos
- Se agrego carpetas nuevas en el templates

## Fixed

- Se corrigieron erros en la imagenes de iniciar sesion y registrarse.
- Se corrigio logica de las views

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











