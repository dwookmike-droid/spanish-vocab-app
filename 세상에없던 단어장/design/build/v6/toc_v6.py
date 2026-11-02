# 24-chapter plan v6 (original plan file not found on the box -> finalized here, reconciled with v5 chapter map)
from plan_v5 import CH,PARTS,SKINS
# n: (grammar KO, example ES, example KO)
GR={
1:('명사 + 형용사 · 성·수 일치 · de 합성어 · 주어 생략','la toalla blanca · el cepillo de dientes','하얀 수건 · 칫솔'),
2:('hay(있다) vs está(…에 있다) · 장소는 뒤에','Hay dos platos en la mesa.','식탁에 접시가 두 개 있어요.'),
3:('위치 전치사구: 명사 + está + al lado de …','El sofá está al lado de la ventana.','소파는 창문 옆에 있어요.'),
4:('소유사: mi는 명사 앞, mío는 명사 뒤','mi cama · la cama mía','내 침대 · 내 것인 침대'),
5:('형용사 자리가 바뀌면 뜻도 바뀜 (gran / grande)','un gran patio · un patio grande','멋진 안뜰 · 넓은 안뜰'),
6:('수량 + de + 명사','un kilo de tomates · media docena de huevos','토마토 1킬로 · 달걀 반 다스'),
7:('gustar: 좋아하는 것이 주어, 뒤에 옴','Me gustan las croquetas.','나는 크로케타를 좋아해요.'),
8:('간접목적 me / le는 동사 앞 (주문하기)','¿Me trae la cuenta, por favor?','계산서 좀 갖다주시겠어요?'),
9:('직접목적 lo / la는 동사 앞','¿El café? Lo quiero con leche.','커피요? 우유 넣어서 주세요.'),
10:('의문문: 의문사 + 동사 + 주어','¿Dónde está la plaza?','광장이 어디예요?'),
11:('이동: ir a + 장소 · en + 교통수단 · a pie','Voy a Toledo en tren.','기차로 톨레도에 가요.'),
12:('긍정 명령: 대명사는 동사 끝에 붙임','Siga recto y gire a la derecha. · Sígame.','직진하다가 오른쪽으로 도세요. · 따라오세요.'),
13:('대명사 두 개: me lo · se lo (사람 먼저)','¿Me lo sube a la habitación?','그거 방으로 올려 주시겠어요?'),
14:('부정: no + 동사 · 이중 부정 nada / nunca','No tengo nada que declarar.','신고할 것이 없어요.'),
15:('진행형: 대명사 자리 두 가지','Me estoy bañando. = Estoy bañándome.','지금 수영하고 있어요.'),
16:('주어 없는 날씨 표현','Llueve. · Hace calor. · Hay niebla.','비가 와요. · 더워요. · 안개가 껴요.'),
17:('빈도부사 자리: Nunca juego = No juego nunca','Siempre corro por la mañana.','나는 늘 아침에 달려요.'),
18:('비교: más + 형용사 + que','Esta montaña es más alta que aquella.','이 산이 저 산보다 높아요.'),
19:('관계절 que: 꾸미는 말은 명사 뒤','la guitarra que toca mi padre','아버지가 치는 기타'),
20:('무인칭·수동의 se','Se prohíbe tocar los cuadros.','그림을 만지면 안 돼요.'),
21:('지시사: este / ese + 대명사로 쓰기','¿Este o ese? Me llevo este.','이거요, 그거요? 이걸로 살게요.'),
22:('doler: 아픈 곳이 주어 · 신체엔 정관사','Me duele la cabeza.','머리가 아파요.'),
23:('재귀 ponerse + 대명사 두 개 붙이기','Me pongo el abrigo. · ¡Póntelo!','외투를 입어요. · 그거 입어!'),
24:('종합: 시간 · 장소 · 방식의 순서와 강조','Mañana vamos a la plaza en metro.','내일 지하철로 광장에 가요.'),
}
WORDS={n:20 for n in range(1,25)}
ROMAN=['I','II','III','IV','V']
