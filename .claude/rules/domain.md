# Alcance funcional

- Registro e inicio de sesión de usuarios.
- CRUD de incidencias (crear, consultar, modificar, eliminar).
- Clasificación de incidencias por prioridad (baja / media / alta) y estado
  (abierta / en proceso / cerrada).
- Filtrado por estado y por prioridad.
- Registro del equipo o servicio afectado.
- Dashboard con estadísticas básicas y al menos 3 gráficos (total de
  incidencias, abiertas/cerradas, prioridad alta, por prioridad, por estado,
  evolución temporal).
- Detección de incidencias similares (posibles duplicados) mediante un
  modelo de ML sencillo: TF-IDF sobre título, descripción y equipo, y
  similitud coseno contra las incidencias abiertas/en proceso. Se sugieren
  al crear una incidencia y en su detalle; no requiere etiquetas.
- Comprobación de conectividad de red (ping/socket a un puerto o petición
  HTTP a un equipo/servicio).
- Comprobación de operabilidad del sistema de extremo a extremo: un botón
  en `incidents:operability` pide, mediante una petición HTTP directa desde
  el navegador, una incidencia aleatoria no archivada ni cerrada al
  microservicio Flask de `networking/`, y la muestra con un enlace a su
  detalle. Confirma que la base de datos, la red y ese servicio externo
  funcionan juntos.

## Modelo de datos: Incidencia

| Campo       | Descripción                                    |
| ----------- | ---------------------------------------------- |
| Título      | Nombre de la incidencia                        |
| Descripción | Explicación del problema                       |
| Equipo      | Equipo o servicio afectado                     |
| Fecha       | Fecha de registro                              |
| Prioridad   | Baja, media, alta                              |
| Estado      | Abierta, en proceso, cerrada                   |
| Usuario     | Usuario que registró la incidencia (FK a User) |

## Modelo de usuario

El registro e inicio de sesión ya está implementado en la app `user/`: un
modelo de usuario propio (`user.CustomUser`, configurado como
`AUTH_USER_MODEL`) que autentica por email en lugar de username, con DNI
español validado (formato + letra de control) como campo obligatorio
adicional. Ver `user/models.py`, `user/managers.py` y `user/validators.py`.
