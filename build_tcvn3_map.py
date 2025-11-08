# -*- coding: utf-8 -*-
"""
Build & test offline TCVN3→Unicode map from VietUnicode (official tables).

Usage:
  python build_tcvn3_map.py --build
  python build_tcvn3_map.py --test "Thµnh phè Hç ChÝ Minh"
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from typing import Dict, List
from io import StringIO

# Optional but recommended: requests + pandas + bs4
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Optional: chardet for encoding detection
import importlib.util
HAS_CHARDET = importlib.util.find_spec("chardet") is not None


# Một tập ký tự “hay gặp” trong TCVN3 (.VnTime)
TCVN3_HINTS = set("µ¸¶·¹¨»¾¼½Æ©ÇÊÈÉË®ÌÐÎÏÑªÒÕÓÔÖ×ÝØÜÞßãáâä«åèæçé¬êíëìîïóñòôõøö÷ùúýûüþ¡¢§£¤¥¦")

# Regex 1 ký tự Latin có dấu (Unicode mở rộng)
RE_UNI_CHAR = re.compile(r"^[\u00C0-\u1EF9]$")  # khoảng Latin-1 + Latin Extended có dấu

def guess_cols(df: pd.DataFrame) -> tuple[int, int]:
    """
    Trả về (unicode_col_idx, tcvn3_col_idx) dựa trên heuristic:
    - Cột Unicode: tỉ lệ cao các ô là đúng 1 ký tự Latin có dấu.
    - Cột TCVN3 : tỉ lệ cao các ô là đúng 1 ký tự thuộc TCVN3_HINTS.
    """

    def score_unicode(col: pd.Series) -> float:
        cnt = 0
        ok = 0
        for v in col.dropna().astype(str):
            v = v.strip()
            if len(v) == 1:
                cnt += 1
                if RE_UNI_CHAR.match(v):
                    ok += 1
        return ok / cnt if cnt else 0.0

    def score_tcvn3(col: pd.Series) -> float:
        cnt = 0
        ok = 0
        for v in col.dropna().astype(str):
            v = v.strip()
            if len(v) == 1:
                cnt += 1
                if v in TCVN3_HINTS:
                    ok += 1
        return ok / cnt if cnt else 0.0

    uni_idx = max(df.columns, key=lambda c: score_unicode(df[c]))
    tcvn_idx = max(df.columns, key=lambda c: score_tcvn3(df[c]))

    # Nếu trùng nhau, thử cột nhì
    if uni_idx == tcvn_idx:
        # sắp xếp tất cả theo điểm rồi lấy phần tử thứ hai
        uni_sorted = sorted(df.columns, key=lambda c: score_unicode(df[c]), reverse=True)
        tcvn_sorted = sorted(df.columns, key=lambda c: score_tcvn3(df[c]), reverse=True)
        uni_idx = uni_sorted[0]
        # tìm cột tcvn khác cột unicode
        tcvn_idx = next((c for c in tcvn_sorted if c != uni_idx), tcvn_sorted[0])

    # thô bạo nhưng hiệu quả: kiểm tra ngưỡng tối thiểu
    if score_unicode(df[uni_idx]) < 0.2 or score_tcvn3(df[tcvn_idx]) < 0.2:
        raise RuntimeError("Không đoán được cột Unicode/TCVN3 (điểm quá thấp).")

    return int(uni_idx), int(tcvn_idx)


VU_URL = "https://vietunicode.sourceforge.net/charset/"
OUT_JSON = Path("tcvn3_map.json")
OUT_CSV = Path("tcvn3_map.csv")

def debug_headers():
    html = fetch_html(VU_URL)
    # Kiểm tra encoding
    print(f"HTML length: {len(html)}")
    print(f"Sample HTML (first 500 chars): {repr(html[:500])}")
    print(f"Has Vietnamese chars: {any(ord(c) >= 0x00C0 and ord(c) <= 0x1EF9 for c in html[:1000])}")
    print()
    
    dfs = extract_tables(html)
    for i, df in enumerate(dfs):
        cols = [str(c).strip().upper() for c in df.columns]
        print(f"[Table {i}] shape={df.shape}, columns -> {cols}")
        # In vài dòng đầu để debug
        print("  First 3 rows:")
        print(df.head(3))
        # In raw values để kiểm tra encoding
        if len(df) > 0:
            print(f"  Sample values from column 0 (first row): {repr(df.iloc[0, 0])}")
            print(f"  Sample values from column 8 (TCVN3, first row): {repr(df.iloc[0, 8]) if df.shape[1] > 8 else 'N/A'}")
        print()

def fix_double_encoding(text: str) -> str:
    """
    Sửa lỗi double-encoding: nếu text bị decode sai (như 'Ã\x80' thay vì 'À'),
    thử fix bằng cách encode lại thành bytes rồi decode đúng.
    
    Ví dụ: 'Ã\x80' là UTF-8 bytes [0xC3, 0x80] bị decode như ISO-8859-1
    -> encode lại như ISO-8859-1 -> bytes [0xC3, 0x80] -> decode như UTF-8 -> 'À'
    """
    if not text:
        return text
    
    try:
        # Kiểm tra xem có dấu hiệu của double-encoding không
        # Nếu có 'Ã' (0xC3) kèm theo các ký tự khác, có thể là UTF-8 bị decode như ISO-8859-1
        has_suspicious_chars = any(c in text for c in ['Ã', 'â', 'Â', 'â€', 'Â¢', 'Â£'])
        
        if has_suspicious_chars:
            # Thử encode lại như ISO-8859-1 (vì có thể đã bị decode sai từ UTF-8)
            try:
                bytes_data = text.encode('iso-8859-1', errors='strict')
                # Decode lại như UTF-8
                fixed = bytes_data.decode('utf-8', errors='strict')
                # Kiểm tra xem có ký tự tiếng Việt hợp lệ không
                sample = fixed[:min(500, len(fixed))]
                vietnamese_count = sum(1 for c in sample if ord(c) >= 0x00C0 and ord(c) <= 0x1EF9)
                if vietnamese_count > 10:  # Có ít nhất 10 ký tự tiếng Việt
                    return fixed
            except (UnicodeEncodeError, UnicodeDecodeError):
                pass
            
            # Thử cách khác: nếu text có pattern như 'Ã\x80', thử fix từng phần
            # 'Ã' = 0xC3, nếu đi kèm với ký tự có mã thấp, có thể là UTF-8 sequence
            if len(text) >= 2 and text[0] == 'Ã':
                try:
                    # Thử lấy byte đầu và byte thứ 2
                    byte1 = ord(text[0])  # 0xC3
                    if len(text) > 1:
                        byte2 = ord(text[1]) if isinstance(text[1], str) else text[1]
                        # Nếu byte2 trong range hợp lệ cho UTF-8 continuation
                        if 0x80 <= byte2 <= 0xBF:
                            # Đây là UTF-8 sequence bị decode sai
                            bytes_seq = bytes([byte1, byte2])
                            fixed_char = bytes_seq.decode('utf-8')
                            # Thay thế 2 ký tự đầu bằng ký tự đúng
                            if len(text) > 2:
                                return fixed_char + fix_double_encoding(text[2:])
                            else:
                                return fixed_char
                except (ValueError, UnicodeDecodeError):
                    pass
    except Exception:
        pass
    
    return text


def fetch_html(url: str) -> str:
    # Be polite; some mirrors can be slow
    resp = requests.get(url, timeout=20, headers={'Accept-Charset': 'utf-8'})
    resp.raise_for_status()
    
    # Để requests tự detect encoding nhưng không decode
    # Sau đó tự decode với encoding đúng
    original_encoding = resp.apparent_encoding or resp.encoding or 'utf-8'
    
    # Thử decode như UTF-8 trước (vì meta tag nói charset=utf-8)
    html_utf8 = None
    try:
        html_utf8 = resp.content.decode('utf-8')
        # Kiểm tra xem có ký tự tiếng Việt không
        sample = html_utf8[:2000]
        vietnamese_count = sum(1 for c in sample if ord(c) >= 0x00C0 and ord(c) <= 0x1EF9)
        if vietnamese_count > 50:
            return html_utf8
    except UnicodeDecodeError:
        pass
    
    # Nếu UTF-8 decode được nhưng không có ký tự tiếng Việt, có thể bị double-encoding
    if html_utf8:
        vietnamese_count = sum(1 for c in html_utf8[:2000] if ord(c) >= 0x00C0 and ord(c) <= 0x1EF9)
        
        # Kiểm tra xem có pattern của double-encoding không
        if 'Ã' in html_utf8[:1000] or 'â€' in html_utf8[:1000]:
            # Có thể HTML thực sự là ISO-8859-1 nhưng được decode như UTF-8
            # Thử decode raw bytes như ISO-8859-1 rồi fix
            try:
                html_iso = resp.content.decode('iso-8859-1')
                # Nếu có nhiều ký tự tiếng Việt hơn, dùng cái này
                sample_iso = html_iso[:2000]
                vietnamese_count_iso = sum(1 for c in sample_iso if ord(c) >= 0x00C0 and ord(c) <= 0x1EF9)
                if vietnamese_count_iso > vietnamese_count:
                    return html_iso
            except UnicodeDecodeError:
                pass
            
            # Thử fix double-encoding cho toàn bộ HTML
            fixed = fix_double_encoding(html_utf8)
            sample_fixed = fixed[:2000]
            vietnamese_count_fixed = sum(1 for c in sample_fixed if ord(c) >= 0x00C0 and ord(c) <= 0x1EF9)
            if vietnamese_count_fixed > vietnamese_count:
                return fixed
    
    # Thử các encoding khác nếu UTF-8 không work
    for encoding in ['iso-8859-1', 'windows-1252', 'windows-1258', original_encoding]:
        if encoding == 'utf-8':
            continue
        try:
            html_content = resp.content.decode(encoding)
            sample = html_content[:2000]
            vietnamese_count = sum(1 for c in sample if ord(c) >= 0x00C0 and ord(c) <= 0x1EF9)
            if vietnamese_count > 50:
                return html_content
        except (UnicodeDecodeError, LookupError):
            continue
    
    # Fallback: dùng UTF-8 (có thể có lỗi nhưng vẫn parse được)
    return resp.content.decode('utf-8', errors='replace')


def extract_tables(html: str) -> List[pd.DataFrame]:
    # Parse với BeautifulSoup, đảm bảo không tự động decode lại
    # BeautifulSoup sẽ giữ nguyên encoding của HTML string
    soup = BeautifulSoup(html, "html.parser")
    tables_html = soup.find_all("table")
    if not tables_html:
        raise RuntimeError("Không tìm thấy bảng nào trên trang VietUnicode.")
    
    # Tìm bảng lớn nhất (bảng chứa mapping)
    dfs: List[pd.DataFrame] = []
    for tbl in tables_html:
        try:
            # Lấy header từ thead hoặc dòng đầu của tbody
            headers = []
            thead = tbl.find('thead')
            if thead:
                header_row = thead.find('tr')
                if header_row:
                    headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
            
            # Lấy data từ tbody hoặc từ table trực tiếp
            rows = []
            tbody = tbl.find('tbody')
            rows_html = (tbody.find_all('tr') if tbody else tbl.find_all('tr'))
            
            # Bỏ qua header row nếu không có thead
            start_idx = 1 if not thead and rows_html else 0
            
            for row in rows_html[start_idx:]:
                cells = []
                for td in row.find_all(['td', 'th']):
                    # Lấy text và fix encoding nếu cần
                    cell_text = td.get_text(strip=True)
                    # Fix double-encoding nếu có
                    cell_text = fix_double_encoding(cell_text)
                    cells.append(cell_text)
                if cells and len(cells) >= 2:
                    rows.append(cells)
            
            if not rows:
                continue
            
            # Tạo DataFrame từ data
            if headers and len(headers) == len(rows[0]):
                df = pd.DataFrame(rows, columns=headers)
            else:
                # Nếu không có header hoặc số cột không khớp, dùng số cột
                max_cols = max(len(row) for row in rows) if rows else 0
                if max_cols >= 5:  # Bảng mapping thường có >= 5 cột
                    df = pd.DataFrame(rows)
                    # Nếu có header từ dòng đầu
                    if rows and not headers:
                        df.columns = df.iloc[0] if len(df) > 0 else range(max_cols)
                        df = df[1:].reset_index(drop=True)
                else:
                    continue
            
            if df.shape[1] >= 5:  # Bảng mapping có nhiều cột
                dfs.append(df)
        except Exception:
            # Fallback: thử dùng pandas.read_html
            try:
                tbl_str = str(tbl)
                parsed = pd.read_html(StringIO(tbl_str), header=0)
                for df in parsed:
                    if df.shape[1] >= 5:
                        dfs.append(df)
            except Exception:
                continue
    
    # Nếu vẫn không có bảng, thử parse trực tiếp từ HTML với pandas
    if not dfs:
        try:
            dfs = pd.read_html(StringIO(html), header=0)
            # Lọc các bảng có nhiều cột
            dfs = [df for df in dfs if df.shape[1] >= 5]
        except Exception:
            pass
    
    if not dfs:
        raise RuntimeError("Không parse được bất kỳ bảng nào.")
    return dfs


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().upper() for c in df.columns]
    return df


def find_unicode_tcvn3_columns(df: pd.DataFrame) -> tuple[int, int, bool] | None:
    """
    Tìm cột Unicode và TCVN3 dựa trên tên cột hoặc nội dung.
    Trả về (unicode_col_idx, tcvn3_col_idx, is_unicode_hex) hoặc None nếu không tìm thấy.
    is_unicode_hex = True nếu cột Unicode chứa mã hex (U+00C0), False nếu chứa ký tự trực tiếp.
    """
    # Chuẩn hóa tên cột
    df_normalized = df.copy()
    df_normalized.columns = [str(c).strip().upper() for c in df.columns]
    
    # Tìm cột TCVN3 (không phải hex)
    tcvn3_col = None
    tcvn3_idx = None
    for idx, col in enumerate(df_normalized.columns):
        col_upper = str(col).upper()
        if "TCVN3" in col_upper and "HEX" not in col_upper:
            tcvn3_col = col
            tcvn3_idx = idx
            break
    
    if tcvn3_col is None:
        # Không tìm thấy cột TCVN3, không thể tiếp tục
        return None
    
    # Tìm cột Unicode - ưu tiên theo thứ tự:
    # 1. Cột "Viet" (cột đầu tiên thường chứa ký tự Unicode)
    # 2. Cột "Unicode" (không hex)
    # 3. Cột "Unicode Hex"
    
    unicode_col = None
    unicode_hex_col = None
    unicode_col_idx = None
    unicode_hex_col_idx = None
    
    # Tìm cột "Viet" trước (thường là cột đầu tiên)
    for idx, col in enumerate(df_normalized.columns):
        col_upper = str(col).upper()
        if col_upper in ["VIET", "V"] or (idx == 0 and "TCVN3" not in col_upper and "HEX" not in col_upper):
            # Kiểm tra xem cột này có chứa ký tự Unicode không
            sample_vals = df.iloc[:min(10, len(df)), idx].dropna().astype(str)
            unicode_count = sum(1 for v in sample_vals if len(v.strip()) == 1 and RE_UNI_CHAR.match(v.strip()))
            if unicode_count >= 3:  # Ít nhất 3 ký tự Unicode trong 10 mẫu
                unicode_col = col
                unicode_col_idx = idx
                break
    
    # Tìm cột "Unicode"
    if unicode_col is None:
        for idx, col in enumerate(df_normalized.columns):
            col_upper = str(col).upper()
            if "UNICODE" in col_upper:
                if "HEX" in col_upper:
                    if unicode_hex_col is None:
                        unicode_hex_col = col
                        unicode_hex_col_idx = idx
                else:
                    unicode_col = col
                    unicode_col_idx = idx
                    break
    
    # Quyết định cột nào dùng
    if unicode_col is not None:
        return (unicode_col_idx, tcvn3_idx, False)
    elif unicode_hex_col is not None:
        return (unicode_hex_col_idx, tcvn3_idx, True)
    
    # Fallback: dùng phương pháp đoán heuristic
    try:
        uni_idx, tcvn_idx = guess_cols(df)
        # Đảm bảo tcvn_idx khớp với cột TCVN3 đã tìm được
        if tcvn_idx == tcvn3_idx:
            return (uni_idx, tcvn_idx, False)
        else:
            # Nếu không khớp, dùng cả hai
            return (uni_idx, tcvn3_idx, False)
    except Exception:
        return None


def parse_unicode_hex(hex_str: str) -> str | None:
    """Chuyển đổi mã hex Unicode (U+00C0 hoặc 00C0) thành ký tự Unicode."""
    hex_str = str(hex_str).strip().upper()
    # Loại bỏ "U+" nếu có
    hex_str = hex_str.replace("U+", "").replace("U", "")
    try:
        code_point = int(hex_str, 16)
        return chr(code_point)
    except (ValueError, OverflowError):
        return None


def build_tcvn3_map() -> Dict[str, str]:
    html = fetch_html(VU_URL)
    dfs = extract_tables(html)

    mapping: Dict[str, str] = {}
    
    print(f"Tìm thấy {len(dfs)} bảng")
    
    for table_idx, df in enumerate(dfs):
        # Bỏ qua bảng có quá ít cột
        if df.shape[1] < 2:
            print(f"Bảng {table_idx}: Bỏ qua (quá ít cột: {df.shape[1]})")
            continue

        print(f"Bảng {table_idx}: shape={df.shape}, columns={list(df.columns)}")
        
        # Tìm cột Unicode và TCVN3
        cols = find_unicode_tcvn3_columns(df)
        if cols is None:
            print("  Không tìm thấy cột Unicode/TCVN3")
            continue
        
        uni_idx, tcvn_idx, is_unicode_hex = cols
        print(f"  Tìm thấy: Unicode cột {uni_idx} (hex={is_unicode_hex}), TCVN3 cột {tcvn_idx}")
        
        # Chuẩn hóa dữ liệu
        sub = df.iloc[:, [uni_idx, tcvn_idx]].copy()
        sub.columns = ['unicode', 'tcvn3']
        
        # Loại bỏ dòng trống
        sub = sub.dropna()
        print(f"  Sau khi loại bỏ dòng trống: {len(sub)} dòng")
        
        count_added = 0
        for _, row in sub.iterrows():
            u_val = str(row['unicode']).strip()
            t_val = str(row['tcvn3']).strip()
            
            # Bỏ qua nếu rỗng
            if not u_val or not t_val or u_val.lower() == 'nan' or t_val.lower() == 'nan':
                continue
            
            # Nếu cột Unicode là mã hex, chuyển đổi sang ký tự
            if is_unicode_hex:
                u_char = parse_unicode_hex(u_val)
                if u_char is None:
                    continue
                u_val = u_char
            elif u_val.startswith('U+'):
                # Cũng thử parse nếu có U+ prefix
                u_char = parse_unicode_hex(u_val)
                if u_char is not None:
                    u_val = u_char
            
            # Nếu unicode vẫn là hex code, thử parse
            if len(u_val) > 1 and u_val.startswith('U+'):
                u_char = parse_unicode_hex(u_val)
                if u_char is not None:
                    u_val = u_char
            
            # Chỉ lấy các cặp 1-ký-tự hợp lệ
            # Unicode có thể là ký tự hợp lệ hoặc TCVN3 cũng phải là 1 ký tự
            if len(t_val) == 1:
                # Nếu unicode là 1 ký tự hợp lệ
                if len(u_val) == 1:
                    # Không ghi đè mapping đã có (ưu tiên mapping đầu tiên)
                    if t_val not in mapping:
                        mapping[t_val] = u_val
                        count_added += 1
        
        print(f"  Đã thêm {count_added} mapping từ bảng này")

    if not mapping:
        raise RuntimeError("Không trích được mapping từ bất kỳ bảng nào. Hãy chạy --debug để xem chi tiết.")

    print(f"\nTổng cộng: {len(mapping)} mapping được tạo")
    return mapping

def save_outputs(mapping: Dict[str, str]) -> None:
    # JSON
    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    # CSV
    df = pd.DataFrame([(k, v) for k, v in mapping.items()], columns=["TCVN3", "UNICODE"])
    df.to_csv(OUT_CSV, index=False, encoding="utf-8")
    print(f"✅ Đã lưu {OUT_JSON.resolve()} và {OUT_CSV.resolve()} (entries: {len(mapping)})")


def load_map_offline() -> Dict[str, str]:
    if not OUT_JSON.exists():
        raise FileNotFoundError(f"Không thấy {OUT_JSON}. Chạy --build trước.")
    with OUT_JSON.open("r", encoding="utf-8") as f:
        return json.load(f)


def make_converter(mapping: Dict[str, str]):
    # Precompile one-pass regex
    pattern = re.compile("|".join(map(re.escape, mapping.keys())))
    return lambda s: pattern.sub(lambda m: mapping[m.group(0)], s)


def main():
    parser = argparse.ArgumentParser(description="Build & test offline TCVN3→Unicode map.")
    parser.add_argument("--build", action="store_true", help="Fetch from VietUnicode and save as JSON/CSV.")
    parser.add_argument("--test", type=str, help="Test convert a sample TCVN3 string using offline JSON.")
    args = parser.parse_args()

    if args.build:
        mapping = build_tcvn3_map()
        save_outputs(mapping)

    if args.test is not None:
        mapping = load_map_offline()
        convert = make_converter(mapping)
        print(convert(args.test))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--test", type=str)
    parser.add_argument("--debug", action="store_true")  # <<< thêm dòng này
    args = parser.parse_args()

    if args.debug:
        debug_headers()
        raise SystemExit

    if args.build:
        mapping = build_tcvn3_map()
        save_outputs(mapping)

    if args.test is not None:
        mapping = load_map_offline()
        convert = make_converter(mapping)
        print(convert(args.test))