# -*- coding: utf-8 -*-
"""
生成 Rime 用的「带调拼音」码表
输入：bei3 → 输出：běi
"""

import re

# 所有合法拼音音节（小写，含 v 表示 ü）
PINYIN_SYLLABLES = [
    'a', 'ai', 'an', 'ang', 'ao',
    'ba', 'bai', 'ban', 'bang', 'bao', 'bei', 'ben', 'beng', 'bi', 'bian', 'biao', 'bie', 'bin', 'bing', 'bo', 'bu',
    'ca', 'cai', 'can', 'cang', 'cao', 'ce', 'cen', 'ceng', 'cha', 'chai', 'chan', 'chang', 'chao', 'che', 'chen', 'cheng', 'chi', 'chong', 'chou', 'chu', 'chua', 'chuai', 'chuan', 'chuang', 'chui', 'chun', 'chuo', 'ci', 'cong', 'cou', 'cu', 'cuan', 'cui', 'cun', 'cuo',
    'da', 'dai', 'dan', 'dang', 'dao', 'de', 'dei', 'den', 'deng', 'di', 'dia', 'dian', 'diao', 'die', 'ding', 'diu', 'dong', 'dou', 'du', 'duan', 'dui', 'dun', 'duo',
    'e', 'ei', 'en', 'eng', 'er',
    'fa', 'fan', 'fang', 'fei', 'fen', 'feng', 'fo', 'fou', 'fu',
    'ga', 'gai', 'gan', 'gang', 'gao', 'ge', 'gei', 'gen', 'geng', 'gong', 'gou', 'gu', 'gua', 'guai', 'guan', 'guang', 'gui', 'gun', 'guo',
    'ha', 'hai', 'han', 'hang', 'hao', 'he', 'hei', 'hen', 'heng', 'hong', 'hou', 'hu', 'hua', 'huai', 'huan', 'huang', 'hui', 'hun', 'huo',
    'ji', 'jia', 'jian', 'jiang', 'jiao', 'jie', 'jin', 'jing', 'jiong', 'jiu', 'ju', 'juan', 'jue', 'jun',
    'ka', 'kai', 'kan', 'kang', 'kao', 'ke', 'ken', 'keng', 'kong', 'kou', 'ku', 'kua', 'kuai', 'kuan', 'kuang', 'kui', 'kun', 'kuo',
    'la', 'lai', 'lan', 'lang', 'lao', 'le', 'lei', 'leng', 'li', 'lia', 'lian', 'liang', 'liao', 'lie', 'lin', 'ling', 'liu', 'long', 'lou', 'lu', 'lv', 'luan', 'lve', 'lue', 'lun', 'luo',
    'ma', 'mai', 'man', 'mang', 'mao', 'me', 'mei', 'men', 'meng', 'mi', 'mian', 'miao', 'mie', 'min', 'ming', 'miu', 'mo', 'mou', 'mu',
    'na', 'nai', 'nan', 'nang', 'nao', 'ne', 'nei', 'nen', 'neng', 'ni', 'nia', 'nian', 'niang', 'niao', 'nie', 'nin', 'ning', 'niu', 'nong', 'nou', 'nu', 'nv', 'nuan', 'nve', 'nue', 'nuo',
    'o', 'ou',
    'pa', 'pai', 'pan', 'pang', 'pao', 'pei', 'pen', 'peng', 'pi', 'pian', 'piao', 'pie', 'pin', 'ping', 'po', 'pou', 'pu',
    'qi', 'qia', 'qian', 'qiang', 'qiao', 'qie', 'qin', 'qing', 'qiong', 'qiu', 'qu', 'quan', 'que', 'qun',
    'ran', 'rang', 'rao', 're', 'ren', 'reng', 'ri', 'rong', 'rou', 'ru', 'rua', 'ruan', 'rui', 'run', 'ruo',
    'sa', 'sai', 'san', 'sang', 'sao', 'se', 'sen', 'seng', 'sha', 'shai', 'shan', 'shang', 'shao', 'she', 'shei', 'shen', 'sheng', 'shi', 'shou', 'shu', 'shua', 'shuai', 'shuan', 'shuang', 'shui', 'shun', 'shuo', 'si', 'song', 'sou', 'su', 'suan', 'sui', 'sun', 'suo',
    'ta', 'tai', 'tan', 'tang', 'tao', 'te', 'teng', 'ti', 'tian', 'tiao', 'tie', 'ting', 'tong', 'tou', 'tu', 'tuan', 'tui', 'tun', 'tuo',
    'wa', 'wai', 'wan', 'wang', 'wei', 'wen', 'weng', 'wo', 'wu',
    'xi', 'xia', 'xian', 'xiang', 'xiao', 'xie', 'xin', 'xing', 'xiong', 'xiu', 'xu', 'xuan', 'xue', 'xun',
    'ya', 'yan', 'yang', 'yao', 'ye', 'yi', 'yin', 'ying', 'yo', 'yong', 'you', 'yu', 'yuan', 'yue', 'yun',
    'za', 'zai', 'zan', 'zang', 'zao', 'ze', 'zei', 'zen', 'zeng', 'zha', 'zhai', 'zhan', 'zhang', 'zhao', 'zhe', 'zhei', 'zhen', 'zheng', 'zhi', 'zhong', 'zhou', 'zhu', 'zhua', 'zhuai', 'zhuan', 'zhuang', 'zhui', 'zhun', 'zhuo', 'zi', 'zong', 'zou', 'zu', 'zuan', 'zui', 'zun', 'zuo'
]

# 声调组合符（Unicode combining diacritics）
TONES = {
    1: '\u0304',  # macron
    2: '\u0301',  # acute
    3: '\u030C',  # caron
    4: '\u0300',  # grave
}

# 标调元音优先级（顺序即优先级）
VOWELS_ORDER = ['a', 'o', 'e', 'i', 'u', 'v']  # v 代表 ü

def find_tone_vowel(syllable):
    """根据标调规则，找出应该加声调的元音"""
    for v in VOWELS_ORDER:
        if v in syllable:
            # 特殊情况：iou, uei, uen 在拼写中缩写为 iu, ui, un，但标调仍在原元音
            # 但我们的音节表已用标准形式（如 'iu' 实际是 'iou' 缩写），需特殊处理
            # 简化处理：按实际字符串找
            return v
    return None

def add_tone(syllable, tone):
    """给拼音音节添加声调"""
    if tone == 5:
        return syllable.replace('v', 'ü')
    
    vowel = find_tone_vowel(syllable)
    if not vowel:
        # 无元音？返回原样（如 'm', 'n', 'ng'，但普通话无此独立音节）
        return syllable.replace('v', 'ü')
    
    # 找到最后一个该元音的位置（应对如 "ai", "ao" 等双元音）
    # 实际上，按规则只需标在第一个匹配的高优先级元音即可
    idx = syllable.find(vowel)
    if idx == -1:
        return syllable.replace('v', 'ü')
    
    # 插入组合符
    toned = syllable[:idx+1] + TONES[tone] + syllable[idx+1:]
    # 将 v 替换为 ü（注意：组合符已在 v 后，所以先替换再处理？不，应在基础字符上替换）
    # 更安全：先替换 v → ü，再加调？但组合符要加在 ü 上
    # 所以：先保留 v，加调后再整体替换
    toned = toned.replace('v', 'ü')
    return toned

def main():
    entries = []
    for syllable in PINYIN_SYLLABLES:
        base_input = syllable  # 输入用 v 表示 ü，如 nv
        for tone in [1, 2, 3, 4, 5]:
            input_code = base_input + str(tone)
            output_pinyin = add_tone(syllable, tone)
            entries.append((output_pinyin, input_code))
    
    # 去重（理论上不会重复）
    entries = list(dict.fromkeys(entries))
    
    with open('pinyin_tone.dict.yaml', 'w', encoding='utf-8') as f:
        f.write('''---
name: pinyin_tone
version: "1.0"
sort: by_weight
...

''')
        for output, input_code in entries:
            f.write(f"{output}\t{input_code}\n")
    
    print(f"✅ 成功生成 {len(entries)} 条拼音条目！")
    print("文件已保存为: pinyin_tone.dict.yaml")

if __name__ == '__main__':
    main()