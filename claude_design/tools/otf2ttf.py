import sys
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
src, dst = sys.argv[1:]
f = TTFont(src); gs = f.getGlyphSet(); glyf = {}
for n in f.getGlyphOrder():
    p = TTGlyphPen(gs); gs[n].draw(Cu2QuPen(p, 1.0, reverse_direction=True)); glyf[n] = p.glyph()
f['loca'] = newTable('loca'); g = f['glyf'] = newTable('glyf'); g.glyphOrder = f.getGlyphOrder(); g.glyphs = glyf
del f['CFF ']; f.sfntVersion = '\0\1\0\0'
f['maxp'].tableVersion = 0x10000
for k in ('maxZones','maxTwilightPoints','maxStorage','maxFunctionDefs','maxInstructionDefs','maxStackElements','maxSizeOfInstructions','maxComponentElements','maxPoints','maxContours','maxCompositePoints','maxCompositeContours','maxComponentDepth'):
    setattr(f['maxp'], k, 0)
f['maxp'].maxZones = 1
f['head'].indexToLocFormat = 1
f['post'].formatType = 3.0
f.save(dst)
