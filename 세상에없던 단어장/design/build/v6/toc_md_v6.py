import sys;sys.path.insert(0,'.')
from toc_v6 import CH,SKINS,PARTS,GR
from base_v6 import V3
from data_v6 import CH02,CH11
W={
1:[i['es'] for i in V3],2:[x[1] for x in CH02],11:[x[1] for x in CH11],
3:'el sofá,el sillón,la mesa,la silla,la lámpara,la alfombra,la estantería,el libro,la televisión,el mando,el cojín,la cortina,la ventana,la puerta,el cuadro,la planta,el reloj,la chimenea,el suelo,la pared',
4:'la cama,la almohada,la sábana,la manta,el armario,la percha,la mesilla,el despertador,el espejo de pie,la cómoda,el cajón,la persiana,el balcón,la llave,la maleta,el pijama,las zapatillas,el enchufe,el cargador,la luz',
5:'el patio,el jardín,la maceta,la flor,el geranio,el árbol,la hoja,la fuente,el banco,la valla,la regadera,la manguera,el césped,el limonero,la buganvilla,el pozo,la reja,el toldo,la hamaca,la sombra',
6:'la manzana,la naranja,el plátano,la uva,la fresa,el melón,la sandía,el limón,el tomate,la lechuga,la cebolla,el ajo,la patata,la zanahoria,el pimiento,el pepino,la berenjena,la seta,el kilo,la bolsa',
7:'la tapa,el pintxo,la croqueta,la tortilla,las aceitunas,el jamón,el queso,las gambas,el pulpo,los calamares,el pan,el palillo,la barra,el camarero,la caña,el vino,el vermut,la ración,la servilleta,el plato pequeño',
8:'la mesa,la carta,el menú del día,el primer plato,el segundo plato,el postre,el agua,la botella,la copa,el vaso,la cuenta,la propina,la reserva,el cocinero,la sopa,la carne,el pescado,el arroz,la ensalada,el aceite',
9:'el café,el café con leche,el cortado,el té,el zumo,el cruasán,la magdalena,los churros,el chocolate,la tostada,la barra de pan,la panadería,la taza,el azúcar,la cucharilla,la terraza,la mesa,la cuenta,el bocadillo,la tarta',
10:'la calle,la plaza,la avenida,el edificio,la iglesia,el ayuntamiento,el mercado,el parque,el puente,la esquina,el semáforo,el paso de cebra,la acera,el balcón,el portal,el barrio,la tienda,el banco,la farmacia,el cajero',
12:'la derecha,la izquierda,todo recto,la esquina,la calle,el cruce,la cuesta,el mapa,el norte,el sur,el este,el oeste,cerca,lejos,al lado de,enfrente de,detrás de,delante de,la señal,el callejón',
13:'el hotel,la recepción,la habitación,la llave,la tarjeta,el ascensor,la escalera,la planta,el desayuno,la toalla,la reserva,el pasaporte,la maleta,el recepcionista,la cama doble,la ducha,el wifi,la salida,la factura,la almohada',
14:'el aeropuerto,el avión,el vuelo,la puerta de embarque,la tarjeta de embarque,el pasaporte,el equipaje,la maleta,el control de seguridad,la terminal,la llegada,la salida,el retraso,el asiento,la ventanilla,el pasillo,el billete,la aduana,el carrito,la pantalla',
15:'la playa,el mar,la arena,la ola,el sol,la sombrilla,la toalla,el bañador,la crema solar,las gafas de sol,el chiringuito,el barco,la roca,la concha,el socorrista,la hamaca,el helado,el cubo,la pala,el puerto',
16:'el tiempo,el sol,la lluvia,la nube,el viento,la niebla,la nieve,la tormenta,el trueno,el rayo,el paraguas,el calor,el frío,la temperatura,el grado,el cielo,el arcoíris,el chubasquero,la previsión,la estación',
17:'el fútbol,el balón,el estadio,el equipo,el partido,el gol,la pelota,la bicicleta,la carrera,el corredor,la fiesta,el pañuelo,la banda,los fuegos artificiales,el desfile,la entrada,el campeón,el árbitro,la piscina,el gimnasio',
18:'la montaña,el río,el puente,el valle,el bosque,el árbol,la roca,el camino,el lago,la cascada,el cielo,la piedra,la cueva,el pájaro,el águila,la flor,el sendero,el mirador,la colina,el olivo',
19:'la guitarra,el cante,el baile,el bailaor,la bailaora,el tablao,las palmas,el abanico,las castañuelas,el vestido de flamenca,el escenario,la canción,el ritmo,el concierto,el músico,el tambor,el piano,el violín,la entrada,el público',
20:'el museo,el cuadro,la pintura,el pintor,la escultura,la sala,la entrada,la taquilla,la exposición,el marco,el retrato,el paisaje,la guía,la audioguía,el guarda,la tienda,el plano,el cartel,el horario,el banco',
21:'la tienda,el mercadillo,el puesto,el precio,la oferta,las rebajas,el euro,la moneda,el billete,la tarjeta,el recibo,la bolsa,la caja,el probador,la talla,el descuento,el regalo,la antigüedad,el vendedor,el cambio',
22:'la cabeza,el ojo,la oreja,la nariz,la boca,el diente,el cuello,el brazo,la mano,el dedo,la pierna,el pie,la espalda,el estómago,la farmacia,la pastilla,la receta,la tirita,el jarabe,el termómetro',
23:'la camisa,la camiseta,el pantalón,la falda,el vestido,la chaqueta,el abrigo,el jersey,los zapatos,las botas,los calcetines,el sombrero,la bufanda,los guantes,el cinturón,la corbata,el botón,la cremallera,el bolso,la gorra',
24:'la fiesta,la falla,el ninot,el petardo,la traca,la mascletà,la hoguera,el fuego,la música,la banda,el traje,la flor,la ofrenda,la procesión,la feria,el farolillo,el confeti,la verbena,la cena,el desfile'}
for k,v in W.items():
    if isinstance(v,str): W[k]=v.split(',')
    assert len(W[k])==20,(k,len(W[k]))
out=['# Vocabulario visual · Español — 24장 총 목차 (v6)','',
'각 장: 사진 오프너 + 단어 20개(핵심 8 + 보조 12) + 어순 포인트 1개(앞 장 위에 쌓아 올림). 굵은 숫자 장(01·02·11)은 이번 PDF에 실린 장.','',
'| 장 | ES | KO | 도시 | 스킨 | 오프너 사진(계획) | 어순 포인트 · 예문 |','|---|---|---|---|---|---|---|']
cur=-1;det=[]
for (part,n,es,ko,city,skin,op,sig,acc) in CH:
    if part!=cur: cur=part;out.append(f'| **{PARTS[part]}** | | | | | | |')
    g,ex,exk=GR[n];b='**' if n in(1,2,11) else ''
    out.append(f'| {b}{n:02d}{b} | {es} | {ko} | {city} | {SKINS[skin][0]} | {op} | {g} — *{ex}* ({exk}) |')
    det.append(f'### {n:02d} · {es} · {ko} — {city} · {SKINS[skin][0]}\n- 어순: {g} — *{ex}* ({exk})\n- 소품: {sig}\n- 단어 20: '+', '.join(W[n])+'\n')
out+=['','## 장별 단어 20개','']+det
open('/workspace/trilingual/es/v6/TOC_v6.md','w').write('\n'.join(out));print('ok',len(out))
