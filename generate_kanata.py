#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kanata Chord Config Generator
==============================
根据 Group-A（左手）和 Group-B（右手）的映射规则，自动生成 kanata 的 defchords 配置。

支持生成：
  1. 精简版：仅同位置组合（推荐，约 95 条）
  2. 行内版：同行交叉组合（约 175 条）
  3. 交叉版：全部单键+双键交叉（约 455 条）
  4. 完整版：含混合组合（约 960 条）

用法：
  python3 generate_kanata.py
"""

import os
from typing import List, Tuple


class KanataChordGenerator:
    def __init__(self):
        # ========== Group-A：左手键位 ==========
        self.group_a_single: List[Tuple[str, str]] = [
            ("q", "q"), ("w", "w"), ("e", "e"), ("r", "r"), ("t", "t"),
            ("a", "a"), ("s", "s"), ("d", "d"), ("f", "f"), ("g", "g"),
            ("z", "z"), ("x", "x"), ("c", "c"), ("v", "v"), ("b", "b"),
        ]

        self.group_a_double: List[Tuple[List[str], str]] = [
            (["e", "f"], "y"),      # 0
            (["e", "r"], "u"),      # 1
            (["w", "e"], "i"),      # 2
            (["w", "r"], "o"),      # 3
            (["q", "r"], "p"),      # 4
            (["w", "f"], "h"),      # 5
            (["d", "f"], "j"),      # 6
            (["s", "d"], "k"),      # 7
            (["s", "f"], "l"),      # 8
            (["a", "f"], ";"),      # 9
            (["s", "c"], "n"),      # 10
            (["c", "v"], "m"),      # 11
            (["x", "c"], ","),      # 12
            (["x", "v"], "."),      # 13
            (["z", "v"], "/"),      # 14
        ]

        # ========== Group-B：右手键位 ==========
        self.group_b_single: List[Tuple[str, str]] = [
            ("p", "q"),     # 0  对应 q
            ("o", "w"),     # 1  对应 w
            ("i", "e"),     # 2  对应 e
            ("u", "r"),     # 3  对应 r
            ("y", "t"),     # 4  对应 t
            (";", "a"),     # 5  对应 a
            ("l", "s"),     # 6  对应 s
            ("k", "d"),     # 7  对应 d
            ("j", "f"),     # 8  对应 f
            ("h", "g"),     # 9  对应 g
            ("/", "z"),     # 10 对应 z
            (".", "x"),     # 11 对应 x
            (",", "c"),     # 12 对应 c
            ("m", "v"),     # 13 对应 v
            ("n", "b"),     # 14 对应 b
        ]

        self.group_b_double: List[Tuple[List[str], str]] = [
            (["j", "i"], "y"),      # 0
            (["u", "i"], "u"),      # 1
            (["i", "o"], "i"),      # 2
            (["u", "o"], "o"),      # 3
            (["p", "u"], "p"),      # 4
            (["j", "o"], "h"),      # 5
            (["j", "k"], "j"),      # 6
            (["k", "l"], "k"),      # 7
            (["j", "l"], "l"),      # 8
            (["j", ";"], ";"),      # 9
            ([",", "l"], "n"),      # 10
            (["m", ","], "m"),      # 11
            ([",", "."], ","),      # 12
            (["m", "."], "."),      # 13
            (["m", "/"], "/"),      # 14
        ]

        self.row_indices = {
            "row1": [0, 1, 2, 3, 4],
            "row2": [5, 6, 7, 8, 9],
            "row3": [10, 11, 12, 13, 14],
        }

    # ------------------------------------------------------------------
    def _fmt(self, keys: List[str], output: str) -> str:
        return f"  ({' '.join(keys)}) {output}"

    def _single_single(self, same: bool = True, cross: bool = False) -> List[str]:
        lines = []
        for i, (lk, lo) in enumerate(self.group_a_single):
            for j, (rk, ro) in enumerate(self.group_b_single):
                if same and cross:
                    # 全部组合
                    pass
                elif same and not cross:
                    if i != j:
                        continue
                elif not same and cross:
                    if i == j:
                        continue
                else:
                    continue  # same=False, cross=False -> 空

                out = f"(macro {lo} {lo})" if i == j else f"(macro {lo} {ro})"
                lines.append(self._fmt([lk, rk], out))
        return lines

    def _double_double(self, same: bool = True, cross: bool = False) -> List[str]:
        lines = []
        for i, (lk, lo) in enumerate(self.group_a_double):
            for j, (rk, ro) in enumerate(self.group_b_double):
                if same and cross:
                    pass
                elif same and not cross:
                    if i != j:
                        continue
                elif not same and cross:
                    if i == j:
                        continue
                else:
                    continue

                out = f"(macro {lo} {lo})" if i == j else f"(macro {lo} {ro})"
                lines.append(self._fmt(lk + rk, out))
        return lines

    def _single_double(self, a_s_b_d: bool = True, a_d_b_s: bool = True) -> List[str]:
        lines = []
        if a_s_b_d:
            for lk, lo in self.group_a_single:
                for rk, ro in self.group_b_double:
                    lines.append(self._fmt([lk] + rk, f"(macro {lo} {ro})"))
        if a_d_b_s:
            for lk, lo in self.group_a_double:
                for rk, ro in self.group_b_single:
                    lines.append(self._fmt(lk + [rk], f"(macro {lo} {ro})"))
        return lines

    def _row_limited(self, rows: List[str]) -> List[str]:
        lines = []
        allowed = set()
        for r in rows:
            allowed.update(self.row_indices.get(r, []))
        # 单键行内交叉
        for i in allowed:
            for j in allowed:
                if i == j:
                    continue
                lk, lo = self.group_a_single[i]
                rk, ro = self.group_b_single[j]
                lines.append(self._fmt([lk, rk], f"(macro {lo} {ro})"))
        # 双键行内交叉
        for i in allowed:
            for j in allowed:
                if i == j:
                    continue
                lk, lo = self.group_a_double[i]
                rk, ro = self.group_b_double[j]
                lines.append(self._fmt(lk + rk, f"(macro {lo} {ro})"))
        return lines

    # ------------------------------------------------------------------
    def generate(self, *,
                 a_s: bool = True, b_s: bool = True,
                 a_d: bool = True, b_d: bool = True,
                 same_s: bool = True, same_d: bool = True,
                 cross_s: bool = False, cross_d: bool = False,
                 mixed: bool = False, rows: List[str] = None) -> str:
        sections = []

        if a_s:
            sections.append(";; === Group-A: 左手单键 ===")
            for k, o in self.group_a_single:
                sections.append(self._fmt([k], o))

        if b_s:
            sections.append("\n;; === Group-B: 右手单键 ===")
            for k, o in self.group_b_single:
                sections.append(self._fmt([k], o))

        if a_d:
            sections.append("\n;; === Group-A: 左手双键 ===")
            for k, o in self.group_a_double:
                sections.append(self._fmt(k, o))

        if b_d:
            sections.append("\n;; === Group-B: 右手双键 ===")
            for k, o in self.group_b_double:
                sections.append(self._fmt(k, o))

        if same_s:
            sections.append("\n;; === A&B: 同位置单键 → 双写 ===")
            sections.extend(self._single_single(same=True, cross=False))

        if same_d:
            sections.append("\n;; === A&B: 同位置双键 → 双写 ===")
            sections.extend(self._double_double(same=True, cross=False))

        if rows:
            sections.append(f"\n;; === A&B: 行内交叉 ({', '.join(rows)}) ===")
            sections.extend(self._row_limited(rows))
        else:
            if cross_s:
                sections.append("\n;; === A&B: 交叉单键 → 组合输出 ===")
                sections.extend(self._single_single(same=False, cross=True))
            if cross_d:
                sections.append("\n;; === A&B: 交叉双键 → 组合输出 ===")
                sections.extend(self._double_double(same=False, cross=True))

        if mixed:
            sections.append("\n;; === A&B: 单键+双键混合 → 组合输出 ===")
            sections.extend(self._single_double())

        return "\n".join(sections)

    def write(self, path: str, timeout: int = 200, **kwargs) -> int:
        body = self.generate(**kwargs)
        full = f"(defchords chording {timeout}\n{body}\n)"
        with open(path, "w", encoding="utf-8") as f:
            f.write(full)
        return body.count("\n  (")


if __name__ == "__main__":
    gen = KanataChordGenerator()
    out_dir = os.path.dirname(os.path.abspath(__file__))

    print("=" * 60)
    print("Kanata Chord 配置生成器")
    print("=" * 60)

    cnt = gen.write(os.path.join(out_dir, "kanata_chords_minimal.kbd"),
                    cross_s=False, cross_d=False, mixed=False)
    print(f"[OK] kanata_chords_minimal.kbd   ({cnt} 条)")

    cnt = gen.write(os.path.join(out_dir, "kanata_chords_row.kbd"),
                    cross_s=False, cross_d=False, mixed=False, rows=["row1", "row2", "row3"])
    print(f"[OK] kanata_chords_row.kbd       ({cnt} 条)")

    cnt = gen.write(os.path.join(out_dir, "kanata_chords_cross.kbd"),
                    cross_s=True, cross_d=True, mixed=False)
    print(f"[OK] kanata_chords_cross.kbd     ({cnt} 条)")

    cnt = gen.write(os.path.join(out_dir, "kanata_chords_full.kbd"),
                    cross_s=True, cross_d=True, mixed=True)
    print(f"[OK] kanata_chords_full.kbd      ({cnt} 条)")

    print("=" * 60)
    print("生成完毕。建议先用 minimal 或 row 版本测试。")
    print("=" * 60)

