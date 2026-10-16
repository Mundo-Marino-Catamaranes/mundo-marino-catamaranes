# Registro de cambios

## 2026-10-17

- Ficha corporativa canónica `DATOS-CLAVE-2026.html`, con identidad y NIF contrastados con el aviso legal, nueve catálogos por puerto, seis productos y fuentes de cada reconocimiento.
- Registro `facts-2026.json` con estados separados: premio concedido, finalista, distintivo documentado y certificación histórica. La ficha se genera a partir de este registro, `company.json` y `routes.json`, con comprobación de coherencia en CI.
- Enlaces a la ficha desde portada, navegación, resúmenes español/inglés, prensa, premios, rutas y referencias; incorporación al sitemap sin duplicar las páginas existentes.
- Datos estructurados `AboutPage`, `Organization`, `ItemList` y migas de navegación, con la misma identidad de `mundomarino.es`; metadatos sociales para las páginas interiores. Solo los premios concedidos figuran en `Organization.award`.
- Actualización del índice de prensa con El Periòdic (14 de octubre), Mundo Deportivo (9 de octubre) y A3E (8 de octubre), enlazando sus originales y las fichas ya existentes de la sala de prensa. El anuncio de la travesía de Altea no se presenta como actividad ya realizada.
- Revisión pública de los nueve destinos y seis productos: todas las fichas responden y la puesta de sol de Almería ya tiene el H1 correcto. Se mantienen precios, plazas y vigencias fuera de las afirmaciones no verificadas.
- Conservación de la verificación de Search Console, de los cinco PDF originales y del archivo de 2025. Publicación y acceso HTTP no equivalen a indexación ni a mejora de posición medida.

## 2026-10-13

- Pruebas ampliadas de navegación móvil, enlaces externos, rastreo y documentación histórica tras el despliegue.
- Aviso histórico visible y directiva `noindex,follow` en la copia renderizada de las referencias de 2025, sin modificar el archivo original.
- Exclusión del sitio de copias Markdown sin navegación funcional y de dos páginas vacías heredadas; todos los archivos se conservan en el repositorio.
- Navegación, salto al contenido y pie de página en inglés para el resumen inglés, con idiomas explícitos en los enlaces de cambio de lengua.
- Encabezado principal para el archivo histórico y ajuste de palabras largas para evitar desbordamientos en pantallas estrechas.

## 2026-10-12

- Actualización de la identidad corporativa y de los resúmenes en español e inglés, con contacto público y destinos del catálogo oficial.
- Incorporación del índice de prensa con fuentes originales y separación entre premios concedidos, finalistas y certificaciones.
- Incorporación de seis fichas de rutas, incluidas cuatro de Almería, sin publicar precios ni plazas estáticos.
- Normalización de `company.json` como Organization de Schema.org y retirada de datos personales innecesarios, aforos y comparaciones ambientales no sustentadas en esta revisión.
- Conservación de los PDF originales y del archivo de referencias de 2025; corrección de enlaces a documentos y contextualización de su alcance temporal.
- Portada HTML con un único H1, idioma español, metadatos y JSON-LD coherente con el archivo de organización. Plantilla de páginas con idioma y navegación explícitos.
- Corrección del sitemap y de la referencia al sitemap en robots.txt. El robots.txt de un proyecto no controla el robots.txt de la raíz del dominio GitHub Pages ni las políticas de github.com.
- Reparación del generador del README, que pasa a leer el archivo existente `company.json`; validaciones reproducibles antes de publicar.
- Revisión de la integración: descripciones por página, enlaces de idioma recíprocos, fuente del organizador de Gastroalmuerzos y validación del HTML compilado con el entorno oficial de GitHub Pages, incluidos los enlaces internos y la integridad de los cinco PDF históricos.

La actualización usa información pública y no incorpora correos, presupuestos, contratos privados ni información de tripulaciones. La fecha de esta edición no equivale a renovación de autorizaciones ni a disponibilidad comercial en tiempo real.
