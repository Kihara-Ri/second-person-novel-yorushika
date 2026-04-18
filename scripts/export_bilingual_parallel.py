from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "exports"
PREVIEW_INDEX_PATH = OUTPUT_DIR / "preview_index.json"
PREVIEW_GROUPS_DIR = OUTPUT_DIR / "preview_groups"

SOURCE_FILES = [
    ROOT / "translations/batches/翻译双语对照_批次A.md",
    ROOT / "translations/batches/翻译双语对照_批次B.md",
    ROOT / "translations/batches/翻译双语对照_批次C.md",
    ROOT / "translations/batches/翻译双语对照_批次D.md",
    ROOT / "translations/batches/翻译双语对照_补遗.md",
    ROOT / "translations/batches/翻译双语对照_批次F.md",
]


@dataclass(frozen=True)
class GlossaryEntry:
    term: str
    reading: str
    short_gloss: str
    work_function: str
    long_note: str
    aliases: tuple[str, ...] = ()


GLOSSARY = [
    GlossaryEntry(
        term="白妙",
        reading="しろたえ",
        short_gloss="古典诗歌语汇中的白布、白衣与洁白之色。",
        work_function="把云、袖、月等意象连在一起，不只是普通的“白”。",
        long_note="原本指白栲布，后来又引申为白衣、白袖与清冷纤薄的洁白。在本作中，它往往同时牵动身体、衣料、月光与云气的联想。",
    ),
    GlossaryEntry(
        term="白栲",
        reading="しろたえ",
        short_gloss="古代树皮纤维织成的白布。",
        work_function="用来说明“白妙”的古典来源。",
        long_note="老师回信通过“白栲”解释“白妙”，提示它不是现代口语，而是古典和歌语汇。",
    ),
    GlossaryEntry(
        term="土用波",
        reading="どようなみ",
        short_gloss="盛夏土用时节的大浪。",
        work_function="把夏天、海边、身体感和乡愁压缩在一个词里。",
        long_note="它不是普通的海浪，而是带季节限定性的夏浪，常带不稳、发热、躁动的气息。",
    ),
    GlossaryEntry(
        term="白南風",
        reading="しらはえ",
        short_gloss="夏季自南吹来的风，带古典季语色彩。",
        work_function="强化夏日、海边、白色与风感的意象链。",
        long_note="比普通“南风”更偏俳句、和歌语感，因此在诗里会带出更鲜明的季节与抒情背景。",
    ),
    GlossaryEntry(
        term="海月",
        reading="くらげ",
        short_gloss="日文汉字词，实指水母。",
        work_function="利用字面“海上的月亮”和实义“水母”的错位制造漂浮感。",
        long_note="它最容易误读成景物，但在日语里就是“水母”，也因此天然带有发光、透明、漂游的双重联想。",
    ),
    GlossaryEntry(
        term="入道雲",
        reading="にゅうどうぐも",
        short_gloss="高高隆起的夏季积雨云。",
        work_function="是作品里“夏天的大云”与乡下海边记忆的重要视觉支点。",
        long_note="名字来自它像剃发僧人光头的外形，因此“入道云”比普通“云”更具体，也更具夏日体感。",
    ),
    GlossaryEntry(
        term="唐紅",
        reading="からくれない",
        short_gloss="古典语汇里的深绯红、浓艳红。",
        work_function="让红色带上华丽、妖异与和歌传统的质感。",
        long_note="它通常不只是颜色描写，也会连到红叶、流水、染色与古典抒情系统。",
        aliases=("唐红",),
    ),
    GlossaryEntry(
        term="不埒",
        reading="ふらち",
        short_gloss="放肆、越界、不规矩。",
        work_function="放在温柔或慈爱旁边时，会产生越界的张力。",
        long_note="它不是单纯粗暴，而是带一点失范、不检点、边界被踩过的语气。",
    ),
    GlossaryEntry(
        term="ビイドロ",
        reading="びいどろ",
        short_gloss="旧式说法里的玻璃、玻璃器。",
        work_function="比普通“玻璃”更有旧时代、透明、易碎的抒情意味。",
        long_note="这个词保留了古早外来语质感，因此常比现代“ガラス”更适合诗里微亮、易碎、怀旧的东西。",
    ),
    GlossaryEntry(
        term="晴る",
        reading="はる",
        short_gloss="被故意拧成诗题的“放晴”，并与“春”同音。",
        work_function="把天气、季节、情绪与关系变化叠在一起。",
        long_note="它不是普通动词写法，而是有意识地保留了“晴”与“春”之间的听觉回响。",
    ),
    GlossaryEntry(
        term="春荒れ",
        reading="はるあれ",
        short_gloss="春日的风暴与荒乱天气。",
        work_function="把“春”从温柔季节拉向失衡与躁动。",
        long_note="在本作中它常不是单纯天气，而是一种关系与心绪正在翻涌的季节状态。",
        aliases=("春荒",),
    ),
    GlossaryEntry(
        term="羊雲",
        reading="ひつじぐも",
        short_gloss="像羊群一样排开的云。",
        work_function="提供非常具体的天象感，不是任意一种云。",
        long_note="它常见于秋日高空，视觉上是一团团散开的白云，因此比笼统的“云”更有形状。",
    ),
    GlossaryEntry(
        term="海原",
        reading="うなばら",
        short_gloss="辽阔铺展开来的海面。",
        work_function="让诗的尺度从局部身体一下展开到远方与大地。",
        long_note="它比单说“海”更古典、更广阔，带有视野整体铺开的感觉。",
    ),
    GlossaryEntry(
        term="鱗粉",
        reading="りんぷん",
        short_gloss="蝴蝶翅膀上的细小粉状鳞片。",
        work_function="把太阳光、蝶翼、粉末状散落感连起来。",
        long_note="它常被用来制造一种轻微、闪烁、会沾附在空气中的触感。",
        aliases=("鳞粉",),
    ),
    GlossaryEntry(
        term="竜田川",
        reading="たつたがわ",
        short_gloss="和歌里常与红叶染水相连的经典意象。",
        work_function="一旦出现，就等于主动接入古典和歌传统。",
        long_note="它不是普通地名，而是日本诗歌史里的意象节点，常写红叶、流水、染色和秋天。",
    ),
    GlossaryEntry(
        term="胡蝶の夢",
        reading="こちょうのゆめ",
        short_gloss="庄周梦蝶，讨论自我与现实边界的不稳定。",
        work_function="直接参与“我是谁”“语言是谁的”这些主题。",
        long_note="它在本作里不仅是知识典故，也是一种身份和感知持续摇晃的结构隐喻。",
        aliases=("胡蝶",),
    ),
    GlossaryEntry(
        term="宗匠俳句",
        reading="そうしょうはいく",
        short_gloss="讲究师承法度的俳句传统。",
        work_function="是老师不愿直接改写“我”的诗的重要思想背景。",
        long_note="老师借它区分“被教出来的熟练”与“只能从本人内里长出的表达”。",
    ),
    GlossaryEntry(
        term="芸事",
        reading="げいごと",
        short_gloss="带训练、习练、师承性质的技艺。",
        work_function="被拿来与“艺术”对比，强调纯技巧不等于真正表达。",
        long_note="它不是贬义，而是指出一种可以被教授和模仿的熟练系统。",
    ),
    GlossaryEntry(
        term="箱庭",
        reading="はこにわ",
        short_gloss="箱中庭园，也引申为封闭而过度可控的作品世界。",
        work_function="用于批评尺度过小、被规训得太精致的写作。",
        long_note="在文学批评语境里，它常指精巧却与真实世界张力脱开的作品。",
    ),
    GlossaryEntry(
        term="ファム・ファタル",
        reading="femme fatale",
        short_gloss="“致命女人”这一文化原型。",
        work_function="是理解“魔性”时被调动的西方文学背景。",
        long_note="它不是普通坏女人，而是带毁灭吸引力、会把他者拖入命运性灾祸的女性形象。",
    ),
    GlossaryEntry(
        term="サロメ",
        reading="salome",
        short_gloss="莎乐美，被文学与绘画不断重写的魔性形象。",
        work_function="把“魔性”连进西方艺术史里的想象系统。",
        long_note="在这里它不只是圣经人物名，而是后世重写出来的危险之美。",
    ),
    GlossaryEntry(
        term="マイルストーン",
        reading="milestone",
        short_gloss="里程碑。",
        work_function="在诗里带出“用告别标记进度”的意味。",
        long_note="它通常象征阶段性节点，放进这部作品里会天然带上旅程和成长的结构意味。",
    ),
    GlossaryEntry(
        term="ポスト春",
        reading="post-haru",
        short_gloss="把 post- 和“春”拼在一起的人造词。",
        work_function="制造“春之后”的空档感，也借用了思想史里的 post- 语感。",
        long_note="它不是简单时间顺序，而是一个被故意理论化、后置化的季节概念。",
    ),
    GlossaryEntry(
        term="ルバート",
        reading="rubato",
        short_gloss="音乐术语，指自由伸缩节拍地演奏。",
        work_function="让诗从文字显露出旋律感，也对应“我”对歌与诗的想象。",
        long_note="它既是具体音乐术语，也是这部作品里“节奏可以不服从规矩”的象征。",
    ),
    GlossaryEntry(
        term="啄木鳥",
        reading="きつつき",
        short_gloss="啄木鸟。",
        work_function="把鸟、笔尖叩击、空洞的心口和被一下下啄中的感觉连在一起。",
        long_note="它在诗中不只是鸟名，也像桌面上的笔声、胸口的空响与持续不断的敲击感。",
    ),
    GlossaryEntry(
        term="琥珀",
        reading="こはく",
        short_gloss="琥珀，树脂化石。",
        work_function="承载被时间沉积、保存下来的事物这一象征。",
        long_note="在这部作品里，它常和砂海、封存、时间重量、被保留下来的微小之物联系在一起。",
    ),
    GlossaryEntry(
        term="翡翠",
        reading="ひすい",
        short_gloss="翡翠，也带宝石般的青绿色感。",
        work_function="提供冷色、透明、珍贵且难以触碰的质地。",
        long_note="它既可能偏向宝石，也可能偏向颜色，因此常让意象显得既坚硬又轻亮。",
    ),
    GlossaryEntry(
        term="橙",
        reading="だいだい",
        short_gloss="橙色，也会牵出橙类果实联想。",
        work_function="让颜色带上果实、黄昏与季节的气味。",
        long_note="它并不只是色卡上的橙色，而常带着温度、香气与傍晚光线。",
    ),
    GlossaryEntry(
        term="銀杏",
        reading="いちょう",
        short_gloss="银杏树。",
        work_function="作为秋深转冷、时间进入收束期的季节标记。",
        long_note="它在作品里主要不是植物知识，而是用来提醒读者季节已经推进到深秋阶段。",
    ),
    GlossaryEntry(
        term="錨",
        reading="いかり",
        short_gloss="锚。",
        work_function="和“桨”一起构成终章里停驻与前行相互拉扯的意象系统。",
        long_note="在最后的诗群中，它不只是船具，而是把人系在原处、又让人意识到自己仍有重量的东西。",
    ),
    GlossaryEntry(
        term="懲役",
        reading="ちょうえき",
        short_gloss="徒刑中的劳役刑。",
        work_function="让“社会的惩罚已经结束”和“本人仍不能原谅自己”的落差变得具体。",
        long_note="这是制度层面的惩罚语汇，因此一出现就会把讨论从情感拉回法律与社会系统。",
    ),
    GlossaryEntry(
        term="七言絶句",
        reading="しちごんぜっく",
        short_gloss="每句七字、共四句的汉诗体裁。",
        work_function="提示文本主动接入汉诗传统，而不只是一般性引用。",
        long_note="它说明这里谈论的不是抽象中国古诗，而是非常具体的一种格律与文学传统。",
    ),
    GlossaryEntry(
        term="離思",
        reading="りし",
        short_gloss="元稹《离思五首》组诗。",
        work_function="把“见过更广大之物后无法回到原先尺度”的比较结构带进作品。",
        long_note="在本作中，它不只是出处说明，也参与了“见过以后就难以再满足”的情感逻辑。",
    ),
    GlossaryEntry(
        term="巫山の雲雨",
        reading="ふざんのうんう",
        short_gloss="中国典故，后常引申为男女情事。",
        work_function="让“云”在自然景象之外，又多出情欲和典故层。",
        long_note="它来自巫山云雨典故，因此一旦出现，云就不只是天气，也会带上身体与关系意味。",
    ),
    GlossaryEntry(
        term="アポリア",
        reading="aporia",
        short_gloss="哲学上“无路可通的思辨困局”。",
        work_function="把抽象思辨和上升、远望、想抵达地平线的欲望绑定在一起。",
        long_note="它不是普通难题，而是一种越想越难通过、却又无法不去想的思想困境。",
    ),
    GlossaryEntry(
        term="ルサンチマン",
        reading="ressentiment",
        short_gloss="带思想史意味的怨愤、积怨。",
        work_function="把情绪从日常“讨厌”提升成更沉、更结构化的反向怨意。",
        long_note="它通常指由无力感、压抑和比较转化出的怨恨，因此比普通愤怒更冷也更久。",
    ),
    GlossaryEntry(
        term="ランデヴー",
        reading="rendezvous",
        short_gloss="会合、私约、约见。",
        work_function="给相遇场景加上旧式、文艺、夜色般的都市抒情气味。",
        long_note="它来自法语外来语，所以比普通“见面”更像带一点装饰性与戏剧感的会合。",
    ),
    GlossaryEntry(
        term="ランタン",
        reading="lantern",
        short_gloss="灯笼、提灯。",
        work_function="提供夜路上可携带、会轻微摇晃的小光源感。",
        long_note="它比普通“灯”更具体，天然带着黑暗中的移动、照亮有限范围的感觉。",
    ),
    GlossaryEntry(
        term="金木犀",
        reading="きんもくせい",
        short_gloss="金木犀，秋日香气很强的花木。",
        work_function="作为“秋天已经到了”的嗅觉标记。",
        long_note="它常不是为了植物说明，而是为了让季节以香气而不是颜色出现。",
    ),
    GlossaryEntry(
        term="沈丁花",
        reading="じんちょうげ",
        short_gloss="沈丁花，也叫瑞香。",
        work_function="提供浓香、早春、贴近身体的嗅觉意象。",
        long_note="它的作用通常不是视觉，而是让空间先被气味填满，带出季节和回忆感。",
    ),
    GlossaryEntry(
        term="百日紅",
        reading="さるすべり",
        short_gloss="百日红，花期很长的夏日花木。",
        work_function="作为夏季仍在延长的花时标记。",
        long_note="它最醒目的不是知识性定义，而是“盛夏还没结束”的视觉与时间感。",
        aliases=("百日红",),
    ),
    GlossaryEntry(
        term="生垣",
        reading="いけがき",
        short_gloss="修剪成篱墙状的灌木。",
        work_function="给场景增加住宅区边界与隔着什么窥见景物的感觉。",
        long_note="它不是自然生长的树丛，而是明显带有人为整理痕迹的绿色边界。",
    ),
    GlossaryEntry(
        term="木立",
        reading="こだち",
        short_gloss="成片站立的小树林、树丛。",
        work_function="比单棵树更有风声、叶声和群体摇动感。",
        long_note="常用于带一点抒情滤镜的自然描写，尺度介于一棵树和森林之间。",
    ),
    GlossaryEntry(
        term="稜線",
        reading="りょうせん",
        short_gloss="山脊线、轮廓线。",
        work_function="让风景更立体，也让远处的云和山有清楚边缘。",
        long_note="它天然带一点锐利感，因此常把柔软的风景压出线条。",
    ),
    GlossaryEntry(
        term="稚拙",
        reading="ちせつ",
        short_gloss="幼稚而拙涩，不够成熟。",
        work_function="是“我”开始把作品交给他人观看时最明显的自我审查词。",
        long_note="它不是单纯说“差”，而是说作品还没有长成，带着未成熟的羞耻感。",
    ),
    GlossaryEntry(
        term="香木",
        reading="こうぼく",
        short_gloss="芳香明显的树木或香材。",
        work_function="把花香从普通嗅觉推进到更古典的香气分类。",
        long_note="作品里提到它时，重点不在植物学，而在季节和香气如何被文化性地命名。",
    ),
    GlossaryEntry(
        term="ダカーポ",
        reading="da capo",
        short_gloss="音乐术语，意为“从头再来一遍”。",
        work_function="把回返、循环与重新开始的感觉带进诗里。",
        long_note="它既是乐谱指令，也很适合在诗里承担“回到开头”的结构意味。",
    ),
    GlossaryEntry(
        term="追伸",
        reading="ついしん",
        short_gloss="附言、追记，相当于 P.S.",
        work_function="标记正式信件结束后，话语仍在纸边继续。",
        long_note="在书信体里它往往意味着更私密、也更忍不住不写的话。",
    ),
    GlossaryEntry(
        term="萩原朔太郎",
        reading="はぎわら さくたろう",
        short_gloss="日本近代诗人，现代口语诗的重要人物。",
        work_function="是作品前半最核心的诗歌参照系之一。",
        long_note="他的现代感伤、身体感和阴影质地，深刻影响了本作中蝶、云、孤独和自我裂开的写法。",
        aliases=("朔太郎",),
    ),
    GlossaryEntry(
        term="宮沢賢治",
        reading="みやざわ けんじ",
        short_gloss="日本作家、诗人，兼具自然、童话与宗教气息。",
        work_function="为“风在呼唤”“自然会说话”这条感受路径提供支点。",
        long_note="在本作里，他不是单纯阅读清单，而是“我”重新走向外部世界时的重要精神资源。",
    ),
    GlossaryEntry(
        term="北原白秋",
        reading="きたはら はくしゅう",
        short_gloss="日本诗人、歌词作者，擅长音乐性强的抒情语言。",
        work_function="为作品中的色彩、香气、枇杷和歌谣感提供背景。",
        long_note="他在这里经常和病、记忆、植物意象一起出现，因此不只是文坛名字，也是阅读方式的参照。",
        aliases=("白秋",),
    ),
    GlossaryEntry(
        term="島崎藤村",
        reading="しまざき とうそん",
        short_gloss="日本诗人、小说家，明治文学代表人物。",
        work_function="把“旅”“太阳”这一近代抒情传统引进作品。",
        long_note="他的出现让本作后段的“诗是旅”不只是一句漂亮话，也连上了日本近代抒情传统。",
    ),
    GlossaryEntry(
        term="正岡子規",
        reading="まさおか しき",
        short_gloss="近代日本俳句革新者。",
        work_function="是老师反对“宗匠俳句”时最关键的思想援引。",
        long_note="他强调写生和近代化，反对旧式宗匠体制，因此在本作里成了“不要把写作变成作法练习”的论据。",
        aliases=("子規",),
    ),
    GlossaryEntry(
        term="荘子",
        reading="そうし",
        short_gloss="中国先秦思想家，道家代表人物。",
        work_function="通过梦蝶典故进入作品的身份摇晃与现实不稳主题。",
        long_note="在本作里，庄子不是普通古人名，而是“我是谁”“梦和现实是否能分开”的思想入口。",
        aliases=("庄子", "荘周"),
    ),
    GlossaryEntry(
        term="孔子",
        reading="こうし",
        short_gloss="中国先秦思想家，儒家代表人物。",
        work_function="作为《孟子》引文中的坐标人物出现。",
        long_note="这里重点不在孔子思想本身，而在“从高处俯瞰世界”的经典尺度。",
    ),
    GlossaryEntry(
        term="元稹",
        reading="げんしん",
        short_gloss="唐代诗人，《离思》作者。",
        work_function="把“曾经沧海难为水”的比较结构与悼亡情感带进作品。",
        long_note="他在本作里非常关键，因为“看过真正重要之物后，其余都失色”的逻辑几乎就是人物关系的暗线。",
    ),
    GlossaryEntry(
        term="孟子",
        reading="もうし",
        short_gloss="中国战国思想家，儒家重要人物。",
        work_function="作为《离思》更早的典据来源，补足古典引文链条。",
        long_note="“观于海者难为水”这层比较结构，正是通过他被重新接入作品的。",
    ),
    GlossaryEntry(
        term="杜甫",
        reading="とほ",
        short_gloss="唐代诗人，中国诗史中心人物之一。",
        work_function="作为老师给“我”的汉诗阅读坐标出现。",
        long_note="在这里他主要是诗歌传统的门牌，不是详细展开的研究对象。",
    ),
    GlossaryEntry(
        term="室生犀星",
        reading="むろう さいせい",
        short_gloss="日本诗人、小说家，近代抒情诗重要人物。",
        work_function="作为朔太郎之外的另一条近代诗歌阅读线。",
        long_note="他的出现让“我”的阅读谱系不只停在朔太郎，也向更宽的近代抒情传统张开。",
        aliases=("犀星",),
    ),
    GlossaryEntry(
        term="シャルル・ボードレール",
        reading="charles baudelaire",
        short_gloss="法国诗人，《恶之花》作者。",
        work_function="把现代都市忧郁与“恶的美学”引进作品。",
        long_note="老师提到他时，实际上也在带“我”进入现代诗如何处理颓美、散文诗与都市感受的传统。",
        aliases=("ボードレール",),
    ),
    GlossaryEntry(
        term="オスカー・ワイルド",
        reading="oscar wilde",
        short_gloss="爱尔兰作家、戏剧家，《莎乐美》作者。",
        work_function="是老师解释“魔性”时拉出的西方文学参照。",
        long_note="在本作里，王尔德的作用主要是把“莎乐美”从宗教人物变成颓美派文学形象。",
        aliases=("ワイルド", "オスカー"),
    ),
    GlossaryEntry(
        term="ヘロディア",
        reading="herodias",
        short_gloss="圣经人物，莎乐美之母。",
        work_function="用于说明“莎乐美原型”和后世魔性形象并不完全相同。",
        long_note="老师特地提到她，是为了纠正“莎乐美天生就是魔性女”的误读。",
    ),
    GlossaryEntry(
        term="大江匡房",
        reading="おおえの まさふさ",
        short_gloss="平安后期学者、歌人。",
        work_function="把梦蝶典故进一步连进日本和歌传统。",
        long_note="他在这里的重要性不在生平，而在于证明“梦蝶”已进入日本古典诗歌的再书写。",
        aliases=("匡房",),
    ),
    GlossaryEntry(
        term="イマヌエル・カント",
        reading="immanuel kant",
        short_gloss="德国哲学家，近代美学与道德哲学代表人物。",
        work_function="让作品后段关于“作品与人格能否分离”的讨论进入哲学语言。",
        long_note="康德在这里不是装饰性引用，而是帮助人物尝试把艺术判断和道德判断分开。",
        aliases=("カント", "イマヌエル"),
    ),
    GlossaryEntry(
        term="ミルトン",
        reading="milton",
        short_gloss="通常指英国诗人约翰·弥尔顿，《失乐园》作者。",
        work_function="把蛇、知识欲与圣经叙事连到一起。",
        long_note="这里提到《失乐园》，重点在蛇如何诱使人类追求知识这一形象链。",
    ),
    GlossaryEntry(
        term="ガウス",
        reading="gauss",
        short_gloss="通常指德国数学家高斯。",
        work_function="把火星通信想象和近代科学史轻微地挂上钩。",
        long_note="老师借他提到的是“曾经真的有人设想和火星人通信”这条历史支线。",
    ),
    GlossaryEntry(
        term="蝶を夢む",
        reading="ちょうを ゆめむ",
        short_gloss="萩原朔太郎的诗题，可译“梦见蝴蝶”。",
        work_function="是本作处理蝶、梦与身份摇晃时的重要镜像文本。",
        long_note="它把朔太郎的现代感伤和庄子梦蝶的古典典故叠到了一起。",
    ),
    GlossaryEntry(
        term="桐の花",
        reading="きりのはな",
        short_gloss="北原白秋诗集名。",
        work_function="为枇杷、植物记忆和病后背景提供阅读上下文。",
        long_note="它在这里不仅是书名，也把白秋个人经历一并带进来了。",
        aliases=("花の桐",),
    ),
    GlossaryEntry(
        term="悪の華",
        reading="あくのはな",
        short_gloss="《恶之花》，波德莱尔诗集。",
        work_function="作为现代诗阅读坐标出现。",
        long_note="它让“我”的阅读从日本近代诗延伸到现代西方诗歌的阴影地带。",
    ),
    GlossaryEntry(
        term="パリの憂鬱",
        reading="paris no yuuutsu",
        short_gloss="《巴黎的忧郁》，波德莱尔散文诗集。",
        work_function="与《恶之花》一起提供“散文诗”这一形式参照。",
        long_note="它对应本作中诗和散文边界不断模糊的现象。",
    ),
    GlossaryEntry(
        term="春と修羅",
        reading="はるとしゅら",
        short_gloss="宫泽贤治诗集名，《春与修罗》。",
        work_function="为“修罗”一诗背后的怒意、恐惧与宇宙感提供背景。",
        long_note="老师提到它时，是在把“修罗”从单纯愤怒拉回宫泽贤治式的宇宙性裂痕。",
    ),
]


GROUP_RE = re.compile(r"^##\s+(第(\d+)组通信)｜(.+)$")
SUPPLEMENT_RE = re.compile(r"^##\s+(补遗)｜(.+)$")
UNIT_RE = re.compile(r"^###\s+单元\s+([^｜]+)｜([^｜]+)｜(.+)$")
PARA_RE = re.compile(r"^####\s+([PL]\d+)$")
SOURCE_REF_RE = re.compile(r"^>\s+原编号：(.+)$")
ANNOTATED_TERM_RE = re.compile(r"\{([^|}]+)\|([^}]+)\}")


def extract_inline_payload(line: str, prefix: str) -> str:
    payload = line[len(prefix) :].strip()
    if payload.startswith("`") and payload.endswith("`"):
        return payload[1:-1]
    return payload


def extract_fenced_block(lines: list[str], start: int) -> tuple[str, int]:
    i = start
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i >= len(lines) or not lines[i].startswith("```"):
        raise ValueError(f"Expected fenced block at line {start + 1}")
    fence = lines[i]
    i += 1
    block: list[str] = []
    while i < len(lines) and lines[i] != fence and lines[i].strip() != "```":
        block.append(lines[i])
        i += 1
    if i >= len(lines):
        raise ValueError("Unclosed fenced block")
    i += 1
    return "\n".join(block).rstrip(), i


def extract_source_or_target(lines: list[str], start: int, label: str) -> tuple[str, int]:
    i = start
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i >= len(lines):
        raise ValueError(f"Missing {label}")
    prefix = f"{label}："
    line = lines[i]
    if not line.startswith(prefix):
        raise ValueError(f"Expected {label} at line {i + 1}")
    if line.strip() == prefix:
        return extract_fenced_block(lines, i + 1)
    return extract_inline_payload(line, prefix).rstrip(), i + 1


def glossary_payload(entry: GlossaryEntry, matched_text: str) -> dict[str, str]:
    return {
        "term": entry.term,
        "matched_text": matched_text,
        "reading": entry.reading,
        "short_gloss": entry.short_gloss,
        "work_function": entry.work_function,
        "long_note": entry.long_note,
    }


def fallback_payload(term: str, reading: str, matched_text: str) -> dict[str, str]:
    return {
        "term": term,
        "matched_text": matched_text,
        "reading": reading,
        "short_gloss": f"原稿中已标注读音：{reading}。",
        "work_function": "作者主动加了注音，说明它不是特别常见、可能易误读，或需要保留字形与读音的并置效果。",
        "long_note": "当前尚未补入详细人工词条。前端至少应显示注音，并可将其视为后续优先补写的疑难词候选。",
    }


def detect_term_notes(source_md: str, target_md: str) -> list[dict[str, str]]:
    haystack = f"{source_md}\n{target_md}"
    matches: list[tuple[int, str, GlossaryEntry]] = []
    for entry in GLOSSARY:
        seen_index: int | None = None
        seen_alias = entry.term
        for alias in (entry.term, *entry.aliases):
            idx = haystack.find(alias)
            if idx != -1 and (seen_index is None or idx < seen_index):
                seen_index = idx
                seen_alias = alias
        if seen_index is not None:
            matches.append((seen_index, seen_alias, entry))
    matched_terms = {entry.term for _, _, entry in matches}
    combined_notes: list[tuple[int, dict[str, str]]] = [
        (index, glossary_payload(entry, alias))
        for index, alias, entry in matches
    ]

    for annotated_match in ANNOTATED_TERM_RE.finditer(haystack):
        term, reading = annotated_match.groups()
        if term in matched_terms:
            continue
        combined_notes.append(
            (
                annotated_match.start(),
                fallback_payload(term, reading, term),
            )
        )
        matched_terms.add(term)

    combined_notes.sort(key=lambda item: item[0])
    return [note for _, note in combined_notes]


def parse_file(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    groups: list[dict] = []
    current_group: dict | None = None
    current_unit: dict | None = None
    i = 0

    while i < len(lines):
        line = lines[i]

        group_match = GROUP_RE.match(line)
        supplement_match = SUPPLEMENT_RE.match(line)
        unit_match = UNIT_RE.match(line)
        para_match = PARA_RE.match(line)
        source_ref_match = SOURCE_REF_RE.match(line)

        if group_match:
            label, group_num, date_label = group_match.groups()
            current_group = {
                "group_id": f"G{int(group_num):02d}",
                "group_label": label,
                "date_label": date_label.strip(),
                "source_file": path.name,
                "units": [],
            }
            groups.append(current_group)
            current_unit = None
            i += 1
            continue

        if supplement_match:
            label, date_label = supplement_match.groups()
            current_group = {
                "group_id": "EX",
                "group_label": label,
                "date_label": date_label.strip(),
                "source_file": path.name,
                "units": [],
            }
            groups.append(current_group)
            current_unit = None
            i += 1
            continue

        if unit_match and current_group is not None:
            unit_id, speaker, unit_type = unit_match.groups()
            current_unit = {
                "unit_id": unit_id.strip(),
                "speaker": speaker.strip(),
                "type": unit_type.strip(),
                "source_refs": [],
                "paragraphs": [],
            }
            current_group["units"].append(current_unit)
            i += 1
            continue

        if source_ref_match and current_unit is not None:
            refs = [part.strip() for part in source_ref_match.group(1).split(",")]
            current_unit["source_refs"] = refs
            i += 1
            continue

        if para_match and current_unit is not None:
            para_label = para_match.group(1)
            source_md, i = extract_source_or_target(lines, i + 1, "原文")
            target_md, i = extract_source_or_target(lines, i, "译文")
            current_unit["paragraphs"].append(
                {
                    "para_id": f"{current_unit['unit_id']}-{para_label}",
                    "para_label": para_label,
                    "render_mode": "block" if para_label.startswith("P") else "line",
                    "source_md": source_md,
                    "target_md": target_md,
                    "notes": [],
                    "term_notes": detect_term_notes(source_md, target_md),
                }
            )
            continue

        i += 1

    return groups


def strip_markdown_title(text: str) -> str:
    return text.strip().removeprefix("**").removesuffix("**").strip()


def is_explicit_poem_title(text: str) -> bool:
    return bool(re.fullmatch(r"\*\*.+\*\*", text.strip()))


def build_paragraph_search_text(paragraph: dict) -> str:
    return "\n".join(
        [
            paragraph["source_md"],
            paragraph["target_md"],
            *(
                f"{note['term']} {note['short_gloss']} {note['long_note']}"
                for note in paragraph["term_notes"]
            ),
        ]
    ).lower()


def build_display_units(group: dict) -> list[dict]:
    result: list[dict] = []

    for unit in group["units"]:
        previous = result[-1] if result else None
        is_poem = unit["type"] == "附诗"
        starts_with_title = bool(unit["paragraphs"] and unit["paragraphs"][0]["source_md"])
        explicit_title = (
            starts_with_title
            and is_explicit_poem_title(unit["paragraphs"][0]["source_md"])
        )
        should_append = (
            is_poem
            and previous is not None
            and previous["type"] == "附诗"
            and previous["speaker"] == unit["speaker"]
            and not explicit_title
        )

        if should_append:
            previous["paragraphs"].extend(dict(paragraph) for paragraph in unit["paragraphs"])
            previous["source_refs"].extend(unit["source_refs"])
            previous["unit_ids"].append(unit["unit_id"])
            continue

        result.append(
            {
                "unit_id": unit["unit_id"],
                "unit_ids": [unit["unit_id"]],
                "speaker": unit["speaker"],
                "type": unit["type"],
                "source_refs": list(unit["source_refs"]),
                "paragraphs": [dict(paragraph) for paragraph in unit["paragraphs"]],
            }
        )

    normalized: list[dict] = []
    for unit in result:
        if unit["type"] != "附诗" or not unit["paragraphs"]:
            normalized.append(
                {
                    **unit,
                    "titleSource": "",
                    "titleTarget": "",
                    "titleLabel": "",
                    "titleTermNotes": [],
                }
            )
            continue

        first, *rest = unit["paragraphs"]
        title_source = strip_markdown_title(first["source_md"])
        title_target = strip_markdown_title(first["target_md"])
        normalized.append(
            {
                **unit,
                "titleSource": title_source,
                "titleTarget": title_target,
                "titleLabel": title_source or title_target,
                "titleTermNotes": list(first["term_notes"]),
                "paragraphs": rest,
            }
        )

    return normalized


def summarize_display_units(display_units: list[dict]) -> dict[str, int]:
    unit_count = len(display_units)
    para_count = sum(len(unit["paragraphs"]) for unit in display_units)
    note_count = sum(
        len(
            [
                note
                for note in paragraph["term_notes"]
                if all(marker not in note["long_note"] for marker in PLACEHOLDER_MARKERS)
            ]
        )
        for unit in display_units
        for paragraph in unit["paragraphs"]
    )
    return {
        "unitCount": unit_count,
        "paraCount": para_count,
        "noteCount": note_count,
    }


PLACEHOLDER_MARKERS = (
    "当前尚未补入详细人工词条",
    "前端至少应显示注音",
    "后续优先补写的疑难词候选",
)


def build_preview_exports(payload: dict) -> tuple[dict, dict[str, dict]]:
    preview_groups: list[dict] = []
    preview_group_files: dict[str, dict] = {}

    for group in payload["groups"]:
        display_units = build_display_units(group)
        for unit in display_units:
            for paragraph in unit["paragraphs"]:
                paragraph["search_text"] = build_paragraph_search_text(paragraph)

        stats = summarize_display_units(display_units)
        poem_titles = [
            unit["titleLabel"]
            for unit in display_units
            if unit["type"] == "附诗" and unit["titleLabel"]
        ]
        search_units = []
        for unit in display_units:
            unit_search = "\n".join(
                filter(
                    None,
                    [
                        unit["titleSource"],
                        unit["titleTarget"],
                        *(paragraph["search_text"] for paragraph in unit["paragraphs"]),
                    ],
                )
            ).lower()
            search_units.append(
                {
                    "unit_id": unit["unit_id"],
                    "speaker": unit["speaker"],
                    "type": unit["type"],
                    "source_refs": unit["source_refs"],
                    "titleLabel": unit["titleLabel"],
                    "paragraph_count": len(unit["paragraphs"]),
                    "search_text": unit_search,
                }
            )

        group_file = f"preview_groups/{group['group_id']}.json"
        preview_groups.append(
            {
                "group_id": group["group_id"],
                "group_label": group["group_label"],
                "date_label": group["date_label"],
                "source_file": group["source_file"],
                "group_file": group_file,
                "poem_titles": poem_titles,
                "stats": stats,
                "search_units": search_units,
            }
        )
        preview_group_files[group["group_id"]] = {
            "group_id": group["group_id"],
            "group_label": group["group_label"],
            "date_label": group["date_label"],
            "source_file": group["source_file"],
            "display_units": display_units,
        }

    index_payload = {
        "work": payload["work"],
        "edition": "preview_index",
        "generated_at": payload["generated_at"],
        "source_files": payload["source_files"],
        "groups": preview_groups,
    }
    return index_payload, preview_group_files


def build_payload() -> dict:
    groups: list[dict] = []
    for path in SOURCE_FILES:
        groups.extend(parse_file(path))

    glossary_index = {
        entry.term: {
            "term": entry.term,
            "reading": entry.reading,
            "short_gloss": entry.short_gloss,
            "work_function": entry.work_function,
            "long_note": entry.long_note,
            "aliases": list(entry.aliases),
        }
        for entry in GLOSSARY
    }
    for group in groups:
        for unit in group["units"]:
            for paragraph in unit["paragraphs"]:
                for note in paragraph["term_notes"]:
                    glossary_index.setdefault(
                        note["term"],
                        {
                            "term": note["term"],
                            "reading": note["reading"],
                            "short_gloss": note["short_gloss"],
                            "work_function": note["work_function"],
                            "long_note": note["long_note"],
                            "aliases": [],
                        },
                    )

    return {
        "work": "一人称",
        "edition": "bilingual_parallel",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_files": [path.name for path in SOURCE_FILES],
        "groups": groups,
        "term_glossary": glossary_index,
    }


def build_stats(payload: dict) -> dict:
    groups = payload["groups"]
    units = sum(len(group["units"]) for group in groups)
    paragraphs = sum(
        len(unit["paragraphs"])
        for group in groups
        for unit in group["units"]
    )
    paragraphs_with_term_notes = 0
    term_frequency: dict[str, int] = {}

    for group in groups:
        for unit in group["units"]:
            for paragraph in unit["paragraphs"]:
                if paragraph["term_notes"]:
                    paragraphs_with_term_notes += 1
                for note in paragraph["term_notes"]:
                    term = note["term"]
                    term_frequency[term] = term_frequency.get(term, 0) + 1

    return {
        "generated_at": payload["generated_at"],
        "group_count": len(groups),
        "unit_count": units,
        "paragraph_count": paragraphs,
        "paragraphs_with_term_notes": paragraphs_with_term_notes,
        "term_note_hits": sum(term_frequency.values()),
        "term_frequency": dict(
            sorted(term_frequency.items(), key=lambda item: (-item[1], item[0]))
        ),
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = build_payload()
    stats = build_stats(payload)
    preview_index, preview_group_files = build_preview_exports(payload)

    bilingual_path = OUTPUT_DIR / "双语对照_前端数据.json"
    glossary_path = OUTPUT_DIR / "疑难词注释_前端词库.json"
    stats_path = OUTPUT_DIR / "疑难词注释_覆盖统计.json"
    PREVIEW_GROUPS_DIR.mkdir(parents=True, exist_ok=True)
    for old_file in PREVIEW_GROUPS_DIR.glob("*.json"):
        old_file.unlink()

    bilingual_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    glossary_path.write_text(
        json.dumps(payload["term_glossary"], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    stats_path.write_text(
        json.dumps(stats, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    PREVIEW_INDEX_PATH.write_text(
        json.dumps(preview_index, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    for group_id, group_payload in preview_group_files.items():
        (PREVIEW_GROUPS_DIR / f"{group_id}.json").write_text(
            json.dumps(group_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    print(bilingual_path)
    print(glossary_path)
    print(stats_path)
    print(PREVIEW_INDEX_PATH)


if __name__ == "__main__":
    main()
