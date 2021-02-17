*TheBoloBot*

Bot diseñado para registrar los fracasos de la pesca de @carpfishingespana.

*Comandos:*

- /help - muestra una ayuda inicial
- /ayuda - muestra una ayuda inicial
- /start - muestra una ayuda inicial
- /register - *comando eliminado* (en futuras versiones ni siquiera existirá)
- /bolo - registra un bolo
- /top - muestra el TOP X actual de bolos. Acepta un parámetro X, por defecto 10. Válido tanto /top3 como con un espacio o barra baja entre *top* y *3* (/top\_3). Permite mostrar hasta 50 usuarios en el ranking.
- /ultimos - muestra los últimos N usuarios que han registrado un bolo. Acepta un parámetro N, por defecto 10. Válido tanto /ultimos3 como con un espacio o barra baja entre *ultimos* y *3* (/ultimos\_3). Permite mostrar hasta 50 usuarios en el ranking.
- /version - muestra la versión actual del bot

*Comandos de administración:*

- /unregister - *[ADMIN]* elimina los datos de un usuario. El usuario puede eliminarse según su *id* (Ej: `/unregister 15156`) o según su *username* (`/unregister @someone` ó `/unregister someone`). Entre el comando y el usuario puede haber una barra baja, un espacio o incluso nada.
- /reset - *[ADMIN]* elimina todos los datos, sin vuelta atrás.
- /remove\_inactive - *[ADMIN]* elimina los usuarios con 0 bolos. Al estar eliminado el comando /register no debería haber ningún usuario con 0 bolos.

Si existe algún problema, contacte con el desarrollador ({developer})
