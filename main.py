import requests
import json
import time
import re
from html import unescape

PAGE_FIELDS = {
    0: [
        "Name", "1_How_often_do_you_visit_gover", "2_What_is_your_role",
        "3_How_satisfied_are_you_with", "4_How_often_do_you_face_diffi",
        "5_Which_problem_do_you_face_m", "6_How_useful_would_a_single_p",
        "7_How_important_is_quick_acce", "8_How_useful_would_AI_generat",
        "9_How_important_are_notificat", "10_How_useful_would_category_b",
        "11_How_important_is_secure_lo", "12_How_important_is_cloud_bas",
        "13_How_useful_would_keyword_b", "14_How_useful_would_document",
        "15_How_important_is_mobile_fr", "16_Which_notice_category_do_y",
        "17_Which_features_would_you_p", "18_Would_you_trust_AI_generat",
        "19_Would_you_use_an_AI_powere", "20_Additional_comments_or_sug"
    ]
}
LAST_PAGE = max(PAGE_FIELDS.keys())


def extract_hidden_fields(html):
    """Pull all hidden <input> fields from the Google Forms response HTML."""
    fields = {}
    for tag in re.findall(r'<input[^>]+>', html, re.I):
        if 'hidden' not in tag.lower():
            continue
        name = re.search(r'name=["\']([^"\']+)["\']', tag)
        value = re.search(r'value=["\']([^"\']*)["\']', tag)
        if name:
            fields[name.group(1)] = unescape(value.group(1)) if value else ''
    return fields


class GoogleFormSubmitter:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.post_url = self.config['form_url']
        self.view_url = self.config.get('view_url', self.post_url.replace('/formResponse', '/viewform'))
        self.field_map = self.config['fields']

    def _new_session(self):
        s = requests.Session()
        s.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        return s

    def _load_form(self, session):
        resp = session.get(self.view_url)
        match = re.search(r'"fbzx"\s*value\s*=\s*"(-?\d+)"', resp.text)
        if not match:
            match = re.search(r'\["(-?\d{15,})"[,\]]', resp.text)
        return match.group(1) if match else self.config.get('static_data', {}).get('fbzx', '0')

    def _build_payload(self, page_data, page_num, fbzx, carried):
        payload = []

        # Field values for this page
        for key, value in page_data.items():
            if key not in self.field_map:
                continue
            entry_id = self.field_map[key]
            if isinstance(value, list):
                for item in value:
                    payload.append((entry_id, item))
            elif value is not None:
                payload.append((entry_id, str(value)))

        # Sentinel fields from previous page response (mark fields as "seen")
        for k, v in carried.items():
            if k.endswith('_sentinel'):
                payload.append((k, v))

        payload.append(('fvv', '1'))

        # pageHistory: use the one from the server response if available
        page_history = carried.get('pageHistory', ','.join(str(p) for p in range(page_num + 1)))
        payload.append(('pageHistory', page_history))

        payload.append(('fbzx', fbzx))

        # partialResponse: carry accumulated answers from server
        if 'partialResponse' in carried:
            payload.append(('partialResponse', carried['partialResponse']))
        else:
            payload.append(('draftResponse', '[]'))

        if 'submissionTimestamp' in carried:
            payload.append(('submissionTimestamp', carried['submissionTimestamp']))

        if page_num < LAST_PAGE:
            payload.append(('continue', '1'))

        return payload

    def submit(self, user_data, index=None):
        session = self._new_session()
        fbzx = self._load_form(session)
        label = user_data.get('Pseudonym', f'entry {index}')

        post_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://docs.google.com',
            'Referer': self.view_url,
        }

        carried = {}  # hidden fields extracted from each page response

        for page_num in range(LAST_PAGE + 1):
            keys = PAGE_FIELDS[page_num]
            page_data = {k: user_data[k] for k in keys if k in user_data}
            payload = self._build_payload(page_data, page_num, fbzx, carried)

            try:
                print(f"Payload for record {index}: {payload}")
                resp = session.post(self.post_url, data=payload, headers=post_headers)
            except Exception as e:
                print(f"[EXCEPTION] Record {index} ({label}) page {page_num}: {e}")
                return False

            if resp.status_code != 200:
                print(f"[ERROR] Record {index} ({label}) page {page_num}: HTTP {resp.status_code}")
                with open(f'error_p{page_num}.html', 'w') as f:
                    f.write(resp.text)
                return False

            if page_num < LAST_PAGE:
                # Extract hidden fields for the next page
                carried = extract_hidden_fields(resp.text)
                # Update fbzx if the server issued a new one
                if 'fbzx' in carried:
                    fbzx = carried.pop('fbzx')

            time.sleep(0.3)

        print(f"[SUCCESS] Record {index}: {label}")
        return True


def main():
    submitter = GoogleFormSubmitter('mapping_social.json')

    with open('generated_60_responses.json', 'r') as f:
        data_list = json.load(f)

    print(f"Submitting {len(data_list)} records (5 pages each)...")
    ok = 0
    for i, entry in enumerate(data_list, start=1):
        if submitter.submit(entry, index=i):
            ok += 1
        time.sleep(2)

    print(f"\nDone: {ok}/{len(data_list)} successful.")


if __name__ == "__main__":
    main()
