from PIL import Image,ImageDraw,ImageFont
V5='/workspace/trilingual/es/v5_mixed';V6='/workspace/trilingual/es/v6'
F=ImageFont.truetype(f'{V6}/fonts/GowunBatang-Bold.ttf',22);Fs=ImageFont.truetype(f'{V6}/fonts/GowunBatang-Regular.ttf',17)
P=[('ch01 오프너: 흐린 사진 → 선명한 312ppi 알람브라 욕실',f'{V5}/ch01/img/opener_comares.jpg',f'{V6}/ch01/img/opener_v6.jpg'),
('ch02 오프너: 간판 보이는 노점 → 발렌시아 중앙시장 외관',f'{V5}/ch02/img/opener.jpg',f'{V6}/ch02/img/opener_v6.jpg'),
('기차: León 열차 → 마드리드 아토차 AVE(로고 지움)',f'{V5}/ch11/img/train.jpg',f'{V6}/ch11/img/train.jpg'),
('버스: EMT 로고·광고 → 지우고 배경 제거',f'{V5}/ch11/img/bus.jpg',f'{V6}/ch11/img/c_bus.png'),
('헬멧: Airoh 로고 → 지움 + 배경 제거',f'{V5}/ch11/img/helmet.jpg',f'{V6}/ch11/img/c_helmet.png'),
('지하철: Metro 로고 → 로고 없는 승강장',f'{V5}/ch11/img/metro.jpg',f'{V6}/ch11/img/metro.jpg'),
('승차권: 저해상도 → 300ppi 이상 + 배경 제거',f'{V5}/ch11/img/ticket.jpg',f'{V6}/ch11/img/c_ticket.png'),
('도로: 저해상도 → 300ppi 이상 A-702',f'{V5}/ch11/img/road.jpg',f'{V6}/ch11/img/road.jpg'),
('냉장고: 좁은 카드 → 가로 카드, 로고 지움',f'{V5}/ch02/img/fridge.jpg',f'{V6}/ch02/img/fridge.jpg'),
('비행기: 항공사 도색 → 무도색 기체',f'{V5}/ch11/img/plane.jpg',f'{V6}/ch11/img/c_plane.png'),
('배낭: 로고·태그 → 무지 배낭',f'{V5}/ch11/img/backpack.jpg',f'{V6}/ch11/img/c_backpack.png'),
('정류장: 광고판 → 빈 패널',f'{V5}/ch11/img/stop.jpg',f'{V6}/ch11/img/stop.jpg'),
('좌석: 중국 열차 → 스페인 Renfe 좌석',f'{V5}/ch11/img/seat.jpg',f'{V6}/ch11/img/seat.jpg'),
('칼: 브랜드 각인 → 지우고 다시 자름',f'{V5}/ch02/img/knife.jpg',f'{V6}/ch02/img/knife.jpg'),
('전자레인지: 브랜드·모델명 → 지움',f'{V5}/ch02/img/microwave.jpg',f'{V6}/ch02/img/microwave.jpg')]
TW,TH=300,240;cols=3;cw=TW*2+40;ch=TH+60
rows=(len(P)+cols-1)//cols
C=Image.new('RGB',(cols*cw+20,rows*ch+70),'#f3ecdf');d=ImageDraw.Draw(C)
d.text((20,18),'v5 → v6 수정 전/후 (왼쪽 v5 · 오른쪽 v6)',font=F,fill='#1f1b17')
def th(p):
    im=Image.open(p).convert('RGBA');im.thumbnail((TW,TH));bg=Image.new('RGBA',(TW,TH),(255,253,248,255));bg.alpha_composite(im,((TW-im.width)//2,(TH-im.height)//2));return bg.convert('RGB')
for n,(lab,a,b) in enumerate(P):
    x=20+(n%cols)*cw;y=60+(n//cols)*ch
    C.paste(th(a),(x,y+30));C.paste(th(b),(x+TW+10,y+30))
    d.text((x,y+4),lab,font=Fs,fill='#7a2f1c');d.text((x+TW-8,y+30+TH//2-12),'→',font=F,fill='#a4533a')
C.save(f'{V6}/_shots/compare_fixes_v6.png');print(C.size)
