# reader.py에서는 오직 엑셀 읽기와 선택적으로 로직용 컬럼 정리, 리터만 담당
# input() 같은 유저 인터랙션은 절대 넣지 않음

import os, tempfile, shutil
import pandas as pd
from config import excel_path, person_path, attachments


def _copy_to_local(src_path: str) -> str:

    tmp_dir = os.path.join(tempfile.gettempdir(), 'mail_sender_cache')
    os.makedirs(tmp_dir, exist_ok=True)
    dst = os.path.join(tmp_dir, os.path.basename(src_path))
    shutil.copy2(src_path, dst)

    return dst

def load_requests() -> pd.DataFrame:
    local_excel = _copy_to_local(excel_path)
    df = pd.read_excel(local_excel, engine='openpyxl')
    cols = [
        '기관명',
        '재평가/신규',
        '종목명',
        '법인번호',
        '평가종류코드',
        '메인GP 또는 의뢰업체',
        '담당자',
        '연락처',
        'email',
        '평가담당자',
        '자료요청담당'
        ]
    return df[[c for c in cols if c in df.columns]].copy()

def load_contacts() -> pd.DataFrame:
    local_person = _copy_to_local(person_path)
    return pd.read_excel(local_person, engine='openpyxl')


